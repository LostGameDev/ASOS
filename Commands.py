import gzip
import json
import os
import subprocess
import sys
import shutil
import threading
import Utils
import time
import configparser
import platform
import psutil
import cpuinfo
import struct
from queue import Queue

registry = configparser.ConfigParser()

def get_base_path():
    return os.path.abspath(".")

def get_absolute_path(relative_path):
    return os.path.join(get_base_path(), relative_path)

def CommandHelp(command=""):
    if command == "":
        Utils.OSPrint("Available commands:")
        time.sleep(0.1)
        for command in commands:
            Utils.OSPrint(command)
            time.sleep(0.1)
    else:
        if command in commandDefinitions:
            Utils.OSPrint(commandDefinitions[command])
        else:
            Utils.OSPrintWarning(f"Command \"{command}\" does not exist or does not have a definition!")

def CheckIfDirectoryExists(directory):
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in directory))
    if os.path.exists(ConvertedDir):
        return True
    if os.path.isfile(ConvertedDir):
        return True
    return False

def CheckIfFileExists(file):
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in file))
    if os.path.isfile(ConvertedDir):
        return True
    return False

def GetUserDirectory():
    registry.read(get_absolute_path("OSRegistry.ini"))
    login = registry.get('AOS', 'CurrentUser')
    if registry.get('AOS', 'UserDirectory') == "":
        try:
            UserDirectory = f"A:/users/{login}/personal_files/"
            registry.read(get_absolute_path("OSRegistry.ini"))
            registry.set('AOS', 'UserDirectory', UserDirectory)
            with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
                registry.write(registryfile)
                registryfile.close()
            char = {"/":'\\', ":":"", '"':''}
            ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
            os.system(f"cd {ConvertedDir}")
        except:
            UserDirectory = f"A:/users/{login}/"
            registry.read(get_absolute_path("OSRegistry.ini"))
            registry.set('AOS', 'UserDirectory', UserDirectory)
            with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
                registry.write(registryfile)
                registryfile.close()
            char = {"/":'\\', ":":"", '"':''}
            ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
            os.system(f"cd {ConvertedDir}")
        return
    else:
        registry.read(get_absolute_path("OSRegistry.ini"))
        UserDirectory = registry.get('AOS', 'UserDirectory')
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
        os.system(f"cd {ConvertedDir}")
        return UserDirectory

def is_binary(file_name):
    try:
        with open(file_name, 'tr') as check_file:  # try open file in text mode
            check_file.read()
            check_file.close()
            return False
    except:  # if fails then file is non-text (binary)
        return True

def CommandDir(arg, arg2=""):
    UserDirectory = GetUserDirectory()

    #For some reason "&" does not work the same way as "and" in python. WHY?!?

    if arg == "getname" and arg2 == "":
        Utils.OSPrint(f"Current directory is: {UserDirectory}")
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
        FileCount = 0
        FolderCount = 0
        for item in os.listdir(get_absolute_path(ConvertedDir)):
            if os.path.isfile(get_absolute_path(os.path.join(ConvertedDir, item))):
                if ".meta" in item: 
                    FileCount += 0
                elif ".gitignore" in item:
                    FileCount += 0
                else:
                    FileCount += 1
            if os.path.isdir(get_absolute_path(os.path.join(ConvertedDir, item))):
                FolderCount += 1
        if FileCount == 0 and FolderCount == 0:
            Utils.OSPrint(f"0 files detected. 0 sub-directories detected. Folder is empty.")
        else:
            Utils.OSPrint(f"{FileCount} files detected. {FolderCount} sub-directories detected.")
        return
    elif arg == "getname" and arg2 == "-P":
        Utils.OSPrint(f"Current directory is: {UserDirectory}")
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
        FileCount = 0
        FolderCount = 0
        for item in os.listdir(get_absolute_path(ConvertedDir)):
            if os.path.isfile(get_absolute_path(os.path.join(ConvertedDir, item))):
                if ".meta" in item: 
                    FileCount += 0
                elif ".gitignore" in item:
                    FileCount += 0
                else:
                    FileCount += 1
                    Utils.OSPrint(f"File: {item}")
            if os.path.isdir(get_absolute_path(os.path.join(ConvertedDir, item))):
                FolderCount += 1
                Utils.OSPrint(f"Sub-directory: {item}")
        if FileCount == 0 and FolderCount == 0:
            Utils.OSPrint(f"0 files detected. 0 sub-directories detected. Folder is empty.")
        else:
            Utils.OSPrint(f"{FileCount} files detected. {FolderCount} sub-directories detected.")
        return
    elif arg == "access" and arg2 != "":
        if "./" in arg2:
            arg2 = arg2.replace("./", UserDirectory)
        if "." in arg2:
            arg2 = arg2.replace(".", UserDirectory)
        if arg2.endswith("/") != True:
            arg2 = arg2 + "/"
        if "A:/users/" in arg2:
            registry.read(get_absolute_path("OSRegistry.ini"))
            login = registry.get('AOS', 'currentuser')
            accredidation = Utils.GetAccountAccredidation(login)
            if login not in arg2 and accredidation != 3:
                Utils.OSPrintError(f"ERROR: Cannot access you do not have permission to access this directory")
                return
        Exists = CheckIfDirectoryExists(arg2)
        if Exists == False:
            Utils.OSPrintError(f"ERROR: Directory does not exist!")
            return
        registry.read(get_absolute_path("OSRegistry.ini"))
        registry.set('AOS', 'UserDirectory', arg2)
        with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
            registry.write(registryfile)
            registryfile.close()
        UserDirectory = arg2
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
        os.system(f"cd {ConvertedDir}")
        Utils.OSPrint(f"Now located in {arg2}")
    else:
        Utils.OSPrintError("ERROR: Invalid argument(s)!")

