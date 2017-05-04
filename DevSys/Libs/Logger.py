import logging
import os, sys
from Utility import LOGGER_FILE, RUNNING_DEBUG_MODE
DEBUG_FORMAT_STRING = "[%(asctime)s] [%(name)16.16s] [%(levelname)8.8s] [%(process)7.7s] [%(module)18.18s] [%(funcName)18.18s] [%(lineno)5.5s] [%(relativeCreated)7.7d] = %(message)s"
LOG_FORMAT_STRING = "[%(asctime)s] [%(name)16.16s] [%(levelname)8.8s] = %(message)s"

if RUNNING_DEBUG_MODE:
    defaultLoggingLevels = logging.DEBUG
else:
    defaultLoggingLevels = logging.INFO


class RegressionLogger(logging.Logger):
    """ This class provides universal logging functionality
        """

    _instance = None

    def __new__(self, timeStamp):
        if not isinstance(self._instance, self):
            self._instance = super(RegressionLogger, self).__new__(self)
            self._instance.__initialized = False
        return self._instance


    def __init__(self, timeStamp):

        if self.__initialized:
            return

        super(RegressionLogger, self).__init__(self)
        self._instance.__initialized = True

        self.logFile = None
        self.defaultHandlers = []
        logFileName = timeStamp + '.log'
        debugSummaryFile = os.path.join(LOGGER_FILE, logFileName)

        self.logger = logging.getLogger(__name__)
        debugLogHandler = logging.FileHandler(debugSummaryFile)
        debugLogHandler.setLevel(logging.DEBUG)
        debugLogHandler.setFormatter(logging.Formatter(DEBUG_FORMAT_STRING))
        self.defaultHandlers.append(debugLogHandler)

        stdoutLogger = logging.StreamHandler(sys.stdout)
        stdoutLogger.setLevel(defaultLoggingLevels)
        stdoutLogger.setFormatter(logging.Formatter(LOG_FORMAT_STRING))
        self.defaultHandlers.append(stdoutLogger)

        self.resetDefaultHandlers()

    def resetDefaultHandlers(self):
        self.handlers = [ handler for handler in self.defaultHandlers]





