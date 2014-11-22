from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory

class EchoProtocol(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(ServerFactory):
    protocol = EchoProtocol


listen_port = 3000
factory = EchoFactory()

port = reactor.listenTCP(listen_port, factory, interface='127.0.0.1')
print "Echo server listening on %s port %s" % (port.getHost(), port.port)
reactor.run()

