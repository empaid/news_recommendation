pipeline {
    agent any
    
    stages {
        stage('codedeploy'){
          steps {
            step([$class: 'AWSCodeDeployPublisher', applicationName: 'newsomania', deploymentGroupAppspec: false, deploymentGroupName: 'newomaniaDeploymentgroup', excludes: '', iamRoleArn: '', includes: '**', proxyHost: '', proxyPort: 0, region: 'ap-southeast-2', s3bucket: 'newsomania-deployment', s3prefix: '', subdirectory: '', versionFileName: '', waitForCompletion: true])
           }
        }
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