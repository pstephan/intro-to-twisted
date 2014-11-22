from twisted.internet import protocol, reactor

subprocesses = {}
max_processes = 3

class MyProc(protocol.ProcessProtocol):
    def connectionMade(self):
        self.pid = self.transport.pid
        print "started process with pid %s" % self.pid

    def outReceived(self, data):
        print "Stdout: %s " % data

    def errReceived(self, data):
        print "Stderr: %s " % data

    def processExited(self, reason):
        print "processExited pid = %s, status %s" % (self.pid, reason.value.exitCode)
        del subprocesses[self.pid]
        print "Remaining subprocesses: ", subprocesses
        if len(subprocesses) == 0:
            reactor.stop()

for i in range(0, max_processes):
    pp = MyProc()
    command = ['/bin/sleep', str(max_processes - i)]
    subprocess = reactor.spawnProcess(pp, command[0], command, {})
    subprocesses[subprocess.pid] = subprocess

reactor.run()

