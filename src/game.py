import transfermarket
import random
import sqlite3
import checkfile
import rewrite as re
from transfermarket import reformat_tuple_list
from pathlib import Path
root = Path(__file__).resolve().parent

conn = sqlite3.connect(root/"config"/"players.db")
cursor = conn.cursor()



class Player:
    def __init__(self, id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value):
        self.name = name
        self.position = position
        self.pace = pace
        self.shooting = shooting
        self.passing = passing
        self.dribbling = dribbling
        self.defending = defending
        self.physical = physical
        self.ovr = ovr
        self.value = value


class Team:
    def __init__(self, team_objects):
        self.team_objects = team_objects



def init_player_obj():
    cursor.execute('''SELECT * FROM starting_eleven''')
    eleven = reformat_tuple_list(cursor.fetchall())
    obj_list = []
    for player in eleven:
        player_obj = Player(player.get("id"),player.get("name"),player.get("position"),player.get("pace"), player.get("shooting"),player.get("passing"),player.get("dribbling"),player.get("defending"), player.get("physical"), player.get("ovr"), player.get("value"))
        obj_list.append(player_obj)
    team_obj = Team(obj_list)
    return team_obj

