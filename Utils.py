import json
import time
import sys
import os
import shutil
import gzip
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

SystemCriticalFolders = ["users", "logs"]

def OSPrint(value):
    Msg = f">> {value}"
    print(Msg)
    OSLatestLog(Msg)

def OSPrintError(value):
    Error = f"{Fore.RED}/!\ {value} /!\{Style.RESET_ALL}"
    LogError = f"/!\ {value} /!\ "
    print(Error)
    OSLatestLog(LogError)

def OSPrintWarning(value):
    Warn = f"{Fore.YELLOW}! {value} !{Style.RESET_ALL}"
    LogWarn = f"! {value} !"
    print(Warn)
    OSLatestLog(LogWarn)

def OSLatestLog(value):
    latest_log = open("./A/logs/latest.log", "a")
    if "\n" in value:
        latest_log.write(value)
    else:
        latest_log.write(value + "\n")

def OSClearLatestLog():
    if os.path.exists("./A/logs/") != True:
        os.mkdir("./A/logs/")
    if os.path.isfile("./A/logs/latest.log") != True:
        open("./A/logs/latest.log", "w").close()
        return
    FileCount = 0
    for item in os.listdir("./A/logs/"):
        if os.path.isfile(os.path.join("./A/logs/", item)):
            if ".meta" not in item or ".gitignore" not in item: 
                FileCount += 1
    if FileCount >= 6:
        shutil.rmtree("./A/logs/")
        os.mkdir("./A/logs/")
        open("./A/logs/latest.log", "w").close()
        return
        
    CurrentTime = time.ctime()
    CurrentTime = CurrentTime.replace(" ", "-")
    CurrentTime = CurrentTime.replace(":", "-")
    shutil.copy("./A/logs/latest.log", f"./A/logs/{CurrentTime}.log")
    with open(f"./A/logs/{CurrentTime}.log", 'rb') as f_in:
        with gzip.open(f"./A/logs/{CurrentTime}.log.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(f"./A/logs/{CurrentTime}.log")
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