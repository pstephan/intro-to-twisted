from twisted.python import log
from twisted.python import logfile
from twisted.internet import reactor

import sys, warnings

f = logfile.LogFile("twisted.log", ".", rotateLength=200)

def write_something(i):
    print "stdout %s" % i
    log.msg("log.msg %s" % i)
    warnings.warn("warn %s" % i)

    try:
        x = 1/0
    except:
        log.err()

def startlog():
    #log.startLogging(sys.stdout)
    log.startLogging(f)
    #log.startLogging(f, setStdout=False)

def end():
    f.rotate()
    log.msg("End of log")
    reactor.stop()

write_something(1)

reactor.callLater(0.1, startlog)
reactor.callLater(0.2, write_something, 3)
reactor.callLater(0.3, end)

reactor.run()

