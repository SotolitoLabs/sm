properties([pipelineTriggers([githubPush()])])

node {
    // This displays colors using the 'xterm' ansi color map.
//    ansiColor('xterm') {
        // Just some echoes to show the ANSI color.
//        stage "\u001B[31mI'm Red\u001B[0m Now not"
//    }
 

    //TODO: check if username and email are already configured
    stage('Setup Environment') {
        sh ('''
            cd /var/sm/
            git config --global user.email "git@sotolitolabs.com"
            git config --global user.name "Super Duper Sotolito User"
        ''')
    }

  
    stage('Sync Development Environment') {
        if (env.BRANCH_NAME ==~ /master/) {
          sh ('''
              cd /var/sm/
              git pull
              echo "Reload application"
              touch src/reload.me
          ''')
       }
    }
}