def CommandExec(program):
    UserDirectory = GetUserDirectory()

    python_executable = sys.executable  # Path to the Python executable running this script
    python_path = os.environ.get("PYTHONPATH", "")  # Get the current PYTHONPATH
    env = os.environ.copy()  # Create a copy of the current environment variables
    env["PYTHONPATH"] = python_path  # Set the PYTHONPATH for the subprocess
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
    for item in os.listdir(get_absolute_path(ConvertedDir)):
        if os.path.isfile(get_absolute_path(os.path.join(ConvertedDir, item))) and item == program:
            if item.endswith(".py"):
                try:
                    Utils.OSLoad(f"Booting \"{program}\"", f"\"{program}\" running.", "Normal")
                    subprocess.run([python_executable, item], env=env, shell=True, cwd = ConvertedDir)
                except FileNotFoundError:
                    Utils.OSPrintWarning("File not found.")
            elif item.endswith(".exe"):
                try:
                    Utils.OSLoad(f"Booting \"{program}\"", f"\"{program}\" running.", "Normal")
                    os.system(f"{ConvertedDir + item}")
                except FileNotFoundError:
                    Utils.OSPrintWarning("File not found.")
            else:
                Utils.OSPrintWarning("Only python programs and windows exe's can be executed.")
            break
    else:
        Utils.OSPrint("Program not found.")

def CommandOpen(File):
    if ".meta" in File:
        File = File.replace(".meta", "")
    UserDirectory = GetUserDirectory()
    python_executable = sys.executable  # Path to the Python executable running this script
    python_path = os.environ.get("PYTHONPATH", "")  # Get the current PYTHONPATH
    env = os.environ.copy()  # Create a copy of the current environment variables
    env["PYTHONPATH"] = python_path  # Set the PYTHONPATH for the subprocess
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
    try:
        FileMetadata = open(get_absolute_path(ConvertedDir + File + ".meta"), "rb")
        min_accredidation = struct.unpack('i', FileMetadata.read())[0]
        FileMetadata.close()
    except:
        min_accredidation = 1
    registry.read(get_absolute_path("OSRegistry.ini"))
    login = registry.get('AOS', 'currentuser')
    accredidation = Utils.GetAccountAccredidation(login)
    if min_accredidation > accredidation:
        Utils.OSPrintWarning(f"Cannot open \"{File}\" you do not have permission to access this file")
        return
    if is_binary(ConvertedDir + File):
        Utils.OSPrintError(f"ERROR: Cannot open file \"{File}\" because \"{File}\" is a binary file!")
        return
    if ".log" in File:
        Utils.OSPrintWarning(f"Log files cannot be opened with the open command! Use the view_log command!")
        return
    Utils.OSLoad(f"Booting \"TextEditor.py\"", f"Aperture Science Text Editor running. Accessing file \"{File}\"", "Normal")
    subprocess.run([python_executable, "TextEditor.py", "..\\" + ConvertedDir + File], env=env, shell=True, cwd = "./ROM/")

