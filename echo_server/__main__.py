import atexit
from optparse import OptionParser

from signal_handler import initialize as signal_interceptor
from logger import initialize as logger_initialize
from server import SocketServer

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose", default=True,
                      help="Set Log level to debug.")
    parser.add_option("-p", "--port", action="store",
                      dest="port", default=False,
                      help="Set server port.")
    parser.add_option("-t", "--timeout", action="store",
                      dest="timeout", default=False,
                      help="Set server socket timeout.")
    parser.add_option("-x", "--max-connections", action="store",
                      dest="max", default=False,
                      help="Set server maximum connections.")
    parser.add_option("-m", "--max-connection-timeout", action="store",
                      dest="conn_timeout", default=False,
                      help="Set server maximum time for an active connection.")
    parser.add_option("-b", "--buffer", action="store",
                      dest="buffer", default=False,
                      help="Set server buffer.")
    parser.add_option("-c", "--trigger", action="store",
                      dest="trigger", default=False,
                      help="Set server response trigger.")

    options, args = parser.parse_args()
    verbose = options.verbose or False
    port = options.port or 10000
    timeout = options.timeout or 0
    max_connections = options.max or 5
    max_connection_timeout = options.conn_timeout or 20
    bfr = options.buffer or 1024
    trigger = options.trigger or '\n'

    # initialize log
    logger_initialize(verbose)
    # exceptions handler
    signal_interceptor()
    # initialize socket server, with default values
    server = SocketServer(port=port, max_connections=max_connections, max_connection_timeout=max_connection_timeout,
                          timeout=timeout, bfr=bfr, trigger=trigger)
    # ensure nothing stays running if the tool blows for some reason
    atexit.register(server.stop)
    # start server, blocks
    server.start()
