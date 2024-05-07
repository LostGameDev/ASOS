import json
import time
import sys
import os

def OSPrint(value):
    print(f">> {value}")

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
    sys.stdout.write(f"\r>> {endmessage} ({Completion}%)                           ")
    sys.stdout.write("\n")

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
    value = input(f"// ")
    if CaseSensitive != True:
        value = value.lower()
    return value

def GetAccountAccredidation(login):
    f = open(f"./accounts/{login}.json")
    data = json.loads(f.read())
    accreditationlvl = data["accreditation"]
    return int(accreditationlvl)