def CommandCat(File, Output=""):
    UserDirectory = GetUserDirectory()
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
    if ".meta" in File:
        File= File.replace(".meta", "")
    if ".meta" in Output:
        Output = Output.replace(".meta", "")
    if ".log" in File:
        Utils.OSPrintWarning(f"Log files cannot be viewed with the cat command! Use the view_log command!")
        return
    files = File.split()
    if len(files) == 1:
        if is_binary(get_absolute_path(ConvertedDir + files[0])):
            Utils.OSPrintError(f"ERROR: Cannot open file \"{files[0]}\" because \"{files[0]}\" is a binary file!")
            return
        f = open(get_absolute_path(ConvertedDir + files[0]), 'r')
        data = f.readlines()
        for line in data:
            line = line.rstrip('\n')
            Utils.OSPrint(line)
            time.sleep(0.1)
        f.close()
    elif len(files) > 1:
        output_data = []
        for file_name in files:
            if is_binary(get_absolute_path(ConvertedDir + file_name)):
                Utils.OSPrintError(f"ERROR: Cannot open file \"{file_name}\" because \"{file_name}\" is a binary file!")
                continue
            try:
                with open(get_absolute_path(ConvertedDir + file_name), 'r') as f:
                    data = f.readlines()
                    output_data.extend(data)
                    if file_name != files[-1]:
                        output_data.append('\n')
            except FileNotFoundError:
                Utils.OSPrintWarning(f"File \"{file_name}\" not found.")
        if Output:
            with open(get_absolute_path(ConvertedDir + Output), 'w') as f:
                f.writelines(output_data)
                f.close()
        else:
            for line in output_data:
                line = line.rstrip('\n')
                Utils.OSPrint(line)
                time.sleep(0.1)
    else:
        Utils.OSPrintWarning("No files specified.")

def CommandClear():
    os.system("cls")

def CommandCreate(Name, Type):
    if ".meta" in Name:
        Name = Name.replace(".meta", "")
    UserDirectory = GetUserDirectory()
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))
    if Type == "-File":
        if os.path.isfile(ConvertedDir + Name) != True:
            try:
                if UserDirectory == "A:/users/":
                    Utils.OSPrintWarning(f"Cannot create \"{Name}\" you do not have permission to create files in this directory.")
                    return
                registry.read(get_absolute_path("OSRegistry.ini"))
                CurrentUser = registry.get('AOS', 'CurrentUser')
                accreditationlvl = Utils.GetAccountAccredidation(CurrentUser)
                Utils.OSPrint(f"Enter the lowest level of accreditation level that is required to access this file")
                Accreditationlevel = int(Utils.OSInput(False))
                while Accreditationlevel > accreditationlvl:
                    Accreditationlevel -= 1;
                if Accreditationlevel < 1:
                    Accreditationlevel = 1
                elif Accreditationlevel > 3:
                    Accreditationlevel = 3
                Utils.OSLoad(f"Creating file \"{Name}\"...", f"File \"{Name}\" created.", "Normal")
                open(ConvertedDir + Name, "w")
                with open(ConvertedDir + Name + ".meta", "wb") as file:
                    binary_data = struct.pack('i', Accreditationlevel)
                    file.write(binary_data)
                    file.close()
            except:
                Utils.OSPrintError(f"ERROR: Failed to create file \"{Name}\"")
                return
        else:
            Utils.OSPrintWarning(f"Failed to create file \"{Name}\" file already exists")
    elif Type == "-Folder":
        if os.path.exists(get_absolute_path(ConvertedDir + Name)) != True:
            if Name in Utils.SystemCriticalFolders:
                Utils.OSPrintWarning(f"Failed to create folder \"{Name}\" you cannot create a folder with the same name as a system critical folder!")
                return
            try:
                if UserDirectory == "A:/users/":
                    Utils.OSPrintWarning(f"Cannot create \"{Name}\" you do not have permission to create folders in this directory.")
                    return
                registry.read(get_absolute_path("OSRegistry.ini"))
                CurrentUser = registry.get('AOS', 'CurrentUser')
                accreditationlvl = Utils.GetAccountAccredidation(CurrentUser)
                Utils.OSPrint(f"Enter the lowest level of accreditation level that is required to access this folder")
                Accreditationlevel = int(Utils.OSInput(False))
                while Accreditationlevel > accreditationlvl:
                    Accreditationlevel -= 1;
                if Accreditationlevel < 1:
                    Accreditationlevel = 1
                elif Accreditationlevel > 3:
                    Accreditationlevel = 3
                Utils.OSLoad(f"Creating Folder \"{Name}\"...", f"Folder \"{Name}\" created.", "Normal")
                os.mkdir(get_absolute_path(ConvertedDir + Name))
                with open(get_absolute_path(ConvertedDir + Name + ".meta"), "wb") as file:
                    binary_data = struct.pack('i', Accreditationlevel)
                    file.write(binary_data)
                    file.close()
            except:
                Utils.OSPrintError(f"ERROR: Failed to create folder \"{Name}\"")
                return
        else:
            Utils.OSPrintWarning(f"Failed to create folder \"{Name}\" folder already exists")
    else:
        Utils.OSPrintWarning(f"Invalid Type \"{Type}\"")
        return

