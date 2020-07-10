// The super duper SotolitoLabs Pipeline with ketchup
node {
    // This displays colors using the 'xterm' ansi color map.
    ansiColor('xterm') {
        // Just some echoes to show the ANSI color.
        stage "\u001B[31mI'm Red\u001B[0m Now not"
    }


    stage('Sync Development') {
        when {
            branch 'master'
        }

        steps {
            sh ('''
                cd /home/ichavero/sotolitoLabs/sm/
                git pull
            ''')
        }
    }


}


