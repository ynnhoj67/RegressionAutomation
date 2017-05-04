import os,time, Queue, sys
from ClientServer import ClientServer
from Logger import BenchmarkLogger
from Utility import *
from FuncThread import FuncThread
from ParseCmdLineArgs import *
import AutoLaunchServer
from tGraph import Tgraph
import datetime



#creating a time stamped folder for result
timeStamp = getTime()
timeStampFolder = RESULT_FILE_DIR + timeStamp
if not os.path.exists(timeStampFolder):
    os.makedirs(timeStampFolder)

#create logger class
queue = Queue.Queue()
logger = BenchmarkLogger(timeStampFolder)
ip = "10.60.224.4"
monitor = "Internal"
loop = 3
type = "workload"

##create tgraph class
#tgraph = Tgraph(logger, 'tGraph', timeStampFolder)
#tgraph.setAppName('WorkLoad_PowerAuto')
#tgraph.setWaitTimer(1)

##tg = Tgraph(logger, 'tGraph', timeStampFolder)
##tg.setAppName('Youtube')
##tg.setWaitTimer(10)
##
##print "appName: %s, waitTimer: %d, dir: %s" %(tg.getAppName(), tg.getWaitTimer(), tg.getTgraphDir())
##
##tg.startApp()
##
##tg.closeApp()
#
#threadTg = FuncThread(logger, queue, None, None, 10)
#threadTg.setTarget(threadTg.startTimer)
#threadTg.start()
#
#while queue.empty():
#    time.sleep(1)
#
#while not queue.empty():
#    val = queue.get()
#    print "rec queue: %s" %val

##Testing socket connection
#client = ClientServer(ip, monitor, logger, list, type, loop, queue, tgraph)
#
#print "waiting for reconnect "
#sleep(30)
#loop -=1
##client.setReconnect(True)
##client.connect()
#client = ClientServer(ip, monitor, logger, list, type, loop, queue, tgraph)
#print "waiting for reconnect "
#loop -=1
#sleep(30)
#client = ClientServer(ip, monitor, logger, list, type, loop, queue, tgraph)


##est time
#runListDir = BENCHMARK_SUIT_DIR + "/workloadList.txt"
#runList = []
#gt = 0
#def getTestsList():
#    """Reads List.txt to look for apps to execute
#        """
#    time = 0
#    if os.path.exists(runListDir):
#        with open(runListDir, "r") as tests:
#            for line in tests:
#                if line[0] == '#':
#                    logger.info("App %s is skipped by user." %line)
#                else:
#                    runList.append(line.rstrip('\n'))
#                    #calaulate est time for entire run
#                    if runList[len(runList) -1] != '':
#                        time += EST_RUNTIME_PERAPP[runList[len(runList)-1]]
#                        logger.info("time: %d" %time)
#    return time
#                        
#gt = getTestsList()
#print "GT: %d" %gt
#gt = 3
#now = datetime.datetime.now()
#deltTime = datetime.datetime.now() + datetime.timedelta(seconds=gt)
#print "now %s"%now
#print "cmp %s"%deltTime
#
##if now < deltTime:
##    print "less"
##elif now > deltTime:
##    print "more"
#
#while True:
#    time.sleep(1)
#    now = datetime.datetime.now()
#    if now > deltTime:
#        print "time to stop %s" %now
#        break