def CommandDelete(Name, Type):
    if ".meta" in Name:
        Name = Name.replace(".meta", "")
    UserDirectory = GetUserDirectory()
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = get_absolute_path("" + ''.join(char.get(s, s) for s in UserDirectory))
    if Type == "-File":
        try:
            if UserDirectory == "A:/users/" or UserDirectory == "A:/logs/":
                Utils.OSPrintWarning(f"Cannot delete \"{Name}\" you do not have permission to delete files in this directory")
                return
            try:
                FileMetadata = open(get_absolute_path(ConvertedDir + Name + ".meta"), "rb")
                min_accredidation = struct.unpack('i', FileMetadata.read())[0]
                FileMetadata.close()
            except:
                min_accredidation = 1
            registry.read(get_absolute_path("OSRegistry.ini"))
            login = registry.get('AOS', 'currentuser')
            accredidation = Utils.GetAccountAccredidation(login)
            if min_accredidation > accredidation:
                Utils.OSPrintWarning(f"Cannot delete \"{Name}\" you do not have permission to delete this file")
                return
            Utils.OSLoad(f"Deleting file \"{Name}\"...", f"File \"{Name}\" deleted.", "Normal")
            os.remove(get_absolute_path(ConvertedDir + Name))
            try:
                os.remove(get_absolute_path(ConvertedDir + Name + ".meta"))
            except:
                Utils.OSLatestLog(f"Failed to delete file \"{Name}\"'s meta file!")
        except FileNotFoundError:
            Utils.OSPrintError(f"ERROR: File \"{Name}\" does not exist!")
        return
    elif Type == "-Folder":
        try:
            if Name in Utils.SystemCriticalFolders:
                Utils.OSPrintWarning(f"Cannot delete \"{Name}\" you do not have permission to delete this directory")
                return
            if UserDirectory == "A:/users/":
                Utils.OSPrintWarning(f"Cannot delete \"{Name}\" you do not have permission to delete this directory")
                return
            try:
                FileMetadata = open(get_absolute_path(ConvertedDir + Name + ".meta"), "rb")
                min_accredidation = struct.unpack('i', FileMetadata.read())[0]
                FileMetadata.close()
            except:
                min_accredidation = 1
            registry.read(get_absolute_path("OSRegistry.ini"))
            login = registry.get('AOS', 'currentuser')
            accredidation = Utils.GetAccountAccredidation(login)
            if min_accredidation > accredidation:
                Utils.OSPrintWarning(f"Cannot delete \"{Name}\" you do not have permission to delete this directory")
                return
            Utils.OSLoad(f"Deleting Folder \"{Name}\"...", f"Folder \"{Name}\" deleted.", "Normal")
            shutil.rmtree(get_absolute_path(ConvertedDir + Name))
            try:
                os.remove(get_absolute_path(ConvertedDir + Name + ".meta"))
            except:
                Utils.OSLatestLog(f"Failed to delete folder \"{Name}\"'s meta file!")
        except:
            Utils.OSPrintError(f"ERROR: Folder \"{Name}\" does not exist!")
        return
    else:
        Utils.OSPrintWarning(f"Invalid Type \"{Type}\"...")
        return

def CommandTime():
    Utils.OSPrint(time.ctime())

def get_cpu_info(result_queue):
    cpu_info = cpuinfo.get_cpu_info()['brand_raw']
    result_queue.put(cpu_info)

def get_cpu_info_load():
    #dont ask...
    Utils.OSLoad("Getting system information.", "System information acquired", "Slow")

