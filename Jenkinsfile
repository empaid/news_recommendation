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
                    sleep 120
                    sh "python3 test_staging.py"
                }
            }
        }
        stage('Release'){
          steps {
            step([$class: 'AWSCodeDeployPublisher', applicationName: 'newsomania', deploymentGroupAppspec: false, deploymentGroupName: 'newomaniaDeploymentgroup', excludes: '', iamRoleArn: '', includes: '**', proxyHost: '', proxyPort: 0, region: 'ap-southeast-2', s3bucket: 'newsomania-deployment', s3prefix: '', subdirectory: '', versionFileName: '', waitForCompletion: true])
           }
        }
        stage('Monitoring'){
          steps {
            script {
              sh 'chmod 400 "news-mania.pem" '
              sh ''' nohup ssh -i "news-mania.pem" ec2-user@ec2-13-211-98-55.ap-southeast-2.compute.amazonaws.com -t 'DD_API_KEY=e6c159b1b2240bd4854400c2fcd18603 DD_SITE="us5.datadoghq.com"  bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"' & '''
             }
           }
        }
    }
        post {
                success {
                    emailext attachLog: true,
                    to: "hardikpurohit26@gmail.com",
                    subject: "Build is successfull.",
                    body: "Please find the attached results of the build"
                }
                failure {
                    emailext attachLog: true,
                    to: "hardikpurohit26@gmail.com",
                    subject: "Build Failed",
                    body: "Please find the attached log of the build."
                }
                

                
                
        }
        
    
}