import os
import subprocess
import sys
import shutil
import Utils
import time
import configparser

registry = configparser.ConfigParser()

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
            Utils.OSPrint(f"Command \"{command}\" does not exist or does not have a definition!")

def CheckIfDirectoryExists(directory):
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in directory)
    if os.path.exists(ConvertedDir):
        return True
    return False

def GetUserDirectory():
    registry.read('.\OSRegistry.ini')
    login = registry.get('AOS', 'CurrentUser')
    if registry.get('AOS', 'UserDirectory') == "":
        UserDirectory = f"A:/users/{login}/personal_files/"
        registry.read('.\OSRegistry.ini')
        registry.set('AOS', 'UserDirectory', UserDirectory)
        with open('.\OSRegistry.ini', "w") as registryfile:
            registry.write(registryfile)
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        os.system(f"cd {ConvertedDir}")
        return 
    else:
        registry.read('.\OSRegistry.ini')
        UserDirectory = registry.get('AOS', 'UserDirectory')
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        os.system(f"cd {ConvertedDir}")
        return UserDirectory

def CommandDir(arg, arg2=""):
    UserDirectory = GetUserDirectory()

    #For some reason "&" does not work the same way as "and" in python. WHY?!?

    if arg == "getname" and arg2 == "":
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
    elif arg == "getname" and arg2 == "-P":
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
    elif arg == "access" and arg2 != "":
        Exists = CheckIfDirectoryExists(arg2)
        if Exists == False:
            Utils.OSPrint(f"Directory does not exist!")
            return
        registry.read('.\OSRegistry.ini')
        registry.set('AOS', 'UserDirectory', arg2)
        with open('.\OSRegistry.ini', "w") as registryfile:
            registry.write(registryfile)
        UserDirectory = arg2
        char = {"/":'\\', ":":"", '"':''}
        ConvertedDir = ".\\" + ''.join(char.get(s, s) for s in UserDirectory)
        os.system(f"cd {ConvertedDir}")
        Utils.OSPrint(f"Now located in {arg2}")
    else:
        return

def CommandExec(program):
    UserDirectory = GetUserDirectory()

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

def CommandOpen(File):
    UserDirectory = GetUserDirectory()

    python_executable = sys.executable  # Path to the Python executable running this script
    python_path = os.environ.get("PYTHONPATH", "")  # Get the current PYTHONPATH
    env = os.environ.copy()  # Create a copy of the current environment variables
    env["PYTHONPATH"] = python_path  # Set the PYTHONPATH for the subprocess
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    Utils.OSLoad(f"Booting \"TextEditor.py\"", f"Aperture Science Text Editor running. Accessing file \"{File}\"", "Normal")
    subprocess.run([python_executable, "TextEditor.py", "..\\" + ConvertedDir + File], env=env, shell=True, cwd = "./ROM/")

def CommandCat(File):
    UserDirectory = GetUserDirectory()
    char = {"/":'\\', ":":"", '"':''}
    ConvertedDir = "" + ''.join(char.get(s, s) for s in UserDirectory)
    f = open(ConvertedDir + File, 'r')
    data = f.readlines()
    for line in data:
        line = line.rstrip('\n')
        Utils.OSPrint(line)
        time.sleep(0.1)
    f.close()

def CommandClear():
    os.system("cls")

def CommandCreate(Name, Type):
    UserDirectory = GetUserDirectory()
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

def CommandDelete(Name, Type):
    UserDirectory = GetUserDirectory()

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

def CommandQuit():
    Utils.OS_Shutdown("Shutting down")
    registry.read('.\OSRegistry.ini')
    registry.set('AOS', 'Quit', "True")
    with open('.\OSRegistry.ini', "w") as registryfile:
        registry.write(registryfile)
    registry.read('.\OSRegistry.ini')
    registry.set('AOS', 'CurrentUser', "")
    with open('.\OSRegistry.ini', "w") as registryfile:
        registry.write(registryfile)
    registry.read('.\OSRegistry.ini')
    registry.set('AOS', 'UserDirectory', "")
    with open('.\OSRegistry.ini', "w") as registryfile:
        registry.write(registryfile)

commands = {
    "help": CommandHelp,
    "dir": CommandDir,
    "exec": CommandExec,
    "open": CommandOpen,
    "cat": CommandCat,
    "clear": CommandClear,
    "create": CommandCreate,
    "delete": CommandDelete,
    "clear": CommandClear,
    "cls": CommandClear,
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
    "create": "Creates a new file or folder in the current directory. It has the following arguments:\n\t<name>: The name of the file or folder to create.\n\t-Type <type>: Specifies whether to create a file (-File) or a folder (-Folder).",
    "delete": "Deletes a specified file or folder. It has the following arguments:\n\t<name>: The name of the file or folder to delete.\n\t-Type <type>: Specifies whether to delete a file (-File) or a folder (-Folder).",
    "quit": "Shuts down the operating system."
}