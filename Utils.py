import json
import time
import sys
import os

SystemCriticalFolders = ["users", "logs"]

def OSPrint(value):
    Msg = f">> {value}"
    print(Msg)
    OSLatestLog(Msg)

def OSLatestLog(value):
    latest_log = open("./A/logs/latest.log", "a")
    if "\n" in value:
        latest_log.write(value)
    else:
        latest_log.write(value + "\n")

def OSClearLatestLog():
    open("./A/logs/latest.log", "w").close()

def OSLoad(value, endmessage, speed):
    Completion = 0
    while Completion != 100:
        sys.stdout.write(f"\r>> {value} ({Completion}%)")
        if speed == "Slow":
            time.sleep(0.1)
        elif speed == "Normal":
            time.sleep(0.01)
        elif speed == "Fast":
            time.sleep(0.001)
        else:
            time.sleep(0.1)
        Completion += 1
    EndMessage = f"\r>> {endmessage} ({Completion}%)"
    sys.stdout.write(f"{EndMessage}                           ")
    sys.stdout.write("\n")
    OSLatestLog(EndMessage)

def OS_Shutdown(value):
    Completion = 0
    while Completion != 3:
        sys.stdout.write(f"\r>> {value}.  ")
        time.sleep(0.1)
        sys.stdout.write(f"\r>> {value}.. ")
        time.sleep(0.1)
        sys.stdout.write(f"\r>> {value}...")
        time.sleep(0.1)
        Completion += 1
    sys.stdout.write("\n")
    os.system("cls")

def OSInput(CaseSensitive):
    value = input("// ")
    if CaseSensitive != True:
        value = value.lower()
    OSLatestLog(f"// {value}")
    return value

def GetAccountAccredidation(login):
    f = open(f"./accounts/{login}.json")
    data = json.loads(f.read())
    accreditationlvl = data["accreditation"]
    return int(accreditationlvl)