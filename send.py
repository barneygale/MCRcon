from __future__ import print_function
import argparse
import socket
import mcrcon
import sys

# python 2 compatibility
try:
    input = raw_input
except NameError:
    pass



def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port", type=int)
    parser.add_argument("password")
    args = parser.parse_args()

    # Connect
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.host, args.port))

    try:
        # Log in
        result = mcrcon.login(sock, args.password)
        if not result:
            print("Incorrect rcon password")
            return

        # Send lines from stdin
        for line in sys.stdin:
            print(line)
            response = mcrcon.command(sock, line)
            print(response)
    finally:
        sock.close()

if __name__ == '__main__':
    main()
