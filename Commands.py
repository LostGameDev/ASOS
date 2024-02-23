import os
import subprocess
import sys
import shutil
import Utils

def CommandHelp(login):
    Utils.OSPrint("Available commands:")
    for command in commands:
        Utils.OSPrint(command)

def CheckIfDirectoryExists(directory):
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in directory)
    if os.path.exists(ConvertedDir):
        return True
    return False

def CommandDir(arg, arg2=None, login=None):
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        os.system(f"cd {ConvertedDir}")
    else:
        file = open(".\\UserDirectory.txt", "r")
        UserDirectory = file.read()
        file.close()
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        os.system(f"cd {ConvertedDir}")
        
    if arg == "getname":
        Utils.OSPrint(f"Current directory is: {UserDirectory}")
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        FileCount = 0
        FolderCount = 0
        for item in os.listdir(ConvertedDir):
            if os.path.isfile(os.path.join(ConvertedDir, item)):
                FileCount += 1
            if os.path.isdir(os.path.join(ConvertedDir, item)):
                FolderCount += 1
        if FileCount == 0 and FolderCount == 0:
            Utils.OSPrint(f"0 files detected. 0 sub-directories detected. Folder is empty.")
        else:
            Utils.OSPrint(f"{FileCount} files detected. {FolderCount} sub-directories detected.")
        return
    elif arg == "getname -P":
        Utils.OSPrint(f"test")
        Utils.OSPrint(f"Current directory is: {UserDirectory}")
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        FileCount = 0
        FolderCount = 0
        for item in os.listdir(ConvertedDir):
            if os.path.isfile(os.path.join(ConvertedDir, item)):
                FileCount += 1
                Utils.OSPrint(f"File: {item}")
            if os.path.isdir(os.path.join(ConvertedDir, item)):
                FolderCount += 1
                Utils.OSPrint(f"Sub-directory: {item}")
        if FileCount == 0 and FolderCount == 0:
            Utils.OSPrint(f"0 files detected. 0 sub-directories detected. Folder is empty.")
        else:
            Utils.OSPrint(f"{FileCount} files detected. {FolderCount} sub-directories detected.")
        return
    Exists = CheckIfDirectoryExists(arg)
    if Exists == False:
        Utils.OSPrint(f"Directory does not exist!")
        return
    file = open(".\\UserDirectory.txt", "w")
    file.write(arg)
    file.close()
    UserDirectory = arg
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
    os.system(f"cd {ConvertedDir}")
    Utils.OSPrint(f"Now located in {arg}")

def CommandExec(program, login):
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()
    else:
        file = open(".\\UserDirectory.txt", "r")
        UserDirectory = file.read()
        file.close()

    python_executable = sys.executable  # Path to the Python executable running this script
    python_path = os.environ.get("PYTHONPATH", "")  # Get the current PYTHONPATH
    env = os.environ.copy()  # Create a copy of the current environment variables
    env["PYTHONPATH"] = python_path  # Set the PYTHONPATH for the subprocess
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    for item in os.listdir(ConvertedDir):
        if os.path.isfile(os.path.join(ConvertedDir, item)) and item == program:
            if item.endswith(".py"):
                try:
                    Utils.OSLoad(f"Booting \"{program}\"", f"\"{program}\" running.", "Normal")
                    subprocess.run([python_executable, item], env=env, shell=True, cwd = ConvertedDir)
                except FileNotFoundError:
                    Utils.OSPrint("File not found.")
            else:
                Utils.OSPrint("Only python programs can be executed.")
            break
    else:
        Utils.OSPrint("Program not found.")

def CommandOpen(File, login):
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()
    else:
        file = open(".\\UserDirectory.txt", "r")
        UserDirectory = file.read()
        file.close()
    python_executable = sys.executable  # Path to the Python executable running this script
    python_path = os.environ.get("PYTHONPATH", "")  # Get the current PYTHONPATH
    env = os.environ.copy()  # Create a copy of the current environment variables
    env["PYTHONPATH"] = python_path  # Set the PYTHONPATH for the subprocess
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    Utils.OSLoad(f"Booting \"TextEditor.py\"", f"Aperture Science Text Editor running. Accessing file \"{File}\"", "Normal")
    subprocess.run([python_executable, "TextEditor.py", "..\\" + ConvertedDir + File], env=env, shell=True, cwd = "./ROM/")

def CommandList(File, login):
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()
    else:
        file = open(".\\UserDirectory.txt", "r")
        UserDirectory = file.read()
        file.close() 
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    f = open(ConvertedDir + File, 'r')
    data = f.readlines()
    for line in data:
        Utils.OSPrint(line)
    f.close()

def CommandClear(login):
    os.system("cls")

def CommandCreate(Name, Type, login):
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()
    else:
        file = open(".\\UserDirectory.txt", "r")
        UserDirectory = file.read()
        file.close() 
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    if Type == "-File":
        try:
            Utils.OSLoad(f"Creating file \"{Name}\"...", f"File \"{Name}\" created.", "Normal")
            open(ConvertedDir + Name, "w")
        except:
            Utils.OSPrint(f"Failed to create file \"{Name}\"")
        return
    elif Type == "-Folder":
        try:
            Utils.OSLoad(f"Creating Folder \"{Name}\"...", f"Folder \"{Name}\" created.", "Normal")
            os.mkdir(ConvertedDir + Name)
        except:
            Utils.OSPrint(f"Failed to create folder \"{Name}\"")
        return
    else:
        Utils.OSPrint(f"Invalid Type \"{Type}\"...")
        return

def CommandDelete(Name, Type, login):
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()
    else:
        file = open(".\\UserDirectory.txt", "r")
        UserDirectory = file.read()
        file.close() 
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    if Type == "-File":
        try:
            Utils.OSLoad(f"Deleting file \"{Name}\"...", f"File \"{Name}\" deleted.", "Normal")
            os.remove(ConvertedDir + Name + ".txt")
        except:
            Utils.OSPrint(f"File \"{Name}\" does not exist!")
        return
    elif Type == "-Folder":
        try:
            Utils.OSLoad(f"Deleting Folder \"{Name}\"...", f"Folder \"{Name}\" deleted.", "Normal")
            shutil.rmtree(ConvertedDir + Name)
        except:
            Utils.OSPrint(f"Folder \"{Name}\" does not exist!")
        return
    else:
        Utils.OSPrint(f"Invalid Type \"{Type}\"...")
        return

commands = {
    "help": CommandHelp,
    "dir": CommandDir,
    "exec": CommandExec,
    "open": CommandOpen,
    "list": CommandList,
    "clear": CommandClear,
    "create": CommandCreate,
    "delete": CommandDelete,
}