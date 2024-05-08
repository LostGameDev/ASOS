import json
import os
import aosAPI

def main_func(create, account=""):
    if create == True:
        aosAPI.AOSPrint("Enter first name")
        firstname = aosAPI.AOSInput(True)
        aosAPI.AOSPrint("Enter last name")
        lastname = aosAPI.AOSInput(True)
        aosAPI.AOSPrint("Enter password")
        password = aosAPI.AOSInput(True)
        aosAPI.AOSPrint("Enter accreditation level")
        accreditationlevel = int(aosAPI.AOSInput(False))
        aosAPI.AOSPrint("Enter email")
        email = aosAPI.AOSInput(False)
        firstname = firstname.replace(" ", "")
        firstname = firstname.replace("_", "")
        lastname = lastname.replace(" ", "")
        lastname = lastname.replace("_", "")
        if accreditationlevel < 1:
            accreditationlevel = 1
        elif accreditationlevel > 3:
            accreditationlevel = 3
        accountname = firstname.lower() + "_" + lastname[0].lower()
        data = {
            "password": password,
            "accreditation": accreditationlevel,
            "name": firstname + " " + lastname,
            "email": email
        }

        with open(f"../accounts/{accountname}.json", "w") as account_json:
            json.dump(data, account_json, indent=4)
        aosAPI.AOSPrint(f"Account created successfully! Your login information is: {accountname}, {password}")
    elif create == False and account != "":
        f = open(f"../accounts/{account}.json")
        data = json.loads(f.read())
        firstname = data["name"].split(" ")[0]
        lastname = data["name"].split(" ")[1]
        password = data["password"]
        accreditationlevel = data["accreditation"]
        email = data["email"]
        newdata = {
            "password": password,
            "accreditation": accreditationlevel,
            "name": firstname + " " + lastname,
            "email": email
        }
        aosAPI.AOSPrint(f"Account: {account}")
        print(" ")
        aosAPI.AOSPrint(f"(1) First Name: {firstname}")
        aosAPI.AOSPrint(f"(2) Last Name: {lastname}")
        aosAPI.AOSPrint(f"(3) Password: {password}")
        aosAPI.AOSPrint(f"(4) Accreditation level: {accreditationlevel}")
        aosAPI.AOSPrint(f"(5) Email: {email}")
        aosAPI.AOSPrint(f"(6) Exit")
        print(" ")
        aosAPI.AOSPrint(f"Which value do you want to edit? (Enter the number corrisponding to each value)")
        choice = aosAPI.AOSInput(False)
        if choice == "1":
            aosAPI.AOSPrint("Enter new first name")
            newfirstname = aosAPI.AOSInput(True)
            newfirstname = newfirstname.replace(" ", "")
            newfirstname = newfirstname.replace("_", "")
            newdata["name"] = newfirstname + " " + lastname
            with open(f"../accounts/{account}.json", "w") as account_json:
                json.dump(newdata, account_json, indent=4)
            main_func(False, account)
        elif choice == "2":
            aosAPI.AOSPrint("Enter new last name")
            newlastname = aosAPI.AOSInput(True)
            newlastname = newlastname.replace(" ", "")
            newlastname = newlastname.replace("_", "")
            newdata["name"] = firstname + " " + newlastname
            with open(f"../accounts/{account}.json", "w") as account_json:
                json.dump(newdata, account_json, indent=4)
            main_func(False, account)
        elif choice == "3":
            aosAPI.AOSPrint("Enter new password")
            newpassword = aosAPI.AOSInput(True)
            newdata["password"] = newpassword
            with open(f"../accounts/{account}.json", "w") as account_json:
                json.dump(newdata, account_json, indent=4)
            main_func(False, account)
        elif choice == "4":
            aosAPI.AOSPrint("Enter new accreditation level")
            newaccreditationlevel = int(aosAPI.AOSInput(False))
            if newaccreditationlevel < 1:
                newaccreditationlevel = 1
            elif newaccreditationlevel > 3:
                newaccreditationlevel = 3
            newdata["accreditation"] = newaccreditationlevel
            with open(f"../accounts/{account}.json", "w") as account_json:
                json.dump(newdata, account_json, indent=4)
            main_func(False, account)
        elif choice == "5":
            aosAPI.AOSPrint("Enter new email address")
            newemail = aosAPI.AOSInput(False)
            newdata["email"] = newemail
            with open(f"../accounts/{account}.json", "w") as account_json:
                json.dump(newdata, account_json, indent=4)
            main_func(False, account)
        elif choice == "6":
            with open(f"../accounts/{account}.json", "w") as account_json:
                json.dump(newdata, account_json, indent=4)
                aosAPI.AOSLoad("Exiting the \"Aperture Science Account Editor\"", "Exited the \"Aperture Science Account Editor\"", "Fast")
        else:
            aosAPI.AOSPrint("Error invalid choice!")
            main_func(False, account)
        
    else:
        aosAPI.AOSPrint("Error you must supply an account name!")

def load():
    aosAPI.AOSPrint("Do you want to create a new account or edit an existing one? (Create or Edit)")
    editType = aosAPI.AOSInput(False)
    if editType == "create":
        main_func(True)
    elif editType == "edit":
        aosAPI.AOSPrint("Enter the account name you want to edit")
        accountToEdit = aosAPI.AOSInput(False)
        if os.path.isfile(f"../accounts/{accountToEdit}.json"):
            main_func(False, accountToEdit)
        else:
            aosAPI.AOSPrint(f"Error account {accountToEdit} does not exist!")
            load()
    else:
        aosAPI.AOSPrint(f"Error: {editType} unrecognized")
        load()
load()