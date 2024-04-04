import os
import sys
import time
import Utils
import json
from Commands import commands

AccreditationLevel = 0

def LoadOS():
    os.system("cls")
    f = open("quit.txt", "w")
    f.write("False")
    f.close()
    Utils.OSPrint("Aperture Science OS ver 0.1A (EXPERIMENTAL!) starting.")
    Utils.OSLoad("Booting sequence initializing...", "Booting sequence initialized.", "Slow")
    Utils.OSLoad("Booting sequence completing...", "Booting sequence completed.", "Slow")
    time.sleep(1)
    Utils.OSPrint("Running on kernel ApertureScienceKernel ver 1. Processing speed of 4294967296 bytes/ms.")
    time.sleep(1)
    OSMain(False)

def CheckIfLoginExists(login):
    if os.path.exists(f"./accounts/{login}.json") == False:
        return False
    return True

def SetCurrentUser(login):
    file = open(".\\CurrentUser.txt", "w")
    file.write(login)
    file.close()

def SetUserDirectory(login):
    CurrentUser = open(".\\CurrentUser.txt")
    login = CurrentUser.read()
    CurrentUser.close()
    if os.stat(".\\UserDirectory.txt").st_size == 0:
        UserDirectory = f"A:/users/{login}/personal_files/"
        file = open(".\\UserDirectory.txt", "w")
        file.write(UserDirectory)
        file.close()

def CheckIfPasswordExists(login, password):
    f = open(f"./accounts/{login}.json")
    data = json.loads(f.read())
    if data['password'] != password:
        return False
    return True

def GetAccreditationLevel(login):
    f = open(f"./accounts/{login}.json")
    data = json.loads(f.read())
    return data["accreditation"]

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
        Utils.OSPrint("Welcome to Aperture Science OS. Please enter your credentials. Enter login below.")
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
    Utils.OSPrint(f"Logged in. Account: \"{login}\". Level {AccreditationLevel} Accreditation.")
    time.sleep(0.5)
    Utils.OSPrint(f"Hello, user \"{login}\". What do you want to do? Enter \"help\" to show commands. Enter \"dir getname\" to show current directory, and its files. Enter \"exec\" to run a program. Enter \"open\" to open a file.")
    while True:
        f = open("quit.txt")
        data = f.read()
        f.close()
        if data == "True":
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
                except:
                    Utils.OSPrint(f"Error command \"{command_lower}\" has too many arguments!")
            else:
                try:
                    commands[command_lower]()
                except:
                    Utils.OSPrint(f"Error command \"{command_lower}\" has too few arguments!")

        else:
            Utils.OSPrint("Invalid command. Enter \"help\" to see available commands.")
LoadOS()