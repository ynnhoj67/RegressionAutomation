import time, shutil, glob, os, subprocess, re
#from UIAutomation import *

RESULT_PASS = {'PASS\n':1}
RESULT_FAIL = {'FAIL\n':2}
RESULT_SKIP = {'SKIP\n':3}
RESULT_CRASH = {'CRASH\n':4}
RESULT_HANG = {'HANG\n':5}
RESULT_UNKNOWN = {'UNKNOWN\n':6}

RESULT_SEND_MAP = {1:'PASS\n', 2:'FAIL\n',3:'SKIP\n',4:'CRASH\n',5:'HANG\n',6:'UNKNOW\n'}

RUNNING_DEBUG_MODE = True
BENCHMARK_SUIT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

LOGGER_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
#os.path.abspath(os.path.dirname(__file__))
RESULT_FILE_DIR = BENCHMARK_SUIT_DIR + "/Results/"
TEST_DIR = BENCHMARK_SUIT_DIR + "/exeList.txt"
EXELIST_NAME = "exeList.txt"
REGISTER_FILE = BENCHMARK_SUIT_DIR + "/REG.txt"

QUITUNEXPECTED_ASCPT = BENCHMARK_SUIT_DIR + "/AppleScripts/quitUnexpected.scpt"
VERTEX_DIR = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf"
VERTEX_DELAY_TIME = 650 #is calculated from plimit running time.


SHELLSCRIPT_DIR = "/Users/atiqa/Desktop/ShellScripts/"

j80Baffin = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -t3 -c -b -A -p triStrip -M displayLists -w 2000 -h 2000 -d 300 -z -75"
j134BaffinLEA = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -c -m -b -A -p quads -M drawArraysWithDynVertBufferObjectsVAO -w 500 -h 500 -d 2 -z -2"
j134BaffinPROA = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -c -m -b -fbo  -p quadStrip -M drawArraysWithVertArrayRng -w 500 -h 500 -d 4 -z 16"
j134BaffinXLA ="/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -l0 -l1 -l2 -l3 -l4 -l5 -l6 -c -m -b -A -p quads -M drawArraysWithStaticVBO -w 2000 -h 800 -d 8 -z -2"
j135BaffinXPA = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -t3 -c -m -b -A -p triangles -M drawArraysWithStaticVBO -w 800 -h 2000 -d 8 -z -75"
j135EllesmereLEA = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -t3 -c -m -b -A -fbo -depth -p triangles -M drawArraysWithStatVertBufferObjectsVAO -w 3000 -h 800 -d 2 -z 16"
j135EllesmerePROA = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -t3 -c -m -b -A -fbo  -p triStrip -M drawArraysWithVertArrayRng -w 800 -h 2000 -d 4 -z -12"
j135EllesmereXTA = "/Volumes/Data/Benchmarks/VertexPerf/vertexperf -r " + str(VERTEX_DELAY_TIME) + "-t0 -t1 -t2 -t3 -t4 -t5 -c -m -b -A -p quadStrip -M drawArraysWithVertArrayRng -w 2000 -h 800 -d 2 -z 50"

ASIC_TYPE = {'J80G_BAFFIN_ULA': j80Baffin, 'J80G_BAFFIN_LEA' : j80Baffin, 'J80G_BAFFIN_PROA' : j80Baffin , 'J134_BAFFIN_XLA' : j134BaffinXLA , 'J134_BAFFIN_PROA' : j134BaffinPROA, 'J134_BAFFIN_LEA': j134BaffinLEA , 'J135_ELLESMERE_XTA' : j135EllesmereXTA, 'J135_ELLESMERE_PROA' : j135EllesmerePROA , 'J135_ELLESMERE_LEA' : j135EllesmereLEA , 'J135_BAFFIN_XPA' : j135BaffinXPA}

#PLIMIT_SCRIPT_DIR = BENCHMARK_SUIT_DIR + "/ShellScripts/gpu_plimit.sh"
PLIMIT_SCRIPT_DIR = SHELLSCRIPT_DIR + "gpu_plimit.sh"

