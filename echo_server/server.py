import logging
import select
import socket
import sys
from repr import repr


class SocketServer(object):
    def __init__(self, port=10000, max_connections=5, timeout=10, trigger='\n', buffer=1024):
        super(SocketServer, self).__init__()
        self.timeout = timeout
        self.max_connections = max_connections
        self.trigger = trigger
        self.buffer = buffer
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server_address = ('localhost', port)
        self.inputs = [self.server]
        self.outputs = []
        self.messages = {}
        self.finished = False

    def start(self):
        self.server.bind(self.server_address)
        self.server.listen(self.max_connections)
        logging.info('Server started on: [%s]', self.server_address)
        while not self.finished:
            # wait for at least one of the sockets to be ready for processing
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, self.timeout)
            for skt in readable:
                self.__handle_new_message(skt)
            for skt in writable:
                self.__handle_replies(skt)
            for skt in exceptional:
                self.__handle_error(skt)

    def __handle_error(self, skt):
        logging.debug('Closing socket [%s] on error.', skt.getpeername())
        self.__handle_close(skt)

    def __handle_close(self, skt):
        logging.debug('Cleaning socket [%s].', skt.getpeername())
        self.__gracefully_close(skt)
        if skt in self.inputs:
            self.inputs.remove(skt)
        if skt in self.outputs:
            self.outputs[skt] = []
        if skt in self.messages:
            self.messages[skt] = []

    def __handle_new_connection(self, skt):
        connection, client_address = skt.accept()
        logging.debug('New socket connection: [%s:%s]' % (client_address, connection.getpeername()))
        connection.setblocking(False)
        self.inputs.append(connection)
        self.messages[connection] = []

    def __handle_replies(self, skt):
        if skt in self.messages:
            msg = ''.join(self.messages[skt])
            if self.trigger in msg:
                logging.debug('Replying back to [%s] with message [%s].' % (skt.getpeername(), repr(msg)))
                skt.send(msg)
                self.messages[skt] = []
                if skt in self.outputs:
                    self.outputs.remove(skt)

    def __handle_new_message(self, skt):
        if skt is self.server:
            self.__handle_new_connection(skt)
        try:
            msg = skt.recv(self.buffer)
        except socket.timeout:
            logging.debug('Socket connection timeout: [%s]. Cleaning...', skt.getpeername())
            self.__handle_close(skt)
        except socket.error:
            msg = None
        if msg:
            logging.debug('Received message [%s] from socket [%s].' % (repr(msg), skt.getpeername()))
            if skt in self.messages:
                self.messages[skt].append(msg)
                if skt not in self.outputs:
                    self.outputs.append(skt)

    def __gracefully_close(self, skt):
        try:
            skt.close()
        except socket.error:
            pass
        self.__handle_close(skt)

    def stop(self):
        self.finished = True
        for skt in self.inputs:
            try:
                skt.close()
            except socket.error:
                pass

    def get_stats(self):
        pass
