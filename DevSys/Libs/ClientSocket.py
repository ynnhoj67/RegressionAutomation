import socket,os
import time
from Utility import *
from socket import error as SocketError
import errno


#from FuncThread import FuncThread

PORT_NUMBER = 65534
PACKET_SIZE = 512
#EACH_RUN_LOOP_TIME = 60 #est 50mins which is 3000 sec

class ClientSocket(object):
    """Client Server Class"""
    def __init__(self, serverIp, logger, retryTimer, timeStamp):
        """ init client and logger"""
        self.client = socket.socket()
        self.timeStamp = timeStamp
        self.logFolder = RESULT_FILE_DIR + self.timeStamp
        self.host = serverIp
        self.port = PORT_NUMBER
        self.logger = logger
        self.retryTimer = retryTimer
        self.waitForResult = 5
        self.status = -1  #use this status to check if server has connection, may not needed
        self.regressionStatus = REGRESSION_STATUS_UNKNOWN
#        self.connect()

    def connect(self):
        '''It connects the server, if received 'Connected' means its connected then send test list'''
        self.logger.info("Dev System trying to connect to test system")
        self.logger.info("retry %d" %self.retryTimer)
        tryAgain = 0
        while tryAgain < self.retryTimer:
            try:
                self.client.connect((self.host, self.port))
            except Exception as e:
                self.logger.info("Re-trying connectiong to test system")
                sleep(1)
                tryAgain += 1
                self.status = -1
            else:
                msgRecv = self.client.recv(512)
                self.logger.info('received: %s' %msgRecv)
                if msgRecv == "Connected\n":
                    self.logger.info("Server connected")
                    self.createCommunication()
                    self.status = 1
                    tryAgain = self.retryTimer
                else:
                    self.logger.info("NO response from Test System")
                    self.status = -1
                    #sleep(1)
                    #tryAgain += 1
        if self.status == -1:
            self.logger.error("Client Lost Connection..Please make sure server is launched on test system.")
            #exit
            self.closeSocket()

    def closeSocket(self):
        ''' Close the socket '''
        self.client.close
        self.logger.info("connection closed")


    def sendTestCmd(self):
        self.client.send('SEND_TEST_CMD\n')
        #mimicing tserver lite cmd...need to read it from a file
        self.client.send('sudo ./tserverlite -d=1,2 -test=abcd123.123 -vm -disable_libdce -tsl_ucode_load -tc_ucode_load -tc_TCorePrefersysmeminternally -pm4ib=system -pm4rb=system -ucode-sysmem=true')
        while True:
            msgRecv = self.client.recv(PACKET_SIZE)
            if msgRecv == 'TEST_CMD_RECEIVED\n':
                self.logger.info('server received test cmd and going to execute')
                break

    def createCommunication(self):
        '''This is used for main communication with server.'''
        self.logger.info("client communication created")
        #send msg to server inform start communication, server read config file locally no need to send it
        #self.sendTestCmd()
        self.client.send('RUN_SCRIPT')
        while True:
            msgRecv = self.client.recv(512)
            self.logger.info('Client Reveived %s',msgRecv)
            if len(msgRecv) != 0:
                if msgRecv == 'SCRIPT_DONE\n':
                    self.logger.info('pre-test script completed')
                    self.client.send('RUN_TEST\n')
                    #NEED TO FIGURE A WAY to check timer
                if msgRecv == 'SCRIPT_ERROR\n':
                    self.logger.error('pre-test script encountered error')
                    self.regressionStatus = REGRESSION_STATUS_SCRIPT_ERROR
                    break
                if msgRecv == 'STARTED_RUNNING_TEST\n':
                    #waiting for result if not received in 10mins error, system hang
                    #Dumb way..to wait for approximite test time
                    self.logger.info("wait for test to complete")
                    sleep(self.waitForResult)   #this can be modified
                    #prob for result
                    try:
                        self.client.send('RESULT_CHECK\n')
                        while True:
                            resultRecv = self.client.recv(512)
                            self.logger.info("resultRecv %s", resultRecv)
#                            while self.waitForResult < 10: #need to adjust this timer
                            if resultRecv == 'PASS\n':
                                #good
                                self.regressionStatus = REGRESSION_STATUS_PASS
                                self.logger.info("This run passed")
                                break
                            elif resultRecv == 'FAIL\n':
                                #fail
                                self.regressionStatus = REGRESSION_STATUS_FAIL
                                self.logger.info("This run Fail")
                                break
                            elif resultRecv == 'SKIP\n':
                                #skip
                                self.regressionStatus = REGRESSION_STATUS_SKIP
                                self.logger.info("This run SKIP")
                            #elif resultRecv == 'NORESULT\n':
                            #    #bad
                            #    self.regressionStatus = REGRESSION_STATUS_CRASH
                            #    self.logger.info("This run crashed")
                            #    break
                            elif resultRecv == 'CRASH\n':
                                #CRASH
                                self.regressionStatus = REGRESSION_STATUS_CRASH
                                self.logger.info("This run crashed")
                                break
                            else:
                                self.logger.info("Test system hang")
                                self.regressionStatus = REGRESSION_STATUS_HANG
                                break

                    except socket.error:
                        self.logger.info("No response, test system seems hung")
                        self.regressionStatus = REGRESSION_STATUS_HANG
                        self.closeSocket()
                        break
                    #need to make decision ...here....svn sync...build...
                    self.logger.info("after decision send cmd to test system")
                    break
                    #send reboot if no result / otherwise send terminate
                    #self.client.send('TERMINATE\n')
            else:  #this case means server socket disconnected
                self.logger.error("Server is disconnected or rebooting")
                #NEED TO retry after reboot time, if no response then system hang
                break

    def sendInstruction(self, msg):    #send TERMINATE\n when the entire process is completed
        self.logger.info("Sending %s to test system", msg)
        #need to check if the socket has connection or not then send inst
        try:
            self.client.send(msg)
        except socket.error:
            self.logger.error("Connection error with TestSystem")

    def getStatus(self):
        return self.status

    def getRegressionStatus(self):
        return self.regressionStatus

    def setTimer(self, timer):
        self.timerThread = FuncThread(self.logger, self.queue, None, None, timer)
        self.timerThread.setTarget(timerThread.startTimer)
        self.timerThread.start()

