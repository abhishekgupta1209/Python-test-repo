node{
  stage('Checkout') {
        
        deleteDir()
        checkout scm
    }
  stage ("Stage 1"){
    sh 'python3 --version'
//     sh 'coverage run test_test1.py'
    sh "coverage combine 
    sh 'coverage report'
    sh 'coverage xml'
    publishCoverage adapters: [jacocoAdapter('coverage.xml')]
  }
  
}
