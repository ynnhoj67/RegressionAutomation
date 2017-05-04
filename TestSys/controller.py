from Libs.Utility import *
import os

LOG_FILE = 'log.txt'
REGEX_RESULT_PASS = r'^<.+<status>.+<Framework>.+(Passs).+'
REGEX_RESULT_FAIL = r'^<.+<status>.+<Framework>.+(Fail).+'
REGEX_RESULT_SKIP = r'^<.+<status>.+<Framework>.+(Skip).+'

class TestSysController(object):

    def __init__(self,logger,parseConfig):
        """This class is used to control script, test execution and capture the result"""
        self.logger = logger
        self.parseConfig = parseConfig
        self.backUpDir = os.path.dirname(os.path.abspath(__file__))
        self.scriptCmd = os.path.abspath(self.parseConfig.getScript()).rstrip('\n')
        self.buildLocation = os.path.abspath(self.parseConfig.getBuildLocation()).rstrip('\n')
        self.testCmd = self.parseConfig.getCmd()
        self.pass_count = 0
        self.skip_count = 0
        self.fail_count = 0

    def runScript(self):
        self.logger.info("runScript %s" ,self.scriptCmd)
#        ret = runCommand(["sh", self.parseConfig.getScript()],None,None,None,True,False,True)
        ret = runCommand(['sh', self.scriptCmd],None,None,None,True,False,True)
        self.logger.info("ret: %d" ,ret)
        if ret != 0:
            self.logger.error("Test system running Script error code: %d", ret)
        return ret

    def runTest(self):
        self.logger.info("runTest at %s" , self.buildLocation)
        os.chdir(os.path.abspath(self.buildLocation))
        self.logger.info("Changed to build location ")
        #remove old log
        self.logger.info("Removing previous log")
        removeLogFile(LOG_FILE, self.buildLocation)
        self.logger.info("Executing cmd: %s", self.testCmd)
        ret, stdout = runCommand(self.testCmd,None,None,None,True,False,False)
        print ("############# ret %d" %ret)
        #if ret != 0:
        #    self.logger.error("Test System run test error, please check cmd is correct")
        #    self.logger.error(stdout)
        #    ret = RESULT_UNKNOW
        #else:
        self.logger.info(stdout)
        ret = self.getResult()
        os.chdir(self.backUpDir)
        return ret

    def getResult(self):
        self.logger.info("Parse test result after its complete")
        os.chdir(self.buildLocation)
        #parse
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as logs:
                for line in logs:
                    ret = regXpParse(line, REGEX_RESULT_PASS)
                    if ret != 'NotFound':
                        self.pass_count += 1
                    ret = regXpParse(line, REGEX_RESULT_FAIL)
                    if ret != 'NotFound':
                        self.fail_count += 1
                    ret = regXpParse(line, REGEX_RESULT_SKIP)
                    if ret != 'NotFound':
                        self.skip_count += 1
            self.logger.info("Passing count: %d " %self.pass_count)
            self.logger.info("Skipping count: %d " %self.skip_count)
            self.logger.info("Failing count: %d " %self.fail_count)

            if self.pass_count == 0 and self.skip_count == 0 and self.fail_count == 0:
                self.logger.info("This run Crashed")
                ret = RESULT_CRASH['CRASH\n']
            elif self.fail_count != 0:
                self.logger.info("This run Failed")
                ret = RESULT_FAIL['FAIL\n']
            elif self.skip_count != 0:
                self.logger.info("This run Skipped")
                ret = RESULT_SKIP['SKIP\n']
            else:
                self.logger.info("this run Passed")
                ret = RESULT_PASS['PASS\n']
        else:
            self.logger.info("Log is missing, either test crashed or hang")
            ret = RESULT_CRASH['CRASH\n']
        return ret

