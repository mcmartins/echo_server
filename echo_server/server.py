import logging
import select
import socket
from repr import repr

import date_util


class SocketServer(object):
    def __init__(self, port=10000, max_connections=5, max_connection_timeout=20, timeout=0, trigger='\n', bfr=1024):
        super(SocketServer, self).__init__()
        self.timeout = timeout
        self.max_connections = max_connections
        self.max_connection_timeout = max_connection_timeout
        self.trigger = trigger
        self.buffer = bfr
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server_address = ('localhost', port)
        self.store = {}
        self.inputs = [self.server]
        self.outputs = []
        self.finished = False

    def start(self):
        self.server.bind(self.server_address)
        self.server.listen(self.max_connections)
        logging.info('Server started on: [%s].', self.server_address)
        while not self.finished:
            # wait for at least one of the sockets to be ready for processing
            to_read_list, to_write_list, on_error_list = select.select(self.inputs, self.outputs, self.inputs,
                                                                       self.timeout)
            for skt in to_read_list:
                self.__handle_new_message(skt)
            for skt in to_write_list:
                self.__handle_replies(skt)
            for skt in on_error_list:
                self.__handle_error(skt)
            # handle timeout connections
            self.__handle_timeout()

    def __handle_new_connection(self, skt):
        connection, client_address = skt.accept()
        logging.debug('New socket connection: [%s:%s]' % (client_address, connection.getpeername()))
        connection.setblocking(False)
        self.store[connection] = {
            'last_access': date_util.get_now(),
            'messages': []
        }
        self.inputs.append(connection)

    def __handle_replies(self, skt):
        if skt in self.store:
            msg = ''.join(self.store[skt]['messages'])
            if self.trigger in msg:
                logging.debug('Replying back to [%s] with message [%s].' % (skt.getpeername(), repr(msg)))
                skt.send(msg)
                self.store[skt]['last_access'] = date_util.get_now()
                self.store[skt]['messages'] = []
                if skt in self.outputs:
                    self.outputs.remove(skt)

    def __handle_new_message(self, skt):
        if skt is self.server:
            self.__handle_new_connection(skt)
        try:
            msg = skt.recv(int(self.buffer))
        except socket.error:
            msg = None
        if msg:
            logging.debug('Received message [%s] from socket [%s].' % (repr(msg), skt.getpeername()))
            if skt in self.store:
                self.store[skt]['messages'].append(msg)
                self.store[skt]['last_access'] = date_util.get_now()
                if skt not in self.outputs:
                    self.outputs.append(skt)

    def __handle_timeout(self):
        delete_keys = []
        for key, value in self.store.iteritems():
            if date_util.difference_in_seconds(value['last_access'],
                                               date_util.get_now()) >= self.max_connection_timeout:
                delete_keys.append(key)
        for key in delete_keys:
            try:
                key.send('Timeout...Bye Bye.')
                key.close()
            except socket.error:
                pass
            self.inputs.remove(key)
            del self.store[key]

    def __handle_error(self, skt):
        logging.debug('Closing socket [%s] on error.', skt.getpeername())
        self.__handle_close(skt)

    def __handle_close(self, skt):
        self.__gracefully_close(skt)
        if skt in self.inputs:
            self.inputs.remove(skt)
        if skt in self.outputs:
            del self.outputs[skt]
        if skt in self.store:
            del self.store[skt]

    @staticmethod
    def __gracefully_close(skt):
        try:
            skt.close()
        except socket.error:
            pass

    def stop(self):
        logging.info('Server stopped on: [%s].', self.server_address)
        self.finished = True
        for skt in self.inputs:
            self.__handle_close(skt)

    def get_stats(self):
        pass
