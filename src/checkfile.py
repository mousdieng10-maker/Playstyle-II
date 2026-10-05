import json
from json import JSONDecodeError

def read(file):
    while True:
        try:
            with open(file, "r") as f:
                return json.load(f)
        except JSONDecodeError:
            with open(file,"w") as f:
                json.dump([], f, indent=4)
        except FileNotFoundError:
            print("File is not found, creating a new file.")
            open(file, "x")
        