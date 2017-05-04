from Libs.Utility import *

class ParseConfig(object):

    def __init__(self,logger,configFile):
        """This class is used to parse Dev config file"""
        self.logger = logger
        self.configFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), configFile)
        self.tempConfigFile = os.path.join(os.path.dirname(os.path.abspath(__file__)),TEMP_CONFIG_FILE)
        self.status = 0
        self.getTempConfigFile()
        self.svnDir = ""
        self.cmakeCmd = ""
        self.cmakeCmdStr = ""
        self.makeCmd = ""
        self.makeCmdStr = ""
        self.buildFolder = ""
        self.cleanBuild = False
        self.topRev = "TOTT"
        self.botRev = "CURR"
        self.testSysIp = ""
        self.testTime = 0
        self.rebootTime = 0
        self.regression = ""

    def getConfigFile(self):
        """Read config file to parse each item. Checks if need continue or start from new"""
        ret = True
        if self.status == REGRESSION_START_NEW:
                ret = self.readFile()
        else:
            #parse tempConfigFile
            self.configFile = self.tempConfigFile
            ret = self.readFile()
        return ret

    def readFile(self):
        if os.path.exists(self.configFile):
            with open(self.configFile, "r") as configs:
                for line in configs:
                    if line[0] != '#':
                        content = line.split(':')
                        self.logger.info("content %s" %content)
                        if content[0] == "SvnBuildDir":
                            self.logger.info("svn build dir : %s" %content[1])
                            self.svnDir = content[1].rstrip('\r\n')
                        elif content[0] == "CmakeCmd":
                            self.cmakeCmdStr = content[1].rstrip('\r\n')
                            self.cmakeCmd = content[1].split(' ')
                            self.cmakeCmd[-1] = self.cmakeCmd[-1].rstrip('\r\n')
                            self.logger.info("cmake cmd: %s" %self.cmakeCmd)
                        elif content[0] == "MakeCmd":
                            self.makeCmdStr = content[1].rstrip('\r\n')
                            self.makeCmd = content[1].split(' ')
                            self.makeCmd[-1] = self.makeCmd[-1].rstrip('\r\n')
                            self.logger.info("cmake cmd: %s" %self.makeCmd)
                        elif content[0] == "BuildFolder":
                            self.logger.info("build folder: %s" %content[1])
                            self.buildFolder = content[1].rstrip('\r\n')
                        elif content[0] == "CleanBuild":
                            self.logger.info("clean build: %s" %content[1])
                            self.cleanBuild = content[1].rstrip('\r\n')
                        elif content[0] == "TopRev":
                            self.logger.info("top rev: %s" %content[1])
                            self.topRev = content[1].rstrip('\r\n')
                        elif content[0] == "BotRev":
                            self.logger.info("bot rev: %s" %content[1])
                            self.botRev = content[1].rstrip('\r\n')
                        elif content[0] == "TestSystemIP":
                            self.logger.info("test sys ip: %s" %content[1])
                            self.testSysIp = content[1].rstrip('\r\n')
                        elif content[0] == "TestTime":
                            self.logger.info("Test time: %s" %content[1])
                            self.testTime = content[1].rstrip('\r\n')
                        elif content[0] == "RebootTime":
                            self.logger.info("Reboot time: %s" %content[1])
                            self.rebootTime = content[1].rstrip('\r\n')
                        elif content[0] == "Regression":
                            self.logger.info("Regression: %s" %content[1])
                            self.regression = content[1].rstrip('\r\n')
            ret = True
        else:
            self.logger.error("Config file: %s not found " %self.configFile)
            ret = False
        return ret

    def getTempConfigFile(self):
        """Read temp config file"""
        if os.path.exists(self.tempConfigFile):
            self.logger.info("tempConfigFile exists..continue from last left over")
            self.setStatus(REGRESSION_CONTINUE)
        else:
            self.logger.info("Starting new")
            #Log the current status in tempConfig
            self.setStatus(REGRESSION_START_NEW)

    def setStatus(self, st):
        self.status = st

    def getStatus(self):
        return self.status

    def getSvnDir(self):
        return self.svnDir

    def getCmakeCmd(self):
        return self.cmakeCmd

    def getCmakeCmdStr(self):
        return self.cmakeCmdStr

    def getMakeCmd(self):
        return self.makeCmd

    def getMakeCmdStr(self):
        return self.makeCmdStr

    def getBuildFolder(self):
        return self.buildFolder

    def getCleanBuild(self):
        return self.cleanBuild

    def getTopRev(self):
        return self.topRev

    def getBotRev(self):
        return self.botRev

    def getTestSysIp(self):
        return self.testSysIp

    def getTestTime(self):
        return self.testTime

    def getRebootTime(self):
        return self.rebootTime

    def getRegression(self):
        return self.regression

    def removeTempFile(self):
        ret = removeFile(self.tempConfigFile)
        if ret != 0:
            self.logger.error("Remove temp file error")


