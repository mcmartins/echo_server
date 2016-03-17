import multiprocessing as mp
import unittest
import socket
import sys
import time
from random import randint

from echo_server.server import SocketServer

messages = ['This is the message.\nThis contains carriage return.', 'It will be sent ', 'in parts.', '\n']
server_address = ('localhost', 10000)


def worker():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    s.settimeout(15)
    name = s.getsockname()
    for message in messages:
        print >> sys.stderr, '%s: sending "%s"' % (name, message)
        s.send(message)
        time.sleep(randint(0,3))
    while True:
        try:
            data = s.recv(512)
        except socket.error:
            break
        if data:
            print >> sys.stderr, '%s: received "%s"' % (name, data)
    print >> sys.stderr, name, ': closing socket'
    s.close()


class TestMultiConnectionsEchoServer(unittest.TestCase):
    
    def test_(self):
        server = SocketServer()
        server.start()
        
        workers = [mp.Process(target=worker) for i in range(0, 5)]
    
        # start multiple connections
        for p in workers:
            p.daemon = True
            p.start()
        
        # wait for all to finish
        for p in workers:
            p.join()
            
        # stop the server
        server.stop()


if __name__ == '__main__':
    unittest.main()
