import socket
import time
import shutil
from tkinter import *
import threading
import psutil
from datetime import datetime
from datetime import timedelta


class SocketData:
    HOST = '192.18=68.86.168'
    PORT = 65432


class Data:
    RPI_Status = "Disconnected"
    RPI_Polling_Period = 0
    RPI_Temperature = 0
    PreviousTemperatureData = []  # Temperature data from the past 8 hours
    TemperatureHistoryTimeStamps = []  # The time of submission of elements in PreviousTemperatureData
    HalfHourTemperatureAverage = 0.00 # 30 minute average; reset with every update to PreviousTemperatureData
    HalfHourTemperatureAverageDataPoints = 0  # Number of data points, used to calculate average


t1 = 0
t2 = 0


def GetAvgTime():  # Return average time elapsed between socket pings
    global t1
    global t2
    t1 = t2
    t2 = time.perf_counter()
    Data.RPI_Polling_Period = round(((t2 - t1) * 1000), 2)

def UpdateRPITemperature(temperature):
    try:
        Data.RPI_Temperature = str(round(float(temperature), 2))
    except:
        Data.RPI_Temperature = temperature[0:5]
        temperature = temperature[0:5]

    Data.HalfHourTemperatureAverage = Data.HalfHourTemperatureAverage + float(temperature)
    Data.HalfHourTemperatureAverageDataPoints = Data.HalfHourTemperatureAverageDataPoints + 1

    if Data.TemperatureHistoryTimeStamps[len(Data.TemperatureHistoryTimeStamps) - 1] <= (datetime.now() - timedelta(minutes=30)):
        HalfHourAverage = float(Data.HalfHourTemperatureAverage) / float(Data.HalfHourTemperatureAverageDataPoints)

        Data.TemperatureHistoryTimeStamps.append(datetime.now())
        Data.PreviousTemperatureData.append(HalfHourAverage)
        del Data.PreviousTemperatureData[0]
        del Data.TemperatureHistoryTimeStamps[0]

        tempString = ''
        for s in Data.PreviousTemperatureData:
            tempString = tempString + str(s) + "%"
        tempString = tempString[:-1]

        backupFile = open("backup.txt", 'w')
        backupFile.write(tempString)
        backupFile.close()

        Data.HalfHourTemperatureAverage = 0.00
        Data.HalfHourTemperatureAverageDataPoints = 0

        print(f'Updated graph ({HalfHourAverage}℉) at {datetime.now().strftime("%I:%M %p")}')

def Main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', SocketData.PORT))
        s.listen()

        conn, addr = s.accept()
        print(f"Connected to RPI [ {datetime.now()} ]")
        print()
        Data.RPI_Status = "Connected"

        with conn:
            n = 1
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                rawSocketData = str(data).split("'")
                usableData = rawSocketData[1]

                UpdateRPITemperature(usableData)

                # Only run GetAvgTime occasionally to minimize resource usage
                # Must be run two cycles in a row otherwise it will not report correctly
                if n < 9:
                    n = n + 1
                elif n == 9:
                    n = n + 1
                    GetAvgTime()
                else:
                    GetAvgTime()
                    UpdateFile()
                    n = 1


def UpdateFile():
    # Format data as: time%rpi-status%rpi-polling-period%temperature%previous$temp$data
    currentTime = datetime.now()
    currentDate = datetime.today()
    timeString = f'{currentTime.strftime("%I:%M %p")} on {currentDate.strftime("%m/%d/%y")}'

    previousTempDataString = ""
    for s in Data.PreviousTemperatureData:
        previousTempDataString = previousTempDataString + str(s) + "$"
    previousTempDataString = previousTempDataString[:-1]

    resultString = f'{timeString}%{Data.RPI_Status}%{Data.RPI_Polling_Period}ms%{Data.RPI_Temperature}%{previousTempDataString}'

    outputFile = open("data.txt", 'w')
    outputFile.write(resultString)
    outputFile.close()

    #print(f'File Update Output: {resultString}')



def RunServer():
    while True:
        Main()

        # This code executed when socket disconnects
        Data.RPI_Status = "Disconnected"
        print(f"Attempting server restart- connection dropped [ {datetime.now()} ]")
        time.sleep(5)


# Populate the previous temperature list
def PopulateLists():
    i = 0
    while i < 15:
        Data.PreviousTemperatureData.append(0)
        Data.TemperatureHistoryTimeStamps.append(datetime.now() - timedelta(hours=10))
        i = i + 1

    recover = input('Recover from backup (Y/N)? ')
    if recover == 'y' or recover == 'Y':
        try:
            backupFile = open('backup.txt', 'r')
            recoveryData = backupFile.read()
            backupFile.close()
            recoveryArr = recoveryData.split('%')
            n = 0
            while n < 15:
                Data.PreviousTemperatureData[n] = recoveryArr[n]
                n = n + 1
        except:
            recoveryData = input('Enter backup file string: ')
            recoveryArr = recoveryData.split('%')

            n = 0
            while n < 15:
                Data.PreviousTemperatureData[n] = recoveryArr[n]
                n = n + 1

        print()
        print('Data recovery complete. Recovered data: ')
        print(f'{Data.PreviousTemperatureData}')

    print()

PopulateLists()

print(f"Initializing server [ {datetime.now()} ]")
RunServer()
