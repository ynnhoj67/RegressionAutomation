import time, shutil, glob, os, subprocess, re


#Regression status
REGRESSION_STATUS_PASS = 1
REGRESSION_STATUS_FAIL = 2
REGRESSION_STATUS_SKIP = 3
REGRESSION_STATUS_CRASH = 4
REGRESSION_STATUS_HANG = 5
REGRESSION_STATUS_UNKNOWN = 6
REGRESSION_STATUS_SCRIPT_ERROR = 7
REGRESSION_STATUS_TERMINATE = 8
REGRESSION_STATUS_BUILD_OK = 9
REGRESSION_STATUS_CMAKE_OK = 10
REGRESSION_STATUS_BUILD_ERROR = 11
REGRESSION_STATUS_CMAKE_ERROR = 12

REGRESSION_CONTINUE = 20
REGRESSION_START_NEW = 21

#logging debug mode
RUNNING_DEBUG_MODE = True

#temp config file name
TEMP_CONFIG_FILE = 'TempConfig'

#timer
SERVER_LAUNCH_SCRIPT_DELAY = 25 #est 120 sec
SOCKET_ATTEMP_TIMER = 3 #sec this is used for server to start socket
#local debug logger file
LOGGER_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

#result file dir
BENCHMARK_SUIT_DIR = os.path.abspath(os.path.dirname(__file__))
RESULT_FILE_DIR = BENCHMARK_SUIT_DIR + "/Results/"
TEST_DIR = BENCHMARK_SUIT_DIR + "/workloadList.txt"
IDLE_DIR = BENCHMARK_SUIT_DIR + "/idleList.txt"

SHELLSCRIPT_DIR = "/Users/atiqa/Desktop/ShellScripts/"

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

def getTime():
    """ Return current time in the format of
        YYYY-MM-DDTimeHH-MM-SS
        """
    tm = time.strftime('%Y-%m-%dTime%H-%M-%S')
    print(tm)
    return tm

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

def sleep(sec):
    """ Input: sec is the seconds for sleeping"""
    time.sleep(sec)

def selectApp(name):
    """ Select the running app by it's process name
        Input: name is the process name
        """
    target.dock().dockItems()[name].performAXAction_("AXPress")
    return target.processes()[name].frontWindow()

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

def checkPid(name):
    """Check if pid exist.
        Input: name is the process name
        Return True if exists.
        """
    proc = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = proc.communicate()
    for line in out.splitlines():
        if name in line:
            pid = int(line.split(None, 1)[0])
            try:
                os.kill(pid, 0)
            except OSError:
                return False
            else:
                return True

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

def disableScreenSaver():
    """ Disable screensaver """
    os.system("defaults -currentHost write com.apple.screensaver idleTime 0")

def copyFile(src, dst):
    """Copy file from src to dst
        src: source dir
        dst: destination dir
        """
    try:
        shutil.copy(src, dst)
        os.rename(dst + "/" + src, dst + "/exeList.txt")
    except IOError, e:
        print "Copy file error"

def zipFromShell(dir):
    """ Zip folder
        Input: dir is the folder dir for zipping
        """
    currentDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(RESULT_FILE_DIR)
    os.system("zip -r %s.zip %s" %(dir,dir))
    os.chdir(currentDir)

def writeToFile(name ,data, dirPath, mode):
    """ Write data to a file
        Input: data is the content to write to the file
        Input: dirPath is the sweep folder where the output name file will be saved
        """
    #remove the file if it exists
    #if os.path.exists(os.path.join(dirPath, name)):
    #    print "temp config exists"
    #    os.remove(os.path.abspath(os.path.join(dirPath, name)))
    #else:
    #    print "temp config doesn't exist"
    writeFile = os.path.abspath(os.path.join(dirPath, name)) #dirPath + '/' + name
    file = open (writeFile, mode)
    file.write(data)
    file.close()
    #    return 0
    #else:
    #    return 1

def removeFile(name):
    """Remove the file
       Input: name full dir to the file
       """
    ret = 1
    if os.path.exists(name):
        try:
           os.remove(name)
           ret = 0
        except OSError:
           print "Remove file error"
           ret = 1
    else:
        ret = 0
    return ret

def pushToServer(timeStampName):
    """ Push result to server
        Input: timeStampName is the name of the result folder, otherwise it will zip the entire directory
        """
    dir = RESULT_FILE_DIR  + timeStampName
    zipFromShell(timeStampName)
    cmd = SHELLSCRIPT_DIR + "pushToServer.command" + " " + dir + '.zip' + " " + "-power"
    os.system(cmd)
