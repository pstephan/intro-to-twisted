from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.wire import QOTD
import twisted.manhole.telnet

f = Factory()
f.protocol = QOTD
reactor.listenTCP(3000, f)

# Add a manhole shell
m = twisted.manhole.telnet.ShellFactory()
m.username = "pstephan"
m.password = "password"
m.namespace['data'] = 12
m.namespace['qotd'] = f
reactor.listenTCP(3001, m)

reactor.run()
