properties([pipelineTriggers([githubPush()])])

node {
    // This displays colors using the 'xterm' ansi color map.
//    ansiColor('xterm') {
        // Just some echoes to show the ANSI color.
//        stage "\u001B[31mI'm Red\u001B[0m Now not"
//    }

    stage('Sync Development Environment') {
        sh ('''
            cd /var/sm/src/sm/sm
            cp settings.py.orig settings.py
            git pull
            cp settings.py.dev settings.py
        ''')
    }
}