#passing value to applescript needs a string, so some timer is string instead of integer
VIDEO_AD_DELAY = 140
VIDEO_PLAYTIME = 180
VIDEO_BUFFER_TIME = 30
YOUTUBE_DELAY_TIMER = '120'
NETFLIX_DELAY_TIMER = '60'
IPHOTO_DELAY_TIME = '5'
IPHOTO_PLAYTIME = 130
QTIME_DELAY_TIME = '13'
ITUNES_DELAY_TIME = '50'
WIRELESSWEB_DELAY_TIME = '15'

IDLE_SETTLE_TIME = 120
IDLE_MEASURE_TIME = 120

def mouseClick():
    """Left click mouse."""
    mouse.click()

def mouseMoveTo(point):
    """Move mouse to a point location.
        Input:point is the argument in (x,y) format
        """
    mouse.moveTo_(point)

def moveToClick(location, delay):
    """A combination of move mouse to a location then click,
        Input:location is the argument in (x,y) format
        Input: delay is a delay value in sec
        """
    mouseMoveTo(location)
    sleep(delay)
    mouseClick()
    sleep(delay)

def keyboardPress(key):
    """ Press a key
        Input: key is the key value for a key
        """
    keyboard.pressKey_(key)

def keyboardRelease(key):
    """ Release a key pressed
        Input: key is hte key value for its to be released
        """
    keyboard.releaseKey_(key)

def keystroke(key):
    """ A combination of key press and then release to mimic typing on keyboard.
        Input: key is the key to stroke
        """
    keyboardPress(key)
    keyboardRelease(key)

def inputString(cmd):
    """ Typing a string.
        Input: cmd is the string
        """
    keyboard.typeString_(cmd)
    sleep(1)

def getRunningApps():
    """ Return the running app array """
    return target.dock().dockItems().withPredicate_("isRunning=1")._.name

def selectApp(name):
    """ Select the running app by it's process name
        Input: name is the process name
        """
    target.dock().dockItems()[name].performAXAction_("AXPress")
    return target.processes()[name].frontWindow()

def getWindowTopLeftX(name):
    """ Input: name is the process name
        Return x value of a process's window's top left corner
        """
    return target.processes()[name].frontWindow().bounds().origin.x

def getWindowTopLeftY(name):
    """ Input: name is the process name
        Return y value of a process's window's top left corner
        """
    return target.processes()[name].frontWindow().bounds().origin.y

def getFrontWindow(name):
    """ Input: name is the process name
        Return the front window of specified process name
        """
    selectApp(name)
    return target.processes()[name].frontWindow().click()

def resizeWindow(window, size):
    """ Resize the window.
        Input: window object from selectApp()
        Input: size NSSize value of the new window size
        """
    prositionX = window.resizeTo_(NSValue.valueWithSize_(size))

def getTime():
    """ Return current time in the format of
        YYYY-MM-DDTimeHH-MM-SS
        """
    tm = time.strftime('%Y-%m-%dTime%H-%M-%S')
    print(tm)
    return tm

def sleep(sec):
    """ Input: sec is the seconds for sleeping"""
    time.sleep(sec)

def terminateProcess(name):
    """ Terminate Process
        Input: name is the process name to be terminated
        """
    proc = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    for line in out.splitlines():
        if name in line:
            pid = int(line.split(None, 1)[0])
            os.system("kill -9 %s" %pid)

def runCommand(cmd, error_msg=None, popen_input=None, timeout=None, waitForCompletion=True, debugMessage=False, onlyReturnStatus=False, stdoutFile=None, stderrFile=None):
    """
        Run a command with subprocess.

        @cmd:               A command list.
        @error_msg:         Message on failure. default 'command failed'.
        @popen_input:       Pass to command on stdin.
        @timeout:           Default to 1/2 hr (This is not used currently).
        @waitForCompletion: Set to False to return before subprocess completion.
        @debugMessage:      Log message as debug rather than note.
        @stdoutFile:        File handle to send stdout to.
        @stderrFile:        File handle to send stderr to.
        @onlyReturnStatus:  Flag for return return status code or with output together
        """

    standardOutput = stdoutFile if stdoutFile else subprocess.PIPE
    standardError = stderrFile if stderrFile else subprocess.PIPE

    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=standardOutput, stderr=standardError)

    if not waitForCompletion:
        return process
    stdout, stderr = process.communicate(input=popen_input)

    if onlyReturnStatus:
        return process.returncode
    else:
        return (process.returncode, stdout)


