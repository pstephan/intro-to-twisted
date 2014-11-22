from twisted.internet import utils, reactor

def writeResponse(resp):
    print "=== ifconfig output ==="
    print resp

def noResponse(err):
    print "Failed to get ifconfig data"

def cleanup(resp):
    reactor.stop()

d = utils.getProcessOutput("/sbin/ifconfig", ("-a",))
d.addCallbacks(writeResponse, noResponse)
d.addBoth(cleanup)
reactor.run()

