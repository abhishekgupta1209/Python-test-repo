from exceptions.exceptions import NGSIUsageError, InvalidParameterValue
from flask import request
from reporter.reporter import _validate_query_params
from translators.factory import translator_for
import logging
import warnings
from .geo_query_handler import handle_geo_query
from utils.jsondict import lookup_string_match


def query_1TNE1A(attr_name,   # In Path
                 entity_type,
                 id_=None,  # In Query
                 aggr_method=None,
                 aggr_period=None,
                 aggr_scope=None,
                 options=None,
                 from_date=None,
                 to_date=None,
                 last_n=None,
                 limit=10000,
                 offset=0,
                 georel=None,
                 geometry=None,
                 coords=None,
                 id_pattern=None):
    """
    See /types/{entityType}/attrs/{attrName} in API Specification
    quantumleap.yml
    """

    r, c = _validate_query_params([attr_name],
                                  aggr_period,
                                  aggr_method,
                                  aggr_scope,
                                  options)
    if c != 200:
        return r, c

    r, c, geo_query = handle_geo_query(georel, geometry, coords)
    if r:
        return r, c

    fiware_s = request.headers.get('fiware-service', None)
    fiware_sp = request.headers.get('fiware-servicepath', '/')

    entities = None
    entity_ids = None
    if id_:
        entity_ids = [s.strip() for s in id_.split(',') if s]
    try:
        with translator_for(fiware_s) as trans:
            entities, err = trans.query(attr_names=[attr_name],
                                        entity_type=entity_type,
                                        entity_ids=entity_ids,
                                        aggr_method=aggr_method,
                                        aggr_period=aggr_period,
                                        aggr_scope=aggr_scope,
                                        from_date=from_date,
                                        to_date=to_date,
                                        last_n=last_n,
                                        limit=limit,
                                        offset=offset,
                                        idPattern=id_pattern,
                                        fiware_service=fiware_s,
                                        fiware_servicepath=fiware_sp,
                                        geo_query=geo_query)
    except NGSIUsageError as e:
        msg = "Bad Request Error: {}".format(e)
        logging.getLogger(__name__).error(msg, exc_info=True)
        return {
            "error": "{}".format(type(e)),
            "description": str(e)
        }, 400

    except InvalidParameterValue as e:
        msg = "Bad Request Error: {}".format(e)
        logging.getLogger(__name__).error(msg, exc_info=True)
        return {
            "error": "{}".format(type(e)),
            "description": str(e)
        }, 422

    except Exception as e:
        # Temp workaround to debug test_not_found
        msg = "Something went wrong with QL. Error: {}".format(e)
        logging.getLogger(__name__).error(msg, exc_info=True)
        return msg, 500

    if err == "AggrMethod cannot be applied":
        r = {
            "error": "AggrMethod cannot be applied",
            "description": "AggrMethod cannot be applied on type TEXT and BOOLEAN."}
        logging.getLogger(__name__).info("AggrMethod cannot be applied")
        return r, 404

    if entities:
        res = _prepare_response(entities,
                                attr_name,
                                entity_type,
                                entity_ids,
                                aggr_method,
                                aggr_period,
                                from_date,
                                to_date,)
        logging.getLogger(__name__).info("Query processed successfully")
        logging.warning(
            "usage of id and type rather than entityId and entityType from version 0.9")
        return res

    r = {
        "error": "Not Found",
        "description": "No records were found for such query."
    }
    logging.getLogger(__name__).info("No value found for query")
    return r, 404


def _prepare_response(entities, attr_name, entity_type, entity_ids,
                      aggr_method, aggr_period, from_date, to_date):
    values = {}
    for e in entities:
        matched_attr = lookup_string_match(e, attr_name)
        values[e['id']] = matched_attr['values'] if matched_attr else []

    if aggr_method and not aggr_period:
        # Use fromDate / toDate
        indexes = [from_date or '', to_date or '']
    else:
        indexes = {}
        for e in entities:
            indexes[e['id']] = e['index']

    # Preserve given order of ids (if any)
    entries = []
    if entity_ids:
        for ei in entity_ids:
            if ei in values:
                if aggr_method and not aggr_period:
                    index = indexes
                else:
                    index = indexes[ei]
                i = {
                    'entityId': ei,
                    'index': index,
                    'values': values[ei],
                }
                entries.append(i)
                values.pop(ei)

    # Proceed with the rest of the values in order of keys
    for e_id in sorted(values.keys()):
        index = [] if aggr_method and not aggr_period else indexes[e_id]
        i = {
            'entityId': e_id,
            'index': index,
            'values': values[e_id],
        }
        entries.append(i)

    res = {
        'entityType': entity_type,
        'attrName': attr_name,
        'entities': entries
    }
    return res


def query_1TNE1A_value(*args, **kwargs):
    res = query_1TNE1A(*args, **kwargs)
    if isinstance(res, dict):
        res.pop('entityType', None)
        res.pop('attrName', None)
        res['values'] = res['entities']
        res.pop('entities', None)
    logging.warning(
        "usage of id and type rather than entityId and entityType from version 0.9")
    return res