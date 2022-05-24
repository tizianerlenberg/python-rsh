#!/usr/bin/env python3

import socket
import logging
import platform
import threading
import os
import time
import subprocess

# own libraries
import utils
import logHandler

logger = logging.getLogger(__name__)
# don't change log level here! change it in logHandler.py instead
logger.setLevel(logging.DEBUG)

logger.addHandler(logHandler.stream_handler)
logger.addHandler(logHandler.file_handler)

# ------------------------------------------------------------------------------

def connectBashToSlave(slave):
    p=subprocess.Popen(["/bin/bash"], stdout=slave, stderr=slave, stdin=slave)

def forwardFrom(readFrom, sock):
    string = ' '
    while string:
        string = os.read(readFrom, 1024)
        if string:
            sock.sendall(string)

def forwardTo(sock, writeTo):
    string = ' '
    while string:
        string = sock.recv(1024)
        if string:
            os.write(writeTo, string)

def platLinux(sock):
    import pty

    master, slave = pty.openpty()
    connectBashToSlave(slave)

    threading.Thread(target=forwardFrom, args=(master, sock,)).start()
    threading.Thread(target=forwardTo, args=(sock, master,)).start()
    while True:
        pass

def platWindows(conn):
    pass

def startOfProgram():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(("0.0.0.0",4445))
        s.listen(5)
        conn = s.accept()[0]

        if platform.system() == "Windows":
            platWindows(conn)
        else:
            platLinux(conn)
    finally:
        try:
            conn.close()
        except:
            pass
        s.close()

def main():
    startOfProgram()

if __name__ == '__main__':
    main()