def CommandSysInfo():
    #didn't think i would have to add mutithreading for this command to work but here we are!
    registry.read(get_absolute_path("OSRegistry.ini"))
    OSVersion = registry.get('AOS', 'version')
    login = registry.get('AOS', 'currentuser')
    f = open(get_absolute_path(f"./accounts/{login}.json"))
    data = json.loads(f.read())
    f.close()
    AccreditationLevel = data["accreditation"]
    CPUArchitecture = platform.machine()
    CPUFamily = platform.processor()
    result_queue = Queue()
    cpu_thread = threading.Thread(target=get_cpu_info, args=(result_queue,))
    os_load_thread = threading.Thread(target=get_cpu_info_load)
    cpu_thread.start()
    os_load_thread.start()
    cpu_thread.join()
    os_load_thread.join()
    CPUName = result_queue.get()
    Cpu = ' '.join([str(CPUName), str(CPUFamily)])
    CPUCores = os.cpu_count()
    Ram = int(round(psutil.virtual_memory().total / (1024. **3)))
    Utils.OSPrint("System Info: ")
    time.sleep(0.1)
    Utils.OSPrint(f"Operating System Version: {OSVersion}")
    time.sleep(0.1)
    Utils.OSPrint(f"Current User: {login}, Accreditation Level: {AccreditationLevel}")
    time.sleep(0.1)
    Utils.OSPrint(f"System Architecture: {CPUArchitecture}")
    time.sleep(0.1)
    Utils.OSPrint(f"Processor: {Cpu}")
    time.sleep(0.1)
    Utils.OSPrint(f"CPU Cores: {CPUCores}")
    time.sleep(0.1)
    Utils.OSPrint(f"Memory: {Ram} GB")
    time.sleep(0.1)

def CommandQuit():
    Utils.OS_Shutdown("Shutting down")
    registry.read(get_absolute_path("OSRegistry.ini"))
    registry.set('AOS', 'Quit', "True")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'Reboot', "False")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'loggedout', "False")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'CurrentUser', "")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'UserDirectory', "")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()

def CommandAccountEditor():
    registry.read(get_absolute_path("OSRegistry.ini"))
    CurrentUser = registry.get('AOS', 'CurrentUser')
    accreditationlvl = Utils.GetAccountAccredidation(CurrentUser)
    if accreditationlvl == 3:
        python_executable = sys.executable  # Path to the Python executable running this script
        python_path = os.environ.get("PYTHONPATH", "")  # Get the current PYTHONPATH
        env = os.environ.copy()  # Create a copy of the current environment variables
        env["PYTHONPATH"] = python_path  # Set the PYTHONPATH for the subprocess
        Utils.OSLoad(f"Booting \"AccountEditor.py\"", f"Aperture Science Account Editor running.", "Normal")
        subprocess.run([python_executable, "AccountEditor.py"], env=env, shell=True, cwd = "./ROM/")
    else:
        Utils.OSPrintWarning("You do not have permission to use the \"Aperture Science Account Editor\"")

def CommandDeleteAccount(account):
    registry.read(get_absolute_path("OSRegistry.ini"))
    CurrentUser = registry.get('AOS', 'CurrentUser')
    accreditationlvl = Utils.GetAccountAccredidation(CurrentUser)
    if accreditationlvl == 3:
        registry.read(get_absolute_path("OSRegistry.ini"))
        CurrentUser = registry.get('AOS', 'CurrentUser')
        if account == CurrentUser:
            Utils.OSPrintWarning(f"Cannot delete account \"{account}\" you cannot delete your own account")
            return
        Utils.OSLoad(f"Deleting account: {account}", f"Account {account} deleted", "Normal")
        try:
            os.remove(get_absolute_path(f"./accounts/{account}.json"))
            shutil.rmtree(get_absolute_path(f"./A/users/{account}/"))
        except:
            Utils.OSPrintError(f"ERROR: Failed to delete account \"{account}\" does this account exist?")
            return
    else:
        Utils.OSPrintWarning(f"Cannot delete account \"{account}\" you do not have permission to run this command")

