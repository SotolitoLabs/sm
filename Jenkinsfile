properties([pipelineTriggers([githubPush()])])

node {
   git url: 'https://github.com/SotolitoLabs/sm.git', branch: 'master'

    // This displays colors using the 'xterm' ansi color map.
//    ansiColor('xterm') {
        // Just some echoes to show the ANSI color.
//        stage "\u001B[31mI'm Red\u001B[0m Now not"
//    }

//    stage('Sync Development Environment') {
//        sh ('''
//            cd /var/sm
//            git pull
//        ''')
//    }
}


