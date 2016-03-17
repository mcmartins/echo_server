import signal
import sys


def signal_handler(signal, frame):
    sys.exit(1)


def initialize():
    signal.signal(signal.SIGINT, signal_handler)
