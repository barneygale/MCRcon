import mcrcon


# python 2 compatibility
try: input = raw_input
except NameError: pass


def main(host, port, password, tlsmode):
    rcon = mcrcon.MCRcon()

    print("# connecting to %s:%i..." % (host, port))
    rcon.connect(host, port, password, tlsmode)

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
    if len(args) != 4:
        print("usage: python demo.py <host> <port> <password> <tlsmode>")
        sys.exit(1)
    host, port, password, tlsmode = args
    port = int(port)
    tlsmode = int(tlsmode)
    main(host, port, password, tlsmode)
