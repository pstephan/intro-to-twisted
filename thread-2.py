from twisted.internet import reactor, threads

def blockingMethod(secs):
    import time
    time.sleep(secs)
    return secs

def blockingResponse(result):
    print "%s blocking seconds elapsed" % result

def nonBlockingMethod(cnt):
    cnt -= 1
    print "1 non-blocking second elapsed"
    if cnt == 0:
        reactor.stop()
    reactor.callLater(1, nonBlockingMethod, cnt)

d = threads.deferToThread(blockingMethod, 2)
d.addCallback(blockingResponse)
reactor.callLater(1, nonBlockingMethod, 3)
reactor.run()
