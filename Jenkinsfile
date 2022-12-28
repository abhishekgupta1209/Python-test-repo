node{
  stage('Checkout') {
        
        deleteDir()
        checkout scm
    }
  stage ("Stage 1"){
    sh 'python3 --version'
    sh 'ls'
    dir("src") {
       try{
        
           sh 'python3  -m unittest discover ./reporter/tests'
        }
     catch(e) {
        build_ok = false
        echo e.toString()  
    }
    sh "pwd"
    try{
        
          sh 'coverage run --source=./reporter/tests -m unittest discover -s ./reporter/tests'
        }
    catch(e) {
        build_ok = false
        echo e.toString()  
    }
//     sh 'python3  -m unittest discover ./reporter/tests'
//     sh 'coverage run --source=./reporter/tests -m unittest discover -s ./reporter/tests'
//     sh "echo En18el301157 | sudo -S chmod +x ./run_tests.sh"
//     sh "./run_tests.sh"
//     sh 'coverage run --source=./src/tests -m unittest discover -s ./src/tests'
//     sh "coverage combine"
    sh 'coverage report'
    sh 'coverage xml'
//       publishCoverage adapters: [jacocoAdapter('coverage.xml')]
      cobertura autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '70, 0, 0', failUnhealthy: false, failUnstable: false, lineCoverageTargets: '80, 0, 0', maxNumberOfBuilds: 0, methodCoverageTargets: '80, 0, 0', onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false
 
    }
     }
  
}
