import socket, re, os
from Libs.Utility import *
import time


PORT_NUMBER = 65534
PACKET_SIZE = 512
REGEX_IP = r'^\(\'(.+)\'.+'


class ServerSocket(object):
    """ Server socket class """
    testCmd = []
    def __init__(self, logger, controller):
        """ init Server """
        self.logger = logger
        self.controller = controller
        self.logger.info("initizing server...waiting for connection")
        self.server = socket.socket()        #create socket object
#        self.server.settimeout(60)       #sets timeout for socket
        self.host = ''  #it will listen to anything connect to it with correct port number get local machine name
        self.port = PORT_NUMBER
        self.server.bind((self.host, self.port))
        self.connection = None
        self.clientAddr = None
        self.runResult = RESULT_HANG

    def startListen(self):
        """First check if the server has internet connection, if not and if its after reboot continue the loop"""
        if self.checkConnection():
            self.server.listen(5)
            while True:
                try:
                    self.connection, self.clientAddr = self.server.accept()
                    self.logger.info("connection: %s, clidneAddr: %s" %(self.connection, self.clientAddr))
                    addr = str(self.clientAddr);
                    #to get client ip used later to scp result back
                    self.clientIP = self.paresResult(addr, REGEX_IP)
                    self.logger.info('Connected with %s', self.clientIP)
                    self.connection.send('Connected\n')
                    self.communicate()
                    break
                except :
                    self.logger.info("Server socket disconnected")
                    break

    def communicate(self):
        """This is used for main communication with DevSys"""
        self.logger.info("server communication created")
        #wait for client response
        while True:
            msgRecv = self.connection.recv(PACKET_SIZE)
            self.logger.info('Server Received %s', msgRecv)
            #Read the cmd locally from config file
#            if msgRecv == 'SEND_TEST_CMD\n':
#                subMsg = ''
#                while not subMsg:
#                    subMsg = self.connection.recv(PACKET_SIZE)
#                    self.logger.info('test cmd: %s', subMsg)
#                self.connection.send('TEST_CMD_RECEIVED\n')

            if msgRecv == 'RUN_SCRIPT':
                #launch the pre-test script
                self.logger.info('launching pre-test script...')
                #check script status...if sucess send pre-test script done
                ret = self.controller.runScript()
                if ret != 0:
                    #else send pre-test error and terminate
                    self.connection.send('SCRIPT_ERROR\n')
                    self.closeSocket()
                else:
                    self.connection.send('SCRIPT_DONE\n')
            if msgRecv == 'RUN_TEST\n':
                #run tserverlite
                #return the test status
                #NEED TO GET TEST RESULT
                self.logger.info('received run test..and get result')
                self.connection.send('STARTED_RUNNING_TEST\n')
#                #HERE NEED TO WORK ON GET THE RESULT AND SEND IT BACK
                self.runResult = self.controller.runTest()
            if msgRecv == 'REBOOT\n':
                #going to reboot
                self.logger.info('going to reboot')
                self.closeSocket()
                self.logger.info('rebooting after close socket')
#ADD reboot command here
                break
            if msgRecv == 'TERMINATE\n':
                #found the rev and stop regression
                self.logger.info('result found and terminating regression')
                self.closeSocket()
                break
            if msgRecv == 'RESULT_CHECK\n':
                #return already parsed result
                self.logger.info('sending result back')
                result = RESULT_SEND_MAP[self.controller.getResult()]
                self.connection.send(result)
                #self.sendTestResult(RESULT_SEND_MAP[self.runResult])


    def sendTestResult(self,msg):
        #self.connection.send('TEST_RESULT\n')
        self.connection.send(msg)

    def checkConnection(self):
        """this method check if internet connect is present on server """
        """waits for 30 sec before continues"""
        try:
            host = socket.gethostbyname("www.google.ca")
            s = socket.create_connection((host,80),2)
            self.logger.info("Server has connectivity")
            return True
        except:
            self.logger.info("Server Lost Internet Connection")
#            pass
        return False

    def closeSocket(self):
        #try:
        #    self.connection.shutdown(socket.SHUT_WR)
        #    self.logger.info("Socket closed")
        #except:
        #    self.logger.error("Error closing socket")
        elf.connection.close()
        self.logger.info("connection closed")


    def paresResult(self, data, regex):
        ''' This method is used to parse any string using regex '''
        ret = None
        findResult = re.match(regex, data)
        if findResult:
            self.logger.info("parsing result: %s" %findResult.group(1))
            ret = findResult.group(1)
        else:
            ret = 'Parsing Error'

        return ret


