import os
import struct
import sys
import time
import Utils
import json
import configparser
import winsound
from Commands import commands

def GetBasePath():
    return os.path.abspath(".")

def GetAbsolutePath(relative_path):
    return os.path.join(GetBasePath(), relative_path)

AccreditationLevel = 0
Registry = configparser.ConfigParser()
AdriveExists = True
OSVersion = ""
OSRegistryPath = GetAbsolutePath('./OSRegistry.ini')

def LoadOS():
    Utils.OSClearLatestLog()
    os.system("cls")
    Registry.read(OSRegistryPath)
    Registry.set('AOS', 'Quit', "False")
    with open(OSRegistryPath, "w") as Registryfile:
        Registry.write(Registryfile)
    Registry.set('AOS', 'Reboot', "False")
    with open(OSRegistryPath, "w") as Registryfile:
        Registry.write(Registryfile)
    OSVersion = Registry.get('AOS', 'version')
    Utils.OSPrint(f"{OSVersion} starting.")
    Utils.OSLoad("Booting sequence initializing...", "Booting sequence initialized.", "Slow")
    Utils.OSLoad("Booting sequence completing...", "Booting sequence completed.", "Normal")
    time.sleep(1)
    Utils.OSPrint("Running on kernel ApertureScienceKernel ver 1. Processing speed of 4294967296 bytes/ms.")
    winsound.PlaySound(GetAbsolutePath("sounds/startup.wav"), winsound.SND_FILENAME)
    OSMain(False)

def CheckIfLoginExists(login):
    if not os.path.exists(GetAbsolutePath(f"accounts/{login}.json")):
        winsound.PlaySound(GetAbsolutePath("sounds/error2.wav"), winsound.SND_FILENAME)
        return False
    winsound.PlaySound(GetAbsolutePath("sounds/correct.wav"), winsound.SND_FILENAME)
    return True

def SetCurrentUser(login):
    Registry.read(OSRegistryPath)
    Registry.set('AOS', 'CurrentUser', login)
    with open(OSRegistryPath, "w") as Registryfile:
        Registry.write(Registryfile)

def SetUserDirectory(login):
    Registry.read(OSRegistryPath)
    login = Registry.get('AOS', 'CurrentUser')
    if Registry.get('AOS', 'UserDirectory') == "":
        UserDirectory = f"A/users/{login}/personal_files/"
        Registry.read(OSRegistryPath)
        Registry.set('AOS', 'UserDirectory', UserDirectory)
        with open(OSRegistryPath, "w") as Registryfile:
            Registry.write(Registryfile)

def CheckIfPasswordExists(login, password):
    with open(GetAbsolutePath(f"accounts/{login}.json")) as f:
        data = json.loads(f.read())
    if data['password'] != password:
        winsound.PlaySound(GetAbsolutePath("sounds/error2.wav"), winsound.SND_FILENAME)
        return False
    winsound.PlaySound(GetAbsolutePath("sounds/correct.wav"), winsound.SND_FILENAME)
    return True

def GetAccreditationLevel(login):
    with open(GetAbsolutePath(f"accounts/{login}.json")) as f:
        data = json.loads(f.read())
    return data["accreditation"]

def CheckIfCriticalFoldersExist(login):
    CheckIfADriveExists()
    CheckIfLogsFolderExists()
    CheckIfUsersFolderExists()
    CheckIfCurrentUserFolderExists(login)
    CheckIfPersonalFilesFolderExists(login)

def CheckIfADriveExists():
    if not os.path.exists(GetAbsolutePath("A")):
        try:
            os.mkdir(GetAbsolutePath("./A"))
        except:
            Utils.OSPrintError("FATAL ERROR: Could not create A drive")
            sys.exit(1)

def CheckIfLogsFolderExists():
        if not os.path.exists(GetAbsolutePath("A/logs/")):
            try:
                os.mkdir(GetAbsolutePath("A/logs/"))
            except:
                Utils.OSPrintError("FATAL ERROR: Could not create logs folder")
                sys.exit(1)
            try:
                with open(GetAbsolutePath("A/logs") + ".meta", "wb") as file:
                    binary_data = struct.pack('i', 2)
                    file.write(binary_data)
                    file.close()
            except:
                Utils.OSPrintError("FATAL ERROR: Could not create logs meta file")
                sys.exit(1)

