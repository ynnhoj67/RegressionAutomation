from Libs.Utility import *

class RegressionSetUp(object):
    """Set up class to parse config file and execute script and test"""

    def __init__(self, logger, timeStamp, configFile):
        """Init class, this class is used to parse the config file"""
        self.logger = logger
        self.timeStamp = timeStamp
        self.configFile = configFile
        self.scriptFile = ""
        self.cmd = []
        self.buildLocation = ""

    def getConfigFile(self):
        """Read config file to parse each item"""
        if os.path.exists(self.configFile):
            with open(self.configFile, "r") as configs:
                for line in configs:
                    content = line.split(':')
                    if content[0] == "script":
                        self.logger.info("script: %s",content[1])
                        self.scriptFile = content[1]
                    elif content[0] == "build_location":
                        self.logger.info("build_location: %s", content[1])
                        self.buildLocation = content[1]
                    elif content[0] == "cmd":
                        self.cmd = content[1].split(' ')
                        self.cmd[-1] = self.cmd[-1].rstrip('\n')
                        self.logger.info("cmd: %s", self.cmd)
        else:
            self.logger.error("Config file not found : %s" %self.configFile)
            exit()

    def getScript(self):
        return self.scriptFile

    def getCmd(self):
        return self.cmd

    def getBuildLocation(self):
        return self.buildLocation
