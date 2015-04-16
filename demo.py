import mcrcon

rcon = mcrcon.MCRcon('host', 25575, 'pass')

try:
    while True:
        command = input('> ')
        response = rcon.send(command)
        print(response)
except KeyboardInterrupt as e:
    r.close()
