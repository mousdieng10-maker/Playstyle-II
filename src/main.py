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
                    "ovr": player[9],
                    "value": player[10]
                }
                all_players.append(player_dict)
            return all_players
        else:
            
            starting_eleven  = select_team_first_time()
            data["saved"] = True
            re.write(root/"config"/"saved.json", data)
            return starting_eleven

    def define_cards(self):
        full_team = self.generate_team()
        for player in full_team:
            ovr = player["ovr"]
            if 50 <= ovr < 65:
                player_link = "assets/bronzeCard_transparent.png"
            elif 65 <= ovr < 80:
                player_link = "assets/goldCard_transparent.png"
            elif 80 <= ovr < 89:
                player_link = "assets/diamondCard_transparent.png"
            elif 89 <= ovr <= 99:
                player_link = "assets/rubyCard_transparent.png"
            else:
                player_link = ""

            player["link"] = player_link
        print(full_team)
        return full_team 
    def show_all_players(self):
        import transfermarket

        all_players = transfermarket.show_transfer_market() 
        return all_players
    def give_player_stats(self, player_dict):
        stats_dict = {
            "pace": player_dict.get("pace"),
            "shooting": player_dict.get("shooting"),
            "passing": player_dict.get("passing"),
            "dribbling": player_dict.get("dribbling"),
            "defending": player_dict.get("defending"),
            "physical": player_dict.get("physical"),
        }
        return stats_dict
    def find(self, letters):
        import transfermarket
        return transfermarket.search(letters)
    def return_budget(self):
        data = checkfile.read(root/"config"/"saved.json")
        return data.get("budget")
    def selling(self, player_dict):
        import transfermarket
        recip_starter = transfermarket.find_in_eleven(player_dict)

        return recip_starter
    def find_budget(self):
        data = checkfile.read(root/"config"/"saved.json")
        budget = data.get("budget")
        return budget
    def sell_player(self, player, reciprocate):
        import transfermarket
        transfermarket.rotate(player, reciprocate)
        


api = Api()

window = webview.create_window("Offside I",str(absolute_root/"app"/"index.html"), js_api=api)
webview.start(debug=True)