import socket
import time
import unittest
from random import randint
from repr import repr

from echo_server.server import SocketServer

messages = ['This is the message\nThis contains carriage return', 'It will be sent', '\rin parts.', '\n']
server_address = ('localhost', 10000)


def setup_server():
    server = SocketServer()
    server.start()
    server.stop()


def setup_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)
    client.settimeout(10)
    name = client.getsockname()
    for message in messages:
        print 'Socket [%s] sending message [%s].' % (repr(name), repr(message))
        client.send(message)
        time.sleep(randint(0, 2))
    received = []
    while True:
        try:
            data = client.recv(1024)
        except socket.error:
            break
        if data:
            received.append(data)
            print 'Socket [%s] received a message [%s].' % (repr(name), repr(data))
    print 'Socket [%s] all data received [%s].' % (repr(name), repr(received))
    assert ''.join(received) == ''.join(messages)
    print 'Closing socket [%s].' % repr(name)
    client.close()


class BaseEchoServerTest(unittest.TestCase):
    def test_(self):
        raise NotImplementedError('Must implement this method!')
