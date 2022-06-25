import socket
import time
import shutil
from tkinter import *
import threading
import psutil
from datetime import datetime

class SocketData:
  HOST = '192.18=68.86.168'
  PORT = 65432

class Data:
    RPI_Status = "Disconnected"
    RPI_Polling_Period = 0
    RPI_Temperature = 0
    PreviousTemperatureData = []


t1 = 0
t2 = 0
def GetAvgTime(): # Return average time elapsed between socket pings
    global t1
    global t2
    t1 = t2
    t2 = time.perf_counter()
    Data.RPI_Polling_Period = round(((t2 - t1) * 1000), 2)

def Main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', SocketData.PORT))
        s.listen()
      
        conn, addr = s.accept()
        print(f"Connected to RPI [ {datetime.now()} ]")
        Data.RPI_Status = "Connected"
      
        with conn:
            n = 1
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                
                rawSocketData = str(data).split("'")
                usableData = rawSocketData[1]
              
                print(usableData)
              
                Data.RPI_Temperature = str(round(float(usabledata), 2))

                # Only run GetAvgTime occasionally to minimize resource usage
                # Must be run two cycles in a row otherwise it will not report correctly
                if n < 89:
                    n = n + 1
                elif n == 89:
                    n = n + 1
                    GetAvgTime()
                else:
                    GetAvgTime()
                    UpdateFile()
                    n = 1


def UpdateFile():
    # Format data as: time%rpi-status%rpi-polling-period%temperature
    currentTime = datetime.now()
    currentDate = datetime.today()
    timeString = f'{currentTime.strftime("%H:%M %p")} on {currentDate.strftime("%m/%d/%y")}'
    
    resultString = f'{timeString}%{Data.RPI_Status}%{Data.RPI_Polling_Period}ms%{Data.RPI_Temperature}'
    
    outputFile = open("data.txt", 'w')
    outputFile.write(resultString)
    outputFile.close()
  
    print(f'File Update Output: {output}')

def RunServer():
    while True:
        Main()

        # This code executed when socket disconnects
        Data.RPI_Status = "Disconnected"
        print(f"Attempting server restart- connection dropped [ {datetime.now()} ]")
        time.sleep(5)

print(f"Initializing server [ { datetime.now() } ]")
RunServer()
