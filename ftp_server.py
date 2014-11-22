from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.cred.portal import Portal
from twisted.cred.checkers import AllowAnonymousAccess
from twisted.internet import reactor

portal = Portal(FTPRealm('./'), [AllowAnonymousAccess()])

factory = FTPFactory(portal)

reactor.listenTCP(21, factory)
reactor.run()

