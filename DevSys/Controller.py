"""
Controller.py
Author: Johnny Zhang
Date: May 2017
"""
from Libs.Utility import *

class Controller(object):

    def __init__(self, logger, topRev, botRev, revList, parser):
        """This is the main controller class.It finds the next rev till complete"""
        self.logger = logger
        self.topRev = topRev
        self.botRev = botRev
        self.revList = revList
        self.parser = parser



    def setTempConfig(self):
        """Writes to TempConfig file for resume purpose"""
        self.logger.info("Generating TempConfig")
        #need to remove the old one first
        removeFile(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),TEMP_CONFIG_FILE)))

        data = "SvnBuildDir:" + self.parser.getSvnDir() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "CmakeCmd:" + self.parser.getCmakeCmdStr() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "MakeCmd:" + self.parser.getMakeCmdStr() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "BuildFolder:" + self.parser.getBuildFolder() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "CleanBuild:" + self.parser.getCleanBuild() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        #HERE NEED TO UPDATE THE NEW TOPREV and BOTREV
        data = "TopRev:" + str(self.topRev) + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "BotRev:" + str(self.botRev) + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')

        data = "TestSystemIP:" + self.parser.getTestSysIp() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "TestTime:" + self.parser.getTestTime() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "RebootTime:" + self.parser.getRebootTime() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')
        data = "Regression:" + self.parser.getRegression() + "\r\n"
        self.logger.info("writing data: %s" %data)
        writeToFile(TEMP_CONFIG_FILE, data, os.path.dirname(os.path.abspath(__file__)), 'a')


