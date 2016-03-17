import atexit
import logging
from optparse import OptionParser

import logger
from server import SocketServer


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-v", "--verbose", action="store_true",
                      dest="verbose", default=False,
                      help="Set Log level to debug.")
    parser.add_option("-p", "--port", action="store",
                      dest="port", default=False,
                      help="Set server port.")
    parser.add_option("-t", "--timeout", action="store",
                      dest="timeout", default=False,
                      help="Set server socket timeout.")
    parser.add_option("-m", "--max-connections", action="store",
                      dest="max", default=False,
                      help="Set server maximum connections.")
    parser.add_option("-b", "--buffer", action="store",
                      dest="buffer", default=False,
                      help="Set server buffer.")
    parser.add_option("-c", "--trigger", action="store",
                      dest="trigger", default=False,
                      help="Set server response trigger.")

    options, args = parser.parse_args()
    verbose = options.verbose
    port = options.port
    timeout = options.timeout
    max = options.max
    buffer = options.buffer
    trigger = options.trigger
    
    # initialize log
    logger.initialize(verbose)
    # initialize socket server, with default values
    server = SocketServer(port=port, timeout=timeout, max_connections=max, buffer=buffer, trigger=trigger)
    # ensure nothing stays running if the tool blows for some reason
    atexit.register(server.stop)
    # start server
    server.start()