def CommandViewLog(File):
    registry.read(get_absolute_path("OSRegistry.ini"))
    CurrentUser = registry.get('AOS', 'CurrentUser')
    accreditationlvl = Utils.GetAccountAccredidation(CurrentUser)
    if accreditationlvl >= 2:
        LogsDirectory = get_absolute_path("./A/logs/")
        if ".meta" in File:
            File= File.replace(".meta", "")
        if is_binary(get_absolute_path(LogsDirectory + File)):
            try:
                with gzip.open(get_absolute_path(f'{LogsDirectory + File}'),'rt') as fin:
                    data = fin.readlines()     
                    Utils.OSPrint(f"{File}:")
                    for line in data:        
                        line = line.rstrip('\n')
                        print(line)
                        Utils.OSLatestLog(line)
                        time.sleep(0.1)
                    Utils.OSPrint(f"End of log file")
            except FileNotFoundError:
                Utils.OSPrintWarning(f"Log \"{File}\" not found.")
            return
        try:
            f = open(get_absolute_path(LogsDirectory + File), 'r')
            data = f.readlines()
            Utils.OSPrint(f"{File}:")
            for line in data:
                line = line.rstrip('\n')
                print(line)
                Utils.OSLatestLog(line)
                time.sleep(0.1)
            f.close()
            Utils.OSPrint(f"End of log file")
        except FileNotFoundError:
            Utils.OSPrintWarning(f"Log \"{File}\" not found.")
            return
    else:
        Utils.OSPrintWarning(f"Could not open log file \"{File}\" you do not have permission to use this command")

def CommandReboot():
    Utils.OS_Shutdown("Rebooting")
    registry.read(get_absolute_path("OSRegistry.ini"))
    registry.set('AOS', 'Reboot', "True")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'CurrentUser', "")
    with open(get_absolute_path('.\OSRegistry.ini')) as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'UserDirectory', "")
    with open(get_absolute_path('.\OSRegistry.ini')) as registryfile:
        registry.write(registryfile)
        registryfile.close()

def CommandLogout():
    Utils.OS_Shutdown("Logging out")
    registry.read(get_absolute_path("OSRegistry.ini"))
    registry.set('AOS', 'Quit', "False")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'Reboot', "False")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'loggedout', "True")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'CurrentUser', "")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'UserDirectory', "")
    with open(get_absolute_path('.\OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()

def CommandCopy(Name, Directory, Type):
    UserDirectory = GetUserDirectory()

    if ".meta" in Name:
        Name = Name.replace(".meta", "")

    if "./" in Directory:
        Directory = Directory.replace("./", UserDirectory)

    if "A:/users/" in Directory:
        registry.read(get_absolute_path("OSRegistry.ini"))
        login = registry.get('AOS', 'currentuser')
        accredidation = Utils.GetAccountAccredidation(login)
        if login not in Directory and accredidation != 3:
            Utils.OSPrintError(f"ERROR: Cannot access you do not have permission to access this directory")
            return
            
    DirExists = CheckIfDirectoryExists(Directory)
    FileExists = CheckIfFileExists(Directory)
    if DirExists == False and Type == "-Folder":
        Utils.OSPrintError(f"ERROR: Directory does not exist!")
        return
    if FileExists == True and Type == "-File":
        Utils.OSPrintError(f"ERROR: File already exists!")
        return
    char = {"/":'\\', ":":"", '"':'', '.':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in Directory))
    ConvertedUserDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))

    if Type == "-File":
        try:
            shutil.copy2(get_absolute_path(ConvertedUserDir + Name, ConvertedDir))
            shutil.copy2(get_absolute_path(ConvertedUserDir + Name + ".meta", ConvertedDir))
            Utils.OSPrint(f"File \"{Name}\" was copied successfully to \"{Directory}\"")
        except shutil.SameFileError:
            Utils.OSPrintError(f"ERROR: Can not copy file \"{Name}\" to \"{Directory}\" because they are the same file")
            return
        except:
            Utils.OSPrintError(f"ERROR: Failed to copy file \"{Name}\"")
            return
    elif Type == "-Folder":
        try:
            os.mkdir(get_absolute_path(f"{ConvertedDir}/{Name}"))
            shutil.copytree(get_absolute_path(ConvertedUserDir + Name), get_absolute_path(ConvertedDir+Name), dirs_exist_ok=True)
            shutil.copy2(get_absolute_path(ConvertedUserDir + Name + ".meta"), get_absolute_path(ConvertedDir))
            Utils.OSPrint(f"Folder \"{Name}\" was copied successfully to \"{Directory}\"")
        except shutil.SameFileError:
            Utils.OSPrintError(f"ERROR: Can not copy folder \"{Name}\" to \"{Directory}\" because they are the same folder")
            return
        except:
            Utils.OSPrintError(f"ERROR: Failed to copy folder \"{Name}\"")
            return
    else:
        Utils.OSPrintWarning(f"Invalid type \"{Type}\"")

