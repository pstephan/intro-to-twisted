from twisted.internet.defer import Deferred

def callback_1(res):
    print 'callback_1 got', res
    raise Exception("Some error")

def callback_2(res):
    print 'callback_2 got', res
    return 2

def callback_3(res):
    print 'callback_3 got', res
    raise Exception("Some other error")

def errback_1(err):
    print 'errback_1: %s/%s' % (err.value, err.type)
    return 2

def cleanup(res):
    print 'In cleanup, arg type is %s' % res.__class__
    from twisted.internet import reactor
    reactor.stop()


d = Deferred()

d.addCallbacks(callback_1, errback_1)
d.addCallback(callback_2)
d.addCallbacks(callback_3, errback_1)
d.addBoth(cleanup)

from twisted.internet import reactor
reactor.callWhenRunning(d.callback, 0)
reactor.run()

print "Done"

