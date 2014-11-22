from twisted.internet import reactor
import traceback

def hello():
  print "Hello, World!"
  traceback.print_stack()
  reactor.stop()

reactor.callLater(1, hello)

print "Starting reactor"
reactor.run()
print "Done"