def CheckIfUsersFolderExists():
    if not os.path.exists(GetAbsolutePath("A/users/")):
        try:
            os.mkdir(GetAbsolutePath("A/users/"))
        except:
            Utils.OSPrintError("FATAL ERROR: Could not create users folder")
            sys.exit(1)

def CheckIfCurrentUserFolderExists(login):
    if not os.path.exists(GetAbsolutePath(f"A/users/{login}")):
        try:
            os.mkdir(GetAbsolutePath(f"A/users/{login}"))
        except:
            Utils.OSPrintError(f"FATAL ERROR: Could not create {login} folder")
            sys.exit(1)

def CheckIfPersonalFilesFolderExists(login):
    if not os.path.exists(GetAbsolutePath(f"A/users/{login}/personal_files")):
        try:
            os.mkdir(GetAbsolutePath(f"A/users/{login}/personal_files"))
        except:
            Utils.OSPrintError("FATAL ERROR: Could not create personal files folder")
            sys.exit(1)

def TokenizeCommand(command):
    tokens = []
    current_token = ''
    in_quotes = False
    for char in command:
        if char == ' ' and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ''
        elif char == '"':
            in_quotes = not in_quotes
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    return tokens

def OSMain(LoginFail):
    Registry.set('AOS', 'LoggedOut', "False")
    with open(OSRegistryPath, "w") as Registryfile:
        Registry.write(Registryfile)
    if LoginFail:
        Utils.OSPrint("Please enter your credentials. Enter login below.")
    else:
        Utils.OSPrint("Welcome to the Aperture Science OS. Please enter your credentials. Enter login below.")
    login = Utils.OSInput(True)
    LoginCheck = CheckIfLoginExists(login)
    if not LoginCheck:
        Utils.OSPrintWarning("Login does not exist! Please try again")
        OSMain(True)
    Utils.OSPrint("Login successfully identified. Please enter your password below.")
    SetCurrentUser(login)
    SetUserDirectory(login)
    password = Utils.OSInput(True)
    PasswordCheck = CheckIfPasswordExists(login, password)
    if not PasswordCheck:
        Utils.OSPrintWarning("Password is incorrect! Please try again")
        OSMain(True)
    Utils.OSPrint(f"Password matching. Logging to account \"{login}\"")
    time.sleep(1)
    AccreditationLevel = GetAccreditationLevel(login)
    CheckIfCriticalFoldersExist(login)
    Utils.OSPrint(f"Logged in. Account: \"{login}\". Level {AccreditationLevel} Accreditation.")
    time.sleep(0.5)
    Utils.OSPrint(f"Hello, user \"{login}\". What do you want to do? Enter \"help\" to show commands. Enter \"dir getname\" to show current directory, and its files. Enter \"exec\" to run a program. Enter \"open\" to open a file.")
    while True:
        Registry.read(OSRegistryPath)
        if Registry.get('AOS', 'Reboot') == "True":
            LoadOS()
        elif Registry.get('AOS', 'loggedout') == "True":
            OSMain(False)
        elif Registry.get('AOS', 'Quit') == "True":
            sys.exit(0)
        command = Utils.OSInput(True)
        tokens = TokenizeCommand(command)
        try:
            command_lower = tokens[0].lower()
        except:
            command_lower = ""
        if command_lower not in commands:
            Utils.OSPrintWarning("Invalid command. Enter \"help\" to see available commands.")
            continue

        if len(tokens) > 1:
            try:
                commands[command_lower](*tokens[1:])  # Pass all arguments
            except Exception as e:
                if "takes 1 positional argument" in str(e) or "takes from 1 to 2 positional arguments" in str(e):
                    Utils.OSPrintError(f"ERROR: Command \"{command_lower}\" has too many arguments!")
                else:
                    Utils.OSPrintError(f"UNKNOWN ERROR: {e}")
        else:
            try:
                commands[command_lower]()
            except Exception as e:
                if "missing 1 required positional argument" in str(e):
                    Utils.OSPrintError(f"ERROR: Command \"{command_lower}\" has too few arguments!")
                else:
                    Utils.OSPrintError(f"UNKNOWN ERROR: {e}")  

LoadOS()