import time
import sys

def AOSPrint(value):
    print(f">> {value}")

def AOSLoad(value, endmessage, speed):
    Completion = 0
    while Completion != 100:
        sys.stdout.write(f"\r>> {value} ({Completion}%)")
        if speed == "Slow":
            time.sleep(0.1)
        elif speed == "Normal":
            time.sleep(0.01)
        elif speed == "Fast":
            time.sleep(0.001)
        else:
            time.sleep(0.1)
        Completion += 1
    sys.stdout.write(f"\r>> {endmessage} ({Completion}%)                           ")
    sys.stdout.write("\n")

def AOSInput(CaseSensitive):
    value = input(f"// ")
    if CaseSensitive != True:
        value = value.lower()
    return value