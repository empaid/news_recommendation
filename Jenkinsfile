pipeline {
    agent any
    
    stages {
        stage('Build'){
          steps {
            dir("backend") {
                sh "pip3 install -r requirements.txt";
            } 
            dir("frontend") {
                sh "npm install";
                dir("test_run"){
                  sh "npm install"
                }
            } 
          }
        }
        stage('Test'){
          steps{
            dir("backend") {
                sh "python3 main_test.py";
            }
            dir("frontend") {

                sh "npm run build";
                sleep 3
            }
          }
        }
        // stage('codedeploy'){
        //   steps {
        //     step([$class: 'AWSCodeDeployPublisher', applicationName: 'newsomania', deploymentGroupAppspec: false, deploymentGroupName: 'newomaniaDeploymentgroup', excludes: '', iamRoleArn: '', includes: '**', proxyHost: '', proxyPort: 0, region: 'ap-southeast-2', s3bucket: 'newsomania-deployment', s3prefix: '', subdirectory: '', versionFileName: '', waitForCompletion: true])
        //    }
        // }
        // stage('Code Analysis') {
        //      options {
        //         timeout(time: 1, unit: 'MINUTES')
        //     }
        //     steps {
        //         script {
        //             sh "touch .env"
        //             sh 'echo "IP=$SERVER_IP">>.env'
        //             sh "if [ \$(docker ps -qa)  ]; then docker rm -v -f \$(docker ps -qa); fi;"
        //             sh "sudo chown root:jenkins /run/docker.sock"
        //             sh 'nohup sudo docker compose up &'
        //             sleep 300
        //         }
        //     }
        // }
    }
}