import json
from pathlib import Path
import sqlite3
import random
import checkfile
import rewrite as re

root = Path(__file__).resolve().parent


def select_team_first_time():
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    full_player_database = cursor.fetchall()
    reformatted_list = []
    position_list = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "ST"]
    for player_tuple in full_player_database:
        player_dict = {
            "id": player_tuple[0],
            "name": player_tuple[1],
            "position": player_tuple[2],
            "pace": player_tuple[3],
            "shooting": player_tuple[4],
            "passing": player_tuple[5],
            "dribbling": player_tuple[6],
            "defending": player_tuple[7],
            "physical": player_tuple[8],
            "ovr": player_tuple[9]
        }
        reformatted_list.append(player_dict)
    player_list = []
    def check_is_there(playing:list, database:list):
        player_to_add = random.choice(playing)
        if player_to_add["position"] in database:
            database.remove(player_to_add["position"])
            player_list.append(player_to_add)
        else:
            check_is_there(playing, database)

    for i in range(11):
        check_is_there(reformatted_list, position_list)


    cursor.execute('''CREATE TABLE IF NOT EXISTS starting_eleven 
                
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    pace INTEGER NOT NULL,
                    shooting INTEGER NOT NULL,
                    passing INTEGER NOT NULL,
                    dribbling INTEGER NOT NULL,
                    defending INTEGER NOT NULL,
                    physical INTEGER NOT NULL,
                    ovr INTEGER NOT NULL
                    )
               
                    ''')  
    for starters in player_list:
        
        cursor.execute(f''' INSERT INTO starting_eleven (name, position, pace, shooting, passing, dribbling, defending, physical, ovr) VALUES (?,?,?,?,?,?,?,?,?) ''', (starters["name"], starters["position"], starters["pace"], starters["shooting"], starters["passing"], starters["dribbling"], starters["defending"], starters["physical"], starters["ovr"]))
    conn.commit()
    return player_list


select_team_first_time()