# Echo Server

The following project implements a TCP socket server that replies to a client 
everytime it gets a '\n', with the sequence of messages received until then.<br/>
The server implements a connection timeout handler, so that connections idle 
more than this threshold get disconnected and cleaned from the system (defaults to 20s).

## Tests

To run the tests just execute:

```bash
python tests/test_multiple_connections.py
```

## Install & Run

The steps to use the application.

### Install

```bash
sudo python setup.py build install
```

### Run

```bash
python -m echo_server [options]
```

Where the options are:

"-p", "--port" - Set server port. Defaults to 10000<br/>
"-t", "--timeout" - Set server socket timeout. Defaults to 0s<br/>
"-x", "--max-connections" - Set server maximum connections. Defaults to 5<br/>
"-m", "--max-connection-timeout" - Set server maximum time for an active connection. Defaults to 20s<br/>
"-b", "--buffer" - Set server buffer length. Defaults to 1024<br/>
"-c", "--trigger" - Set server response trigger. Defaults to '\n'<br/>

```bash
telnet 127.0.0.1 10000
```
