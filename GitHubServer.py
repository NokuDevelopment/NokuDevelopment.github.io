import socket
import time
import shutil
from tkinter import *
import threading
import psutil
from datetime import datetime

HOST = '192.168.86.168'
PORT = 65432

def runmain():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', PORT))
        s.listen()
        conn, addr = s.accept()
        print(f"Connected to RPI [ {datetime.now()} ]")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                raw = str(data).split("'")
                usabledata = raw[1]
                print(usabledata)
                outputFile = open("data.txt", "w")
                outputFile.write(usabledata)
                outputFile.close()

def runserver():
    while True:
        runmain()
        print(f"Attempting server restart- connection dropped [ {datetime.now()} ]")
        time.sleep(5)

print(f"Initializing server [ { datetime.now() } ]")
runserver()