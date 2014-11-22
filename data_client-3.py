# Run it like this:
# 
#   python data_client-3.py port1 port2 port3 ...
# 
# Make sure that there are servers listening on those ports.

import optparse

from twisted.internet import defer
from twisted.internet.protocol import Protocol, ClientFactory

def parse_args():
    usage = """usage: %prog [options] [hostname]:port ..."""

    parser = optparse.OptionParser(usage)

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


class SimpleDataProtocol(Protocol):

    data = ''

    def dataReceived(self, data):
        print "Got %d bytes from %s (total %d)" % (len(data), self.transport.getHost(), len(self.data) + len(data))
        self.data += data

    def connectionLost(self, reason):
        self.dataComplete(self.data)

    def dataComplete(self, data):
        self.factory.data_finished(data)


class SimpleDataClientFactory(ClientFactory):

    # Specify what protocol to build
    protocol = SimpleDataProtocol

    def __init__(self, deferred):
        self.deferred = deferred

    def data_finished(self, data):
        if self.deferred is not None:
            d = self.deferred
            self.deferred = None
            d.callback(data)

    def clientConnectionFailed(self, connector, reason):
        if self.deferred is not None:
            d = self.deferred
            self.deferred = None
            d.errback(reason)


def get_data(host, port):
    d = defer.Deferred()

    from twisted.internet import reactor
    factory = SimpleDataClientFactory(d)
    reactor.connectTCP(host, port, factory)
    return d


def main():
    addresses = parse_args()

    from twisted.internet import reactor

    data_collected = []
    errors = []

    def got_data(data):
        data_collected.append(data)

    def data_failed(err):
        print 'Failed to get data:', err
        errors.append(err)

    def data_complete(data):
        if len(data_collected) + len(errors) == len(addresses):
            reactor.stop()

    for address in addresses:
        host, port = address
        d = get_data(host, port)
        d.addCallbacks(got_data, data_failed)
        d.addBoth(data_complete)

    reactor.run()

    for data in data_collected:
        print data

    print "Done"


if __name__ == '__main__':
    main()
