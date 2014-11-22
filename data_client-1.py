# Run it like this:
# 
#   python data_client-1.py port1 port2 port3 ...
# 
# Make sure that there are servers listening on those ports.

import optparse

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

    def __init__(self, data_count):
        self.data_count = data_count
        self.data_collected = []

    def data_finished(self, data=None):
        if data is not None:
            self.data_collected.append(data)

        self.data_count -= 1

        if self.data_count == 0:
            self.report()
            from twisted.internet import reactor
            reactor.stop()

    def report(self):
        for data in self.data_collected:
            print data

    def clientConnectionFailed(self, connector, reason):
        print 'Failed to connect to:', connector.getDestination()
        self.data_finished()


def main():
    addresses = parse_args()

    factory = SimpleDataClientFactory(len(addresses))

    from twisted.internet import reactor

    for address in addresses:
        host, port = address
        reactor.connectTCP(host, port, factory)

    reactor.run()


if __name__ == '__main__':
    main()
