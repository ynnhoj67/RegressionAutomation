from Libs.ServerSocket import ServerSocket
from Libs.Logger import RegressionLogger
from Libs.Utility import *
from setup import RegressionSetUp
from controller import TestSysController
import os, commands, sys

def InitConnection():
    timeStamp = getTime()
    logger = RegressionLogger(timeStamp)

    logger.info("logging info")
    server = ServerSocket(logger)
    server.startListen()


#InitRegressionAuto()

def parseConfig():
    timeStamp = getTime()
    logger = RegressionLogger(timeStamp)
    curDir = os.path.dirname(os.path.abspath(__file__))

    logger.info("sys argv len: %d", len(sys.argv))
    #check for missing cog file
    if len(sys.argv) < 2 :
        logger.error("Missing config file ")
    else:
        conf = os.path.join(curDir, sys.argv[1])
        print "cconf: %s" %conf
        if os.path.exists(conf):
            parse = RegressionSetUp(logger, timeStamp,conf)
            parse.getConfigFile()
            ##creating controller
            control = TestSysController(logger,parse)
            server = ServerSocket(logger,control)
            server.startListen()
            #ret = control.runScript()
            #ret = control.runTest()
            #logger.info("Result %d" %ret)
        else:
            logger.error("Config file doesn't exist: %s" %conf)

parseConfig()


