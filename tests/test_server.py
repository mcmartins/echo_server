import unittest
import socket

from echo_server.server import SocketServer


class TestEchoServer(unittest.TestCase):
    def test_(self):
        server_address = ('localhost', 10000)
        server = SocketServer()
        server.start()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(server_address)
        client.settimeout(5)
        message = 'hello!\n'
        client.send(message)
        assert message == client.recv(512)
        server.stop()


if __name__ == '__main__':
    unittest.main()
