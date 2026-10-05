import webview
from pathlib import Path
import rewrite as re
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
            conn = sqlite3.connect(root/"config"/"players.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM starting_eleven")
            starting_eleven = cursor.fetchall()
            all_players = []
            for player in starting_eleven:
                player_dict = {
                    "id": player[0],
                    "name": player[1],
                    "position": player[2],
                    "pace": player[3],
                    "shooting": player[4],
                    "passing": player[5],
                    "dribbling": player[6],
                    "defending": player[7],
                    "physical": player[8],
                    "ovr": player[9]
                }
                all_players.append(player_dict)
            return all_players
        else:
            
            starting_eleven  = select_team_first_time()
            data["saved"] = True
            re.write(root/"config"/"saved.json", data)
            return starting_eleven












api = Api()

window = webview.create_window("Offside I",str(absolute_root/"app"/"index.html"), js_api=api)
webview.start(debug=True)