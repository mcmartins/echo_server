# Echo Server

[![Build Status](https://travis-ci.org/mcmartins/echo_server.svg)](https://travis-ci.org/mcmartins/echo_server)
[![Code Climate](https://codeclimate.com/github/mcmartins/echo_server/badges/gpa.svg)](https://codeclimate.com/github/mcmartins/echo_server)
[![Issue Count](https://codeclimate.com/github/mcmartins/echo_server/badges/issue_count.svg)](https://codeclimate.com/github/mcmartins/echo_server)

## Description

The following project implements a TCP socket server that replies to a client 
everytime it gets a '\n' (configurable, defaults to '\n'), with the sequence of messages received until then.<br/>
The server implements a connection timeout handler, so that connections idle 
more than this threshold get disconnected and cleaned from the system (configurable, defaults to 20s). 
This means that if a connected socket is not emiting for more than the threshold defined, 
the connection will be closed in order to flush resources.

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

"-v", "--verbose" - Set the loog level to 'DEBUG'.<br/>
"-p", "--port" - Set server port. Defaults to 10000<br/>
"-t", "--timeout" - Set server socket timeout. Defaults to 0s<br/>
"-x", "--max-connections" - Set server maximum connections. Defaults to 5<br/>
"-m", "--max-connection-timeout" - Set server maximum time for an active connection. Defaults to 20s<br/>
"-b", "--buffer" - Set server buffer length. Defaults to 1024<br/>
"-c", "--trigger" - Set server response trigger. Defaults to '\n'<br/>

```bash
telnet 127.0.0.1 10000
```