def waitForEvent(eventFunction, timeout, errorMessage=None, raiseOnTimeout=True):
    """
        Wait for an event to occur.

        @eventFunction:  call this function in polling loop until it returns True.
        @timeout:        give up after timeout and raise.
        @errorMessage:   raise with this. Required unless raiseOnTimeout is False
        @raiseOntimeout: raise exception after timeout
        return time in seconds waited or 0 if event did not occur before timeout.

        """
    timeout = scaledTime(timeout)
    startTime = time()
    with patience(0):
        if eventFunction():
            logger.debug('Event found at start of waitForEvent.')
            return time() - startTime
        while not eventFunction():
            if time() - startTime > timeout:
                if raiseOnTimeout:
                    raise TestFailure(errorMessage)
                return 0
            sleep(POLL_INTERVAL)
    endTime = time()
    logger.debug("Waited for %.2fs. Maximum was %.2fs. We used %02.0f%% of this." % \
                 (endTime - startTime, timeout, (endTime - startTime) / timeout * 100))
    return endTime - startTime

def sudoCopyFile(src, dst):
    """Copy file from src to dst
        src: source dir
        dst: destination dir
        """
#    try:
#        shutil.copy(src, dst)
#    except IOError, e:
#        print "Copy file error"

    os.system("echo atiqa | sudo -S cp -r " + src + " " + dst)

def writeToFile(name ,data, dirPath):
    """ Input: name is the file name to be written into
        Input: data is the content to write to the file
        Input: dirPath is the sweep folder where the output name file will be saved
        """

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    writeFile = dirPath + '/' + name
    file = open (writeFile, 'w')
    file.write(data)
    file.close()

def appendToFile(name, data, dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    writeFile = dirPath + '/' + name
    file = open (writeFile, 'w')
    file.write(data)
    file.close()

def disableScreenSaver():
    """ Disable screensaver """
    os.system("defaults -currentHost write com.apple.screensaver idleTime 0")

def getSystemProfile(folder, isAMD):
    """ Calling CaptureSystemConfig.php located on desktop
        to obtain the PowerLog.log
        Input: folder is the result dir to save the log
        """

    backUpCurrentDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir("/Users/atiqa/Desktop/")

    if isAMD:
        ret = os.system("php CaptureSystemConfig.php 1")
    else:
        ret = os.system("php CaptureSystemConfig.php 0")
    if (ret != 0):
        #terminate when system config script failed
        exit(1)

    #copy generated file to result folder
    try:
        shutil.copy("/Users/atiqa/Desktop/PowerLog.log",folder)
        shutil.copy("/Users/atiqa/Desktop/SystemReport.spx",folder)
    #print("copied setting files")
    except IOError, e:
        print "Unable to copy system file "
        os.chdir(backUpCurrentDir)

    #checks for Benchmarks HDD
    if not os.path.exists("/Volumes/Data/Benchmarks/"):
        print "Missing Benchmarks HDD can not continue."
        exit(1)

def tempCheck():
    """ Check for tempeature """
    dir = '/Users/atiqa/Desktop/tools/ypc2'
    if not os.path.exists(dir):
        print "Missing ypc2 tool, please copy it to BenchmarksAutomation directory"
        exit(1)
    else:
        os.system(SHELLSCRIPT_DIR + '/checktemperature.sh' + ' ' + dir)


def removeLogFile(filename, srcdir):
    """Remove log file from srdir with specified file
       Input: filename is the format of log file
       Input: srcdir is the dir for log file
       """
    #check the existance of file
    fileName = filter(os.path.isfile, glob.glob(srcdir + filename))
    if len(fileName) > 0:
        os.remove(fileName[0])

def regXpParse(data, regex):
    """Use Regex to parse data
    Input: data the string need to be parsed
    Input: regex the pattern to parse
    Output: return the matching string
    """
    ret = None
    findResult = re.match(regex, data)
    if findResult:
        print("parsing result: %s" %findResult.group(1))
        ret = findResult.group(1)
    else:
        ret = 'NotFound'

    return ret
