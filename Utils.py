import json
import time
import sys
import os
import shutil
import gzip
from colorama import init as colorama_init
from colorama import Fore, Style

colorama_init()

SystemCriticalFolders = ["users", "logs"]

def get_base_path():
    return os.path.abspath(".")

def get_log_path():
    return os.path.join(get_base_path(), "A", "logs")

def ensure_log_directory():
    log_path = get_log_path()
    if not os.path.exists(log_path):
        os.makedirs(log_path)

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
    ensure_log_directory()
    latest_log = open(os.path.join(get_log_path(), "latest.log"), "a")
    if "\n" in value:
        latest_log.write(value)
    else:
        latest_log.write(value + "\n")

def OSClearLatestLog():
    log_path = get_log_path()
    ensure_log_directory()
    if not os.path.isfile(os.path.join(log_path, "latest.log")):
        open(os.path.join(log_path, "latest.log"), "w").close()
        return
    FileCount = 0
    for item in os.listdir(log_path):
        if os.path.isfile(os.path.join(log_path, item)):
            if ".meta" not in item and ".gitignore" not in item: 
                FileCount += 1
    if FileCount >= 6:
        shutil.rmtree(log_path)
        os.makedirs(log_path)
        open(os.path.join(log_path, "latest.log"), "w").close()
        return
        
    CurrentTime = time.ctime()
    CurrentTime = CurrentTime.replace(" ", "-")
    CurrentTime = CurrentTime.replace(":", "-")
    latest_log_path = os.path.join(log_path, "latest.log")
    backup_log_path = os.path.join(log_path, f"{CurrentTime}.log")
    gzip_log_path = f"{backup_log_path}.gz"
    shutil.copy(latest_log_path, backup_log_path)
    with open(backup_log_path, 'rb') as f_in:
        with gzip.open(gzip_log_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(backup_log_path)
    open(latest_log_path, "w").close()

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
    if not CaseSensitive:
        value = value.lower()
    OSLatestLog(f"// {value}")
    return value

def GetAccountAccredidation(login):
    with open(os.path.join(get_base_path(), "accounts", f"{login}.json")) as f:
        data = json.loads(f.read())
    accreditationlvl = data["accreditation"]
    return int(accreditationlvl)
