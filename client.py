#!/usr/bin/env python3

import socket
import logging
import platform
import threading
import os
import time
import subprocess
import tty
import termios
import sys

# own libraries
import utils
import logHandler

logger = logging.getLogger(__name__)
# don't change log level here! change it in logHandler.py instead
logger.setLevel(logging.DEBUG)

logger.addHandler(logHandler.stream_handler)
logger.addHandler(logHandler.file_handler)

# ------------------------------------------------------------------------------

def forwardTo(sock):
    string = ' '
    while string:
        string = str(sys.stdin.read(1))
        if string:
            sock.sendall(string.encode())

def forwardFrom(sock):
    string = ' '
    while string:
        string = sock.recv(1024)
        if string:
            print(string.decode(), end="")
            sys.stdout.flush()

def platLinux(sock):
    threading.Thread(target=forwardFrom, args=(sock,)).start()
    threading.Thread(target=forwardTo, args=(sock,)).start()
    while True:
        pass

def platLinuxOld(sock):
    import pty
    os.dup2(0, sock.fileno())
    os.dup2(1, sock.fileno())
    os.dup2(2, sock.fileno())
    os.popen()
    while True:
        pass

def platWindows(conn):
    pass

def startOfProgram():
    try:
        file_desc = sys.stdin.fileno()
        old_setting = termios.tcgetattr(file_desc)

        tty.setraw(sys.stdin)

        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("127.0.0.1",4445))

        if platform.system() == "Windows":
            platWindows(s)
        else:
            platLinux(s)
    finally:
        termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)
        s.close()

def main():
    startOfProgram()

if __name__ == '__main__':
    main()
