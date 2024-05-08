import os
import time
import Utils
import json
import configparser
import winsound
import struct
from Commands import commands

AccreditationLevel = 0
registry = configparser.ConfigParser()
AdriveExists = True
OSVersion = ""

def LoadOS():
    os.system("cls")
    registry.read('.\OSRegistry.ini')
    registry.set('AOS', 'Quit', "False")
    with open('.\OSRegistry.ini', "w") as registryfile:
        registry.write(registryfile)
    OSVersion = registry.get('AOS', 'version')
    Utils.OSPrint(f"{OSVersion} starting.")
    Utils.OSLoad("Booting sequence initializing...", "Booting sequence initialized.", "Slow")
    Utils.OSLoad("Booting sequence completing...", "Booting sequence completed.", "Normal")
    time.sleep(1)
    Utils.OSPrint("Running on kernel ApertureScienceKernel ver 1. Processing speed of 4294967296 bytes/ms.")
    winsound.PlaySound("./sounds/startup.wav", winsound.SND_FILENAME)
    OSMain(False)

def CheckIfLoginExists(login):
    if os.path.exists(f"./accounts/{login}.json") == False:
        winsound.PlaySound("./sounds/error2.wav", winsound.SND_FILENAME)
        return False
    winsound.PlaySound("./sounds/correct.wav", winsound.SND_FILENAME)
    return True

def SetCurrentUser(login):
    registry.read('.\OSRegistry.ini')
    registry.set('AOS', 'CurrentUser', login)
    with open('.\OSRegistry.ini', "w") as registryfile:
        registry.write(registryfile)

def SetUserDirectory(login):
    registry.read('.\OSRegistry.ini')
    login = registry.get('AOS', 'CurrentUser')
    if registry.get('AOS', 'UserDirectory') == "":
        UserDirectory = f"A:/users/{login}/personal_files/"
        registry.read('.\OSRegistry.ini')
        registry.set('AOS', 'UserDirectory', UserDirectory)
        with open('.\OSRegistry.ini', "w") as registryfile:
            registry.write(registryfile)

def CheckIfPasswordExists(login, password):
    f = open(f"./accounts/{login}.json")
    data = json.loads(f.read())
    if data['password'] != password:
        winsound.PlaySound("./sounds/error2.wav", winsound.SND_FILENAME)
        return False
    winsound.PlaySound("./sounds/correct.wav", winsound.SND_FILENAME)
    return True

def GetAccreditationLevel(login):
    f = open(f"./accounts/{login}.json")
    data = json.loads(f.read())
    return data["accreditation"]

def CheckIfADriveExists(login):
    #This function checks if A drive exists, and if a user folder exists, if a user folder doesn't exist then it will create one
    if os.path.exists("./A"):
        if os.path.exists(f"./A/users/{login}/personal_files") != True:
            if os.path.exists(f"./A/users/") != True:
                os.mkdir("./A/users/")
            if os.path.exists(f"./A/users/{login}") != True:
                os.mkdir(f"./A/users/{login}")
            os.mkdir(f"./A/users/{login}/personal_files")
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
    if LoginFail == True:
        Utils.OSPrint("Please enter your credentials. Enter login below.")
    else:
        Utils.OSPrint("Welcome to the Aperture Science OS. Please enter your credentials. Enter login below.")
    login = Utils.OSInput(True)
    LoginCheck = CheckIfLoginExists(login)
    if LoginCheck != True:
        Utils.OSPrint("Login does not exist! Please try again!")
        OSMain(True)
    Utils.OSPrint("Login successfully identified. Please enter your password below.")
    SetCurrentUser(login)
    SetUserDirectory(login)
    password = Utils.OSInput(True)
    PasswordCheck = CheckIfPasswordExists(login, password)
    if PasswordCheck != True:
        Utils.OSPrint("Password is incorrect! Please try again!")
        OSMain(True)
    Utils.OSPrint(f"Password matching. Logging to account \"{login}\"")
    time.sleep(1)
    AccreditationLevel = GetAccreditationLevel(login)
    AdriveExists = CheckIfADriveExists(login)
    if AdriveExists != True:
        Utils.OSPrint("A drive does not exist")
        exit(1)
    Utils.OSPrint(f"Logged in. Account: \"{login}\". Level {AccreditationLevel} Accreditation.")
    time.sleep(0.5)
    Utils.OSPrint(f"Hello, user \"{login}\". What do you want to do? Enter \"help\" to show commands. Enter \"dir getname\" to show current directory, and its files. Enter \"exec\" to run a program. Enter \"open\" to open a file.")
    while True:
        registry.read(".\OSRegistry.ini")
        if registry.get('AOS', 'Quit') == "True":
            exit(0)
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
                        Utils.OSPrint(f"Error command \"{command_lower}\" has too many arguments!")
                    elif "takes from 1 to 2 positional arguments" in str(e):
                        Utils.OSPrint(f"Error command \"{command_lower}\" has too many arguments!")
                    else:
                        Utils.OSPrint(f"Unknown Error: {e}")
            else:
                try:
                    commands[command_lower]()
                except Exception as e:
                    if "missing 1 required positional argument" in str(e):
                        Utils.OSPrint(f"Error command \"{command_lower}\" has too few arguments!")
                    else:
                        Utils.OSPrint(f"Unknown Error: {e}")

        else:
            Utils.OSPrint("Invalid command. Enter \"help\" to see available commands.")
LoadOS()