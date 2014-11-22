from twisted.enterprise import adbapi

def getPassword(user):
    return dbpool.runQuery("SELECT name, password FROM users WHERE name = ?", (user,))

def printResult(data):
    if data:
        print "User: %s, Password: %s" % (data[0][0], data[0][1])
    else:
        print "No such user"

def errorResult(err):
    print "We got an error:"
    print err

def cleanup(result):
    dbpool.close()
    from twisted.internet import reactor
    reactor.stop()


dbfile = 'db.sqlite3'
dbpool = adbapi.ConnectionPool('sqlite3', dbfile, check_same_thread=False)

d = getPassword("pstephan")
d.addCallbacks(printResult, errorResult)
d.addBoth(cleanup)

from twisted.internet import reactor
reactor.run()

