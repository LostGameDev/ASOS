import os
import struct
import sys
import time
import Utils
import json
import configparser
import winsound
from Commands import commands

AccreditationLevel = 0
registry = configparser.ConfigParser()
AdriveExists = True
OSVersion = ""

def get_base_path():
    return os.path.abspath(".")

def get_absolute_path(relative_path):
    return os.path.join(get_base_path(), relative_path)

def LoadOS():
    Utils.OSClearLatestLog()
    os.system("cls")
    registry.read(get_absolute_path('OSRegistry.ini'))
    registry.set('AOS', 'Quit', "False")
    with open(get_absolute_path('OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    registry.set('AOS', 'Reboot', "False")
    with open(get_absolute_path('OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
        registryfile.close()
    OSVersion = registry.get('AOS', 'version')
    Utils.OSPrint(f"{OSVersion} starting.")
    Utils.OSLoad("Booting sequence initializing...", "Booting sequence initialized.", "Slow")
    Utils.OSLoad("Booting sequence completing...", "Booting sequence completed.", "Normal")
    time.sleep(1)
    Utils.OSPrint("Running on kernel ApertureScienceKernel ver 1. Processing speed of 4294967296 bytes/ms.")
    winsound.PlaySound(get_absolute_path("sounds/startup.wav"), winsound.SND_FILENAME)
    OSMain(False)

def CheckIfLoginExists(login):
    if not os.path.exists(get_absolute_path(f"accounts/{login}.json")):
        winsound.PlaySound(get_absolute_path("sounds/error2.wav"), winsound.SND_FILENAME)
        return False
    winsound.PlaySound(get_absolute_path("sounds/correct.wav"), winsound.SND_FILENAME)
    return True

def SetCurrentUser(login):
    registry.read(get_absolute_path('OSRegistry.ini'))
    registry.set('AOS', 'CurrentUser', login)
    with open(get_absolute_path('OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)

def SetUserDirectory(login):
    registry.read(get_absolute_path('OSRegistry.ini'))
    login = registry.get('AOS', 'CurrentUser')
    if registry.get('AOS', 'UserDirectory') == "":
        UserDirectory = f"A/users/{login}/personal_files/"
        registry.read(get_absolute_path('OSRegistry.ini'))
        registry.set('AOS', 'UserDirectory', UserDirectory)
        with open(get_absolute_path('OSRegistry.ini'), "w") as registryfile:
            registry.write(registryfile)

def CheckIfPasswordExists(login, password):
    with open(get_absolute_path(f"accounts/{login}.json")) as f:
        data = json.loads(f.read())
    if data['password'] != password:
        winsound.PlaySound(get_absolute_path("sounds/error2.wav"), winsound.SND_FILENAME)
        return False
    winsound.PlaySound(get_absolute_path("sounds/correct.wav"), winsound.SND_FILENAME)
    return True

def GetAccreditationLevel(login):
    with open(get_absolute_path(f"accounts/{login}.json")) as f:
        data = json.loads(f.read())
    return data["accreditation"]

def CheckIfADriveExists(login):
    if os.path.exists(get_absolute_path("A")):
        if not os.path.exists(get_absolute_path(f"A/users/{login}/personal_files")):
            if not os.path.exists(get_absolute_path("A/users/")):
                os.mkdir(get_absolute_path("A/users/"))
            if not os.path.exists(get_absolute_path(f"A/users/{login}")):
                os.mkdir(get_absolute_path(f"A/users/{login}"))
            os.mkdir(get_absolute_path(f"A/users/{login}/personal_files"))
        if not os.path.exists(get_absolute_path("A/logs/")):
            os.mkdir(get_absolute_path("A/logs/"))
            with open(get_absolute_path("A/logs") + ".meta", "wb") as file:
                binary_data = struct.pack('i', 2)
                file.write(binary_data)
                file.close()
        return True
    else:
        return False

def tokenize_command(command):
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
    registry.set('AOS', 'LoggedOut', "False")
    with open(get_absolute_path('OSRegistry.ini'), "w") as registryfile:
        registry.write(registryfile)
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
    AdriveExists = CheckIfADriveExists(login)
    if not AdriveExists:
        Utils.OSPrintError("FATAL ERROR: A drive does not exist")
        sys.exit(1)
    Utils.OSPrint(f"Logged in. Account: \"{login}\". Level {AccreditationLevel} Accreditation.")
    time.sleep(0.5)
    Utils.OSPrint(f"Hello, user \"{login}\". What do you want to do? Enter \"help\" to show commands. Enter \"dir getname\" to show current directory, and its files. Enter \"exec\" to run a program. Enter \"open\" to open a file.")
    while True:
        registry.read(get_absolute_path("OSRegistry.ini"))
        if registry.get('AOS', 'Reboot') == "True":
            LoadOS()
        elif registry.get('AOS', 'loggedout') == "True":
            OSMain(False)
        elif registry.get('AOS', 'Quit') == "True":
            sys.exit(0)
        command = Utils.OSInput(True)
        tokens = tokenize_command(command)
        try:
            command_lower = tokens[0].lower()
        except:
            command_lower = ""
        if command_lower in commands:
            if len(tokens) > 1:
                try:
                    commands[command_lower](*tokens[1:])  # Pass all arguments
                except Exception as e:
                    if "takes 1 positional argument" in str(e):
                        Utils.OSPrintError(f"ERROR: Command \"{command_lower}\" has too many arguments!")
                    elif "takes from 1 to 2 positional arguments" in str(e):
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

        else:
            Utils.OSPrintWarning("Invalid command. Enter \"help\" to see available commands.")

LoadOS()