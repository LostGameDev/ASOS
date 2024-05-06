import json
import sys
sys.path.append("..\\")
import Utils

def main_func(create, account=""):
    if create == True:
        firstname = Utils.OSInput("Enter first name: ")
        lastname = Utils.OSInput("Enter last name: ")
        password = Utils.OSInput("Enter password: ")
        accreditationlevel = int(Utils.OSInput("Enter accreditation level: "))
        email = Utils.OSInput("Enter email: ")
        accountname = firstname + "_" + lastname[0]
        data = {
            "password": password,
            "accreditation": accreditationlevel,
            "name": firstname + " " + lastname,
            "email": email
        }

        with open(f"../accounts/{accountname}.json", "w") as account_json:
            json.dump(data, account_json)
    else:
        pass

def start():
    editType = Utils.OSInput("Do you want to create a new account or edit an existing one? (Create or Edit): ")
    editType = editType.lower()
    if editType == "create":
        main_func(True)
    elif editType == "edit":
        accountToEdit = Utils.OSInput("Enter the account name you want to edit: ")
        main_func(False, accountToEdit)
    else:
        Utils.OSPrint(f"Error: {editType} unrecognized please choose Create or Edit!")
        start()

start()