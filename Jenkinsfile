pipeline {
  agent any
  stages {
    stage('Model  ') {
      parallel {
        stage('Model  ') {
          steps {
            sh '''echo "Design"
'''
            sh '''echo "ModelAdvisor"
'''
          }
        }

        stage('') {
          steps {
            sh '''echo "design"
'''
            sh 'echo "modelAdivsor"'
          }
        }

      }
    }

    stage('') {
      steps {
        sh 'echo "functionalTest"'
      }
    }

  }
}