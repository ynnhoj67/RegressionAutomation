import threading
from Libs.Utility import *

class FuncThread(threading.Thread):
    
    def __init__(self, logger, *args):
        self.logger = logger
        self._args = args
        threading.Thread.__init__(self)
    
    
    def run(self):
        self.logger.info("Thread started")
        self._target(*self._args)
    
    
    def setTarget(self, target):
        self._target = target
    
    def launchVertex(self, *args):
        self.logger.info("starts vertex with command: %s" %args[0])
        os.system(args[0])

    def stopVertex(self):
        self.logger.info("stop vertex")
        terminateProcess('vertexperf')
