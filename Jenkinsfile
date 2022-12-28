node{
  stage('Checkout') {
        
        deleteDir()
        checkout scm
    }
  stage ("Stage 1"){
    sh 'python3 --version'
    sh "sudo -S En18el301157 ./run_tests.sh"
    sh 'coverage run --source=./src/tests -m unittest discover -s ./src/tests'
//     sh "coverage combine"
    sh 'coverage report'
    sh 'coverage xml'
    publishCoverage adapters: [jacocoAdapter('coverage.xml')]
  }
  
}