def CommandMove(Name, Directory, Type):
    UserDirectory = GetUserDirectory()

    if ".meta" in Name:
        Name = Name.replace(".meta", "")

    if "./" in Directory:
        Directory = Directory.replace("./", UserDirectory)

    if "A:/users/" in Directory:
        registry.read(get_absolute_path("OSRegistry.ini"))
        login = registry.get('AOS', 'currentuser')
        accredidation = Utils.GetAccountAccredidation(login)
        if login not in Directory and accredidation != 3:
            Utils.OSPrintError(f"ERROR: Cannot access you do not have permission to access this directory")
            return
        
    DirExists = CheckIfDirectoryExists(Directory)
    FileExists = CheckIfFileExists(Directory)
    if DirExists == False and Type == "-Folder":
        Utils.OSPrintError(f"ERROR: Directory does not exist!")
        return
    if FileExists == True and Type == "-File":
        Utils.OSPrintError(f"ERROR: File already exists!")
        return
    char = {"/":'\\', ":":"", '"':'', '.':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in Directory))
    ConvertedUserDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))

    if Type == "-File":
        try:
            shutil.copy2(get_absolute_path(ConvertedUserDir + Name, ConvertedDir))
            shutil.copy2(get_absolute_path(ConvertedUserDir + Name + ".meta", ConvertedDir))
            os.remove(get_absolute_path(ConvertedUserDir + Name))
            os.remove(get_absolute_path(ConvertedUserDir + Name + ".meta"))
            Utils.OSPrint(f"File \"{Name}\" was moved successfully to \"{Directory}\"")
        except shutil.SameFileError:
            Utils.OSPrintError(f"ERROR: Can not move file \"{Name}\" to \"{Directory}\" because they are the same file")
            return
        except:
            Utils.OSPrintError(f"ERROR: Failed to move file \"{Name}\"")
            return
    elif Type == "-Folder":
        try:
            os.mkdir(get_absolute_path(f"{ConvertedDir}/{Name}"))
            shutil.copytree(get_absolute_path(ConvertedUserDir + Name), get_absolute_path(ConvertedDir+Name), dirs_exist_ok=True)
            shutil.copy2(get_absolute_path(ConvertedUserDir + Name + ".meta"), get_absolute_path(ConvertedDir))
            shutil.rmtree(get_absolute_path(ConvertedUserDir + Name))
            os.remove(get_absolute_path(ConvertedUserDir + Name + ".meta"))
            Utils.OSPrint(f"Folder \"{Name}\" was moved successfully to \"{Directory}\"")
        except shutil.SameFileError:
            Utils.OSPrintError(f"ERROR: Can not move folder \"{Name}\" to \"{Directory}\" because they are the same folder")
            return
        except:
            Utils.OSPrintError(f"ERROR: Failed to move folder \"{Name}\"")
            return
    else:
        Utils.OSPrintWarning(f"Invalid type \"{Type}\"")

def CommandRename(Name, NewName, Type):
    UserDirectory = GetUserDirectory()

    if ".meta" in Name:
        Name = Name.replace(".meta", "")

    char = {"/":'\\', ":":"", '"':'', '.':''}
    ConvertedDir = get_absolute_path(".\\" + ''.join(char.get(s, s) for s in UserDirectory))

    if Type == "-File":
        try:
            shutil.copy2(get_absolute_path(ConvertedDir + Name), get_absolute_path(ConvertedDir + NewName))
            shutil.copy2(get_absolute_path(ConvertedDir + Name + ".meta"), get_absolute_path(ConvertedDir + NewName + ".meta"))
            os.remove(get_absolute_path(ConvertedDir + Name))
            os.remove(get_absolute_path(ConvertedDir + Name + ".meta"))
            Utils.OSPrint(f"File \"{Name}\" renamed to \"{NewName}\"")
            return
        except shutil.SameFileError:
            #if the name is the same then just do nothing
            Utils.OSPrint(f"File \"{Name}\" renamed to \"{NewName}\"")
            return
        except:
            Utils.OSPrintError(f"Failed to rename \"{Name}\" to \"{NewName}\"")
            return
    if Type == "-Folder":
        try:
            os.mkdir(get_absolute_path(ConvertedDir + NewName))
            shutil.copytree(get_absolute_path(ConvertedDir + Name), get_absolute_path(ConvertedDir + NewName), dirs_exist_ok=True)
            shutil.rmtree(get_absolute_path(ConvertedDir + Name))
            shutil.copy2(get_absolute_path(ConvertedDir + Name + ".meta"), get_absolute_path(ConvertedDir + NewName + ".meta"))
            os.remove(get_absolute_path(ConvertedDir + Name + ".meta"))
            Utils.OSPrint(f"File \"{Name}\" renamed to \"{NewName}\"")
            return
        except shutil.SameFileError:
            #if the name is the same then just do nothing
            Utils.OSPrint(f"File \"{Name}\" renamed to \"{NewName}\"")
            return
        except:
            Utils.OSPrintError(f"Failed to rename \"{Name}\" to \"{NewName}\"")
            return
    else:
        Utils.OSPrintWarning(f"Invalid type \"{Type}\"")

