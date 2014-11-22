from twisted.internet import defer, reactor, threads

file = 'file.inline'

def read_file():
    data = ''
    f = open(file, 'r')
    for line in f:
        data += line
    f.close()
    return data

def print_data(data):
    print data

@defer.inlineCallbacks
def print_file():
    try:
        # deferToThread returns a deferred
        data = yield threads.deferToThread(read_file)

        yield print_data(data)
        print "Success"
    except Exception as err:
        print "Error: %s" % err
    finally:
        print "Shutting down"
        reactor.stop()

print_file()
reactor.run()

