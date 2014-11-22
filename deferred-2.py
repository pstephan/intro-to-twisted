from twisted.internet.defer import Deferred

def outer_callback_1(res):
    print 'In outer_callback_1'
    d = Deferred()
    d.addCallback(inner_callback_1)
    d.addCallback(inner_callback_2)
    d.callback(0)
    return d

def inner_callback_1(res):
    print 'In inner_callback_1'

def inner_callback_2(res):
    print 'In inner_callback_2'

def outer_callback_2(res):
    print 'In outer_callback_2'
    raise Exception("Some other error")

def outer_callback_3(res):
    print 'In outer_callback_3'

def errback_1(err):
    print 'In errback_1: %s/%s' % (err.value, err.type)
    #return err

def cleanup(res):
    print 'In cleanup, arg type is %s' % res.__class__
    from twisted.internet import reactor
    reactor.stop()

d = Deferred()

d.addCallbacks(outer_callback_1, errback_1)
d.addCallbacks(outer_callback_2, errback_1)
d.addCallbacks(outer_callback_3, errback_1)
d.addBoth(cleanup)

from twisted.internet import reactor
reactor.callWhenRunning(d.callback, 0)
reactor.run()

print "Done"
