"""
RegressionClient.py
Author: Johnny Zhang
Date: May 2017
"""
from Libs.ClientSocket import ClientSocket
from Libs.Logger import RegressionLogger
from Libs.Utility import *
import os, commands,sys
from Svn import CSvn
from ParseConfig import ParseConfig
from Controller import Controller

SERVER_IP = '10.1.37.21'
RETRY_TIMER = 10

#debug parsing file func
def testParse(parser):
    print "getStatus(): %s " %parser.getStatus()
    print "getSvnDir: %s " %parser.getSvnDir()
    print "getCmakeCmd: %s " %parser.getCmakeCmd()
    print "getMakeCmd: %s " %parser.getMakeCmd()
    print "getBuildFolder: %s " %parser.getBuildFolder()
    print "getTopRev: %s " %parser.getTopRev()
    print "getBotRev: %s " %parser.getBotRev()
    print "getTestSysIp: %s " %parser.getTestSysIp()
    print "getTestTime: %s " %parser.getTestTime()
    print "getRebootTime: %s " %parser.getRebootTime()

#Build
def svnOperation(svn,logger):
    status = 0
    ret = svn.runCmake()
    if ret == REGRESSION_STATUS_CMAKE_OK:
        logger.info("cmake done")
#DEBUG TEMP REMOVE RUNMAKE
        #status = svn.runMake()
        return status
    else:
        logger.error("cmake error %s " %ret)
        return ret

def InitClient():
    """This is the main method"""
    timeStamp = getTime()
    logger = RegressionLogger(timeStamp)
    #checking if config file is supplied
    if len(sys.argv) < 2:
        logger.error("Missing config file ")
    else:
        logger.info("ParseConfig init")
        parser = ParseConfig(logger,sys.argv[1])
        ret = parser.getConfigFile()
        if ret != True:
            logger.error("Error reading config file..terminate")
            exit()

        logger.info("CSVN init")
        svn = CSvn(logger, parser.getSvnDir(), parser.getCmakeCmd(), parser.getMakeCmd(), parser.getBuildFolder(), parser.getCleanBuild(),  parser.getTopRev(), parser.getBotRev())

        logger.info("Controller init")
        controller = Controller(svn.getTopRev(), svn.getBotRev(), svn.getRevList(), parser)

        status = svnOperation(svn,logger)
        if status == REGRESSION_STATUS_BUILD_ERROR:
            #MOVE ON TO NEXT REV...NEED TO DO
            logger.error("BUILD ERROR @...")
        elif status == REGRESSION_STATUS_BUILD_OK:
            #NEED TO WORK ON
            pass
        elif status == REGRESSION_STATUS_CMAKE_ERROR:
            #SHALL WE EXIT HERE?
            logger.error("Please fix cmake command or build directory before resume automation")
            exit()

#        logger.info("Client init")
#        client = ClientSocket( parser.getTestSysIp(), logger, RETRY_TIMER, timeStamp)
#        client.connect()

        #sleep(10)
        #client.sendInstruction('REBOOT\n')

#InitClient()


def testingController():
    timeStamp = getTime()
    logger = RegressionLogger(timeStamp)
    parser = ParseConfig(logger,sys.argv[1])
    ret = parser.getConfigFile()
    logger.info("svnDir: %s" %parser.getSvnDir())
    svn = CSvn(logger, parser.getSvnDir(), parser.getCmakeCmd(), parser.getMakeCmd(), parser.getBuildFolder(), parser.getCleanBuild(),  parser.getTopRev(), parser.getBotRev())
    logger.info("Controller init")
    controller = Controller(logger, svn.getTopRevInit(), svn.getBotRevInit(), svn.getRevList(), parser)
    controller.setTempConfig()
    status = svnOperation(svn,logger)
    if status == REGRESSION_STATUS_BUILD_ERROR:
        #MOVE ON TO NEXT REV...NEED TO DO
        logger.error("BUILD ERROR @%s" %svn.getCurRev())
    elif status == REGRESSION_STATUS_BUILD_OK:
        #NEED TO WORK ON
        logger.info("BUILD COMPLETE")
        pass
    elif status == REGRESSION_STATUS_CMAKE_ERROR:
        logger.error("cmake error")
        #SHALL WE EXIT HERE?


testingController()
