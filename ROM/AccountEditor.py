import json
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
        f = open(f"./accounts/{account}.json")
        data = json.loads(f.read())
        firstname = data["name"].split(" ")[0]
        lastname = data["name"].split(" ")[1]
        password = data["password"]
        accreditationlevel = data["accreditation"]
        email = data["email"]
        aosAPI.AOSPrint(f"Account: {account}")
        print(" ")
        aosAPI.AOSPrint(f"(1) First Name: {firstname}")
        aosAPI.AOSPrint(f"(2) Last Name: {lastname}")
        aosAPI.AOSPrint(f"(3) Password: {password}")
        aosAPI.AOSPrint(f"(4) Accreditation level: {accreditationlevel}")
        aosAPI.AOSPrint(f"(5) Email: {email}")
        print(" ")
        aosAPI.AOSPrint(f"Which value do you want to edit? (Enter the number corrisponding to each value)")
        choice = aosAPI.AOSInput(False)
        if choice == "1":
            aosAPI.AOSPrint("Enter new first name")
            newfirstname = aosAPI.AOSInput(True)
            newfirstname = newfirstname.replace(" ", "")
            newfirstname = newfirstname.replace("_", "")
    else:
        pass

    
aosAPI.AOSPrint("Do you want to create a new account or edit an existing one? (Create or Edit)")
editType = aosAPI.AOSInput(False)
if editType == "create":
    main_func(True)
elif editType == "edit":
    aosAPI.AOSPrint("Enter the account name you want to edit")
    accountToEdit = aosAPI.AOSInput(False)
    main_func(False, accountToEdit)
else:
    aosAPI.AOSPrint(f"Error: {editType} unrecognized")