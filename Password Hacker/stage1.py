import argparse
import socket

def connect(args):
    with socket.socket() as sock:
        sock.connect((args.hostname, args.port))
        sock.send(' '.join(args.msg).encode())
        response = sock.recv(1024).decode("utf-8")
        print(response)

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('port', type=int)
parser.add_argument('msg', nargs=argparse.REMAINDER)
connect(parser.parse_args())