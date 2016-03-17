# Echo Server

The following project implements a TCP socket server that replies to a client 
everytime it gets a '\n', with the sequence of messages received until then.

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

"-p", "--port" - Set server port. Defaults to 10000
"-t", "--timeout" - Set server socket timeout. Defaults to 10s
"-m", "--max-connections" - Set server maximum connections. Defaults to 5
"-b", "--buffer" - Set server buffer. Defaults to 1024
"-c", "--trigger" - Set server response trigger. Defaults to '\n'

```bash
python -m echo_server -v
```