import mcrcon

# python 2 compatibility
try: input = raw_input
except NameError: pass

def main(host, port, password):
    rcon = mcrcon.McRcon(host, port, password)

    print("# connecting to %s:%i..." % (host, port))

    print("# ready")

    try:
        while True:
            response = rcon.command(input('> '))
            if response:
                print("  %s" % response)

    except KeyboardInterrupt:
        print("\n# disconnecting...")
        rcon.disconnect()


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    if len(args) != 3:
        print("usage: python demo.py <host> <port> <password>")
        sys.exit(1)
    host, port, password = args
    port = int(port)
    main(host, port, password)