#USER INPUT
#SUBMENULIST = BENCHMARK_SUIT_DIR + "/subMenuList"
#def selectSubFunction(selection):
#    print "selected: %d" %selection
#
#def dispSubMenu():
#    cnt = 0
#    os.system('clear')
#    #read the subMenuList and display it
#    if os.path.exists(SUBMENULIST):
#        with open(SUBMENULIST) as input:
#            line = input.readlines()
#
#        #show each entry
#        print "Please select following platform:\n"
#        for i in range(0 ,len(line)):
#            if line[i] != '' and line[i] != '\n':
#                print "%d. %s" %(i,line[i])
#                cnt += 1
#        print "%d. Back" %i
#
#        selection = raw_input("select:")
#        try:
#            selection = int(selection)
#            if selection > cnt:
#                dispSubMenu()
#            elif selection == cnt:
#                dispMenu()
#            else:
#                selectSubFunction(selection)
#        except ValueError:
#            print "Please enter integer"
#            dispSubMenu()
#                #calling plimit specific function
#
#    else:
#        print "Error accessing submenuList file"
#        exit(1)
#
#
#def workload():
#    print "work load selected"
#
#def idle():
#    print "idle selected"
#
#def plimit():
#    print "plimit selected"
#    dispSubMenu()
#
#def terminate():
#    print "exiting"
#    exit()
#
#def selectFunction(select):
#    switcher = { 1: workload, 2: idle, 3: plimit, 4:terminate }
#    func = switcher.get(select, lambda: "nothing")
#    return func()
#
#def dispMenu():
#    os.system('clear')
#    print "Please select the following actions:\n"
#    print "1. WorkLoad\n"
#    print "2. Idle\n"
#    print "3. Plimit\n"
#    print "4. Exit\n"
#    selection = raw_input("Enter selection number: ")
#    try:
#        selection = int(selection)
#        if (selection > 4) or (selection < 1):
#            dispMenu()
#        else:
#            selectFunction(selection)
#    
#    except ValueError:
#        print "Please enter integer"
#        dispMenu()
#
##print(chr(27) + "[2J")
#os.system('clear')
#inputVar = raw_input("PLease Make sure tGraph is synced with target system: (type yes to Continue)\n")
#if inputVar == 'yes' or inputVar == 'Yes' or inputVar == 'YES':
#
#    print ("continue")
#else:
#    print ("exiting")
#dispMenu()


##tgraph selection
#tGraph_AppleScript = BENCHMARK_SUIT_DIR + "/LaunchtGraph.scpt"
#MojoCable_DropDown = (281, 196)
#MojoCable_select = (281,230)   #select item 1 from drop down list
#
#
#def selectMojoCable():
#    moveToClick(MojoCable_DropDown, 3)
#    sleep(1)
#    moveToClick(MojoCable_select, 3)
#    sleep(10)
#
#def savetGraph(appendName):
#    #command
#    keyboardPress(55)
#    #command 1
#    keyboardPress(1)
#    keyboardRelease(1)
#    keyboardRelease(55)
#    sleep(1)
#    #append name to the name of saved graph
#    keystroke(124)
#    inputString('_'+appendName)
#    sleep(2)
#    #return
#    keystroke(36)
#    #given delay to allow it to save
#    sleep(5)
#
##open tgraph
##ret = runCommand(["osascript", tGraph_AppleScript], None, None, None, True, False, True)
##error check
##bring up tgraph to front
#selectApp('tGraph')
#sleep(1)
##selectMojoCable()
#savetGraph('ab')
#terminateProcess('tGraph')
#listName = ""
#def getIndexOfApp(listName):
#    '''thie method find the index of running app and return it'''
#    i = 0
#    listN = listName
#    print TEST_DIR
#    if os.path.exists(TEST_DIR):
#        with open(TEST_DIR, "r") as tests:
#            for line in tests:
#                print line
#                if line[0] == '#' or line == '' or line == '\n':
#                    print "ignore i: %d" %i
#                else:
#                    listN += '_' + str(i)
#                i += 1
#    print listN
#
#getIndexOfApp(listName)

#list = []
#with open('workloadList.txt', 'r') as tests:
#    for line in tests:
#        if line[0] == '#':
#            logger.info("skip %s" %line)
#        else:
#            eachLine = line.split('-')
#            id = eachLine[0].split(':')
#            category = eachLine[1]
#            name = eachLine[2].rstrip('\n')
#            logger.info("id: %s, cat: %s, name: %s" %(id[1],category,name))
#            list.append("%s:%s:%s" %(id[1],category,name))
#    print list

