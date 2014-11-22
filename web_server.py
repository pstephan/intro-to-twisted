from twisted.internet import reactor
from twisted.web import server, static

resource = static.File('.')
factory = server.Site(resource)
reactor.listenTCP(3000, factory, interface='localhost')
reactor.run()
