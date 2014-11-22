# Run it like this:
# 
#   python data_client-2.py port1 port2 port3 ...
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

    def __init__(self, callback, errback):
        self.callback = callback
        self.errback = errback

    def data_finished(self, data):
        self.callback(data)

    def clientConnectionFailed(self, connector, reason):
        self.errback(reason)


def get_data(host, port, callback, errback):
    """
    Download data from the given host and port and invoke

      callback(data)

    when the data is complete. If there is a failure, invoke:

      errback(err)

    instead, where err is a twisted.python.failure.Failure instance.
    """

    from twisted.internet import reactor
    factory = SimpleDataClientFactory(callback, errback)
    reactor.connectTCP(host, port, factory)


def main():
    addresses = parse_args()

    from twisted.internet import reactor

    data_collected = []
    errors = []

    def got_data(data):
        data_collected.append(data)
        data_complete()

    def data_failed(err):
        print 'Failed to get data:', err
        errors.append(err)
        data_complete()

    def data_complete():
        if len(data_collected) + len(errors) == len(addresses):
            reactor.stop()

    for address in addresses:
        host, port = address
        get_data(host, port, got_data, data_failed)

    reactor.run()

    for data in data_collected:
        print data

    print "Done"


if __name__ == '__main__':
    main()
