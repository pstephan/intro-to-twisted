from twisted.internet import reactor

def blockingMethod(secs):
    import time
    time.sleep(secs)
    print "%d blocking seconds elapsed" % secs

def nonBlockingMethod(cnt):
    cnt -= 1
    print "1 non-blocking second elapsed"
    if cnt == 0:
        reactor.stop()
    reactor.callLater(1, nonBlockingMethod, cnt)

reactor.callInThread(blockingMethod, 2)
reactor.callLater(1, nonBlockingMethod, 3)
reactor.run()
