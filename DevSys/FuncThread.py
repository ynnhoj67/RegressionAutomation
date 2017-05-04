import threading, time
from Utility import *
#server ssh info
#SERVERIP = "172.27.226.209"
SERVER_USR = "atiqa"
SERVER_PW = "atiqa"
#SERVER_SCRIPT = 'bash /Users/atiqa/Desktop/PowerAuto/launch.sh'
SERVER_SCRIPT = 'python /Users/atiqa/Desktop/PowerAuto/FirstTimeLaunch.py'

class FuncThread(threading.Thread):
    
    def __init__(self, logger, queue, ip, tgraph , timer = 0):
        self.logger = logger
#        self._args = args
        self.queue = queue
        self.serverIp = ip
        self.tgraph = tgraph
        self.timer = timer
        threading.Thread.__init__(self)
    
    
    def run(self):
        self.logger.info("Thread started")
        self._target()

    
    def setTarget(self, target):
        self._target = target
    
    def autoLaunch(self):
        
        sshHost = SERVER_USR + "@" + self.serverIp #SERVER_USR + ":" + SERVER_PW + "@" + SERVERIP
        self.logger.info("ssh into : %s" %sshHost)

        ret = runCommand(["ssh", sshHost, SERVER_SCRIPT], None, None, None, False, False, True)
        time.sleep(5)
        self.logger.info("successfully launched server side program")
        self.queue.put("Launched")
#        if ret == 0:
#            self.logger.info("successfully launch server side program")
#            self.queue.put("Launched")
#        
#        elif ret == 1:
#            self.logger.error("launch server side program error...please check connection")
#            self.queue.put("Launch Error")

#
    def launchtGraph(self):
        self.tgraph.startApp()

    def startTimer(self):
        self.logger.info("count down timer starts: %d" %self.timer)
        while self.timer > 0:
            time.sleep(1)
            self.timer = self.timer - 1
        self.logger.info("Timer expired TO DO SOMETHING HERE")
        self.queue.put("TimerExpired")

