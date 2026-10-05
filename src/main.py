import webview
from pathlib import Path
import rewrite
import checkfile
import sqlite3
import json
import playergen
from generateplayers import select_team_first_time

root = Path(__file__).resolve().parent
absolute_root = Path(__file__).resolve().parent.parent

print(root)
class Api():
    def __init__(self):
        pass
    def generate_team(self):
        data = checkfile.read(root/"config"/"saved.json")
        if data.get("saved") == True:
            pass
        else:
            starting_eleven  = select_team_first_time()
            return starting_eleven












api = Api()

window = webview.create_window("Offside I",str(absolute_root/"app"/"index.html"), js_api=api)
webview.start()