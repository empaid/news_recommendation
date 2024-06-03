pipeline {
    agent any
    
    stages {
        stage('Build'){
          steps {
            dir("backend") {
                sh "pip3 install -r requirements.txt";
            } 
            nodejs(nodeJSInstallationName: 'nodejs'){
              dir("frontend") {
                  sh "npm install";
                  sh "npm run build";
                  dir("test_run"){
                    sh "npm install"
                  }
              } 
            }
          }
        }
        stage('Test'){
          steps{
            dir("backend") {
                sh "python3 main_test.py";
            }
            nodejs(nodeJSInstallationName: 'nodejs'){
            dir("frontend") {

                sh "nohup npm start &";
                sleep 3
                  sh "python3 tests.py"
            }}
          }
        }
        stage('Deploy') {
            steps {
                script {
                    sh "touch .env"
                    sh 'echo "IP=$SERVER_IP">>.env'
                    sh "if [ \$(docker ps -qa)  ]; then docker rm -v -f \$(docker ps -qa); fi;"
                    sh "sudo chown root:jenkins /run/docker.sock"
                    sh 'nohup sudo docker compose up &'
                    sleep 300
                }
            }
        }
        // stage('codedeploy'){
        //   steps {
        //     step([$class: 'AWSCodeDeployPublisher', applicationName: 'newsomania', deploymentGroupAppspec: false, deploymentGroupName: 'newomaniaDeploymentgroup', excludes: '', iamRoleArn: '', includes: '**', proxyHost: '', proxyPort: 0, region: 'ap-southeast-2', s3bucket: 'newsomania-deployment', s3prefix: '', subdirectory: '', versionFileName: '', waitForCompletion: true])
        //    }
        // }
        
    }
}