commands = {
    "help": CommandHelp,
    "dir": CommandDir,
    "exec": CommandExec,
    "open": CommandOpen,
    "cat": CommandCat,
    "clear": CommandClear,
    "create": CommandCreate,
    "delete": CommandDelete,
    "copy": CommandCopy,
    "move": CommandMove,
    "rename": CommandRename,
    "cls": CommandClear,
    "time": CommandTime,
    "sysinfo": CommandSysInfo,
    "account_edit": CommandAccountEditor,
    "delete_account": CommandDeleteAccount,
    "view_log": CommandViewLog,
    "logout": CommandLogout,
    "reboot": CommandReboot,
    "quit": CommandQuit
}

commandDefinitions = {
    "help": "Prints all available commands or provides specific information about a command. It has the following arguments:\n\t<command>: The name of the command to help the user with.",
    "dir": "Used to list files and directories in the current directory or change the current directory. It has the following arguments:\n\tgetname: Prints the current directory and the number of files and subdirectories.\n\tgetname -P: Prints the current directory, the number of files and subdirectories, and lists all files and subdirectories.\n\taccess <directory>: Changes the current directory to the specified directory.",
    "exec": "Executes a specified Python program in the current directory. It has the following arguments:\n\t<program>: The name of the Python program to execute.",
    "open": "Opens a specified file in the default text editor. It has the following arguments:\n\t<file>: The name of the file to open.",
    "cat": "Lists the contents of a specified file however if given two or more files it will concatenate them displaying them directly after each other. It has the following arguments:\n\t<file>: The name of the file(s) to list.\n\t<output>: The name of the file to output too.",
    "clear": "Clears the screen.",
    "cls": "Clears the screen.",
    "create": "Creates a new file or folder in the current directory. It has the following arguments:\n\t<name>: The name of the file or folder to create.\n\t<Type>: Specifies whether to create a file (-File) or a folder (-Folder).",
    "delete": "Deletes a specified file or folder. It has the following arguments:\n\t<name>: The name of the file or folder to delete.\n\t-Type <type>: Specifies whether to delete a file (-File) or a folder (-Folder).",
    "quit": "Shuts down the operating system.",
    "reboot": "Reboots the operating system.",
    "time": "Prints the current time",
    "sysinfo": "Prints system information",
    "account_edit": "Runs the built-in account editor allowing for users to edit or create accounts only useable for accounts with an accreditation level of 3",
    "logout": "Logs out the current user",
    "delete_account": "Deletes a specified account, you cannot delete the currently logged-in account, only useable for accounts with an accreditation level of 3. It has the following arguments:\n\t<account>: The name of the account to delete",
    "view_log": "Lists specified log file only useable for accounts with an accreditation level of 2, it has the following arguments:\n\t<file> The log file to view",
    "copy": "Copies the specified file or directory to the specified location. It has the following arguments:\n\t<Name> The name of the file or directory to copy.\n\t<Type>: Specifies whether to copy a file (-File) or a folder (-Folder).\n\t<Destination> The path to the destination directory/file to copy to.",
    "move": "Moves the specified file or directory to the specified location. It has the following arguments:\n\t<Name> The name of the file or directory to copy.\n\t<Type>: Specifies whether to move a file (-File) or a folder (-Folder).\n\t<Destination> The path to the destination directory/file to move to.",
    "rename": "Rename the specified file or directory. It has the following arguments:\n\t<Name> The name of the file/directory to be renamed.\n\t<NewName> The new name that the file/directory will be renamed to.\n\t<Type>: Specifies whether to rename a file (-File) or a folder (-Folder)."
}