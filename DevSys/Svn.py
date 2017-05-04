#! /usr/bin/python
import pysvn,os,string
from Libs.Utility import *

SVN_PATH = "/home/johnny/Source/backUp/"
SVN_URL = "http://ppesvn.amd.com/diagnostics/gpu"
#backUpCurrentDir = os.path.dirname(os.path.abspath(__file__))
#os.chdir("/home/johnny/Source/trunkDbg/")

#set svn client path
#svnClient = pysvn.Client()
#svnRoot = SVN_PATH  # "http://ppesvn.amd.com/diagnostics/gpu/trunk"

#get current rev
#curRev = svnClient.info(svnRoot).get("revision").number
#print "curRev %d" %curRev

#get tott rev
#headrev = pysvn.Revision(pysvn.opt_revision_kind.head)
#revLog = svnClient.log(SVN_URL, revision_start=headrev, revision_end=headrev, discover_changed_paths=False)
#headrev = revLog[0].revision.number

#tottRev = svnClient.revpropget("revision", url=SVN_URL)[0].number
#print "headrev %d" %tottRev
class CSvn(object):
    def __init__(self, logger, svnDir, cmakeCmd, makeCmd, buildFolder, cleanBuild, topRev, botRev):
        self.logger = logger
        self.logger.info("Passing to CSvn: %s,%s,%s,%s,%s,%s,%s" %(svnDir,cmakeCmd,makeCmd,buildFolder,cleanBuild,topRev,botRev))
        self.topRevInit = topRev
        self.botRevInit = botRev
        self.buildFolder = buildFolder
        self.cleanBuild = cleanBuild
        self.cmakeCmd = cmakeCmd
        self.makeCmd = makeCmd
        self.revList = []
        self.svnClient = pysvn.Client()
        self.svnRoot = os.path.abspath(svnDir)
        self.buildDir = os.path.join(self.svnRoot, self.buildFolder)
        self.curRev = 0
        self.tottRev = 0
        self.setTottRev()
        self.setCurRev()
        self.setTopRevInit()
        self.setBotRevInit()

#        self.topRevCont = 0
#        self.botRevCont = 0
#        self.curRevCont = 0

    def getListOfRev(base, head):
        """This function gets a list of rev from svn
            @base: the base svn rev #
            @head: the head svn rev #
        """
        revList = []
        ret,stdOut = runCommand(['svn','log', '-r', `base`+':'+`head`, '-q'],None,None,None,True,False,False)
#    p = subprocess.Popen("svn log -r " + cmd + " -q", stdout=subprocess.PIPE, shell=True)
#    (stdOut, err) = p.communicate()
        if ret != 0:
            self.logger.error("Getting svn revs error")
            #NEED TO DECIDE IF EXIT HERE
        multiLines = stdOut.split('\n')

        for l in multiLines:
            eachLine = l.split(' |')
            for e in eachLine:
                if e[:1] == 'r':
                    self.revList.append(e[1:])

    def runCmake(self):
        #Go to build folder
        backUpCurDir = os.path.dirname(os.path.abspath(__file__))
        self.logger.info("cmake folder: %s" %self.buildDir)
        status = REGRESSION_STATUS_CMAKE_OK
        if os.path.exists(self.buildDir):
            self.logger.info("build dir exists")
            self.isCleanBuild()
            status = self.cmake()
        else:
            self.logger.info("build dir doesn't exist")
            os.makedirs(self.buildDir)
            self.isCleanBuild()
            status = self.cmake()
        os.chdir(backUpCurDir)
        return status

    def cmake(self):
        os.chdir(self.buildDir)
        self.logger.info("running cmake %s" %self.cmakeCmd)
        ret = runCommand(self.cmakeCmd,None,None,None,True,False,True)
        if ret != 0:
            self.logger.error("Cmake error please check cmake command")
            return REGRESSION_STATUS_CMAKE_ERROR
        else:
            return REGRESSION_STATUS_CMAKE_OK

    def runMake(self):
        backUpCurDir = os.path.dirname(os.path.abspath(__file__))
        self.logger.info("run make command %s" %self.makeCmd)
        #assumption build dir is already exists, since make is after cmake
        os.chdir(self.buildDir)
        ret = runCommand(self.makeCmd,None,None,None,True,False,True)
        if ret != 0:
            self.logger.error("Build encounter error")
            return REGRESSION_STATUS_BUILD_ERROR
        else:
            return REGRESSION_STATUS_BUILD_OK

    def isCleanBuild(self):
        if self.cleanBuild == 'TRUE' or self.cleanBuild == 'True' or self.cleanBuild == 'true':
            self.makeClean()

    def makeClean(self):
        self.logger.info("running make clean...")
        ret = runCommand(['make','clean'],None,None,None,True,False,True)
        return ret

    def setCurRev(self):
        #somehow the following cmd doesn't work in class...but when define at top works
        self.logger.info("svnroot %s" %self.svnRoot)
        self.curRev = self.svnClient.info(self.svnRoot).get("revision").number
        self.logger.info("setting curRev to %s " %self.curRev)

    def setTottRev(self):
        self.tottRev = self.svnClient.revpropget("revision", url=SVN_URL)[0].number
        self.logger.info("setting tottRev to %s " %self.tottRev)

    def getTottRev(self):
        return self.tottRev

    def setTopRevInit(self):
        if self.topRevInit == 'TOTT' or self.topRevInit == 'tott' or self.topRevInit == 'Tott':
            self.topRevInit = self.tottRev
        self.logger.info("Top rev %s" %self.topRevInit)

    def setBotRevInit(self):
        if self.botRevInit == 'CURR' or self.botRevInit == 'curr' or self.botRevInit == 'Curr':
            self.botRevInit = self.curRev
        self.logger.info("bot rev %s" %self.botRevInit)

#    def setTopRevCont(self, top):
#        self.topRevInitCont = top

#    def setBotRevCont(self, bot):
#        self.botRevCont = bot

    def getTopRevInit(self):
        return self.topRevInit

    def getBotRevInit(self):
        return self.botRevInit

    def getCurRev(self):
        return self.curRev
#    def getTopRevCont():
#        return self.tobRevCont

#    def getBotRevCont():
#        return self.botRevCont

    def getRevList(self):
        return self.revList

#list = getListOfRev(146190, 146200)
#list = getListOfRev(146190, 146536)
#for i in list:
#    print i
