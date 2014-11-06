import getpass
import mcrcon

print 'Ctrl-C to exit'
host = raw_input('Host: ')
if not host: host = "pimine.local"
port = raw_input('Port (25575): ')
if not port: port = 25566
else: port = int(port)
pwd  = getpass.getpass('Password: ')
if not pwd: pwd = "mc2014"

print "Connecting..."
server = mcrcon.MCRcon(host, port, pwd)
print "Logged in successfully"

try:
    while True:
        line = raw_input('Rcon: ')
        print server.send(line)
except KeyboardInterrupt, e:
	server.close()