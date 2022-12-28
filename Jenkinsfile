node{
  stage('Checkout') {
        
        deleteDir()
        checkout scm
    }
  stage ("Stage 1"){
    sh 'python3 --version'
    sh 'ls'
    dir("src") {
    sh "pwd"
    sh 'python3  -m unittest discover ./src/reporter/tests'
    sh 'coverage run --source=./src/reporter/tests -m unittest discover -s ./src/reporter/tests'
//     sh "echo En18el301157 | sudo -S chmod +x ./run_tests.sh"
//     sh "./run_tests.sh"
//     sh 'coverage run --source=./src/tests -m unittest discover -s ./src/tests'
//     sh "coverage combine"
    sh 'coverage report'
    sh 'coverage xml'
    }
//     publishCoverage adapters: [jacocoAdapter('coverage.xml')]
  }
  
}
