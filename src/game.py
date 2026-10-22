import transfermarket
import random
import sqlite3
import checkfile
import rewrite as re
from transfermarket import reformat_tuple_list
from pathlib import Path
root = Path(__file__).resolve().parent

class Player:
    def __init__(self, id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness):
        self.id = id
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
        self.fitness = fitness
    def train(self):
        stats_to_upg = ["pace","shooting","passing","dribbling","defending","physical"]
        weights = {
            "LW":[3,3,2,4,.5,1],
            "RW":[3,3,2,4,.5,1],
            "ST":[3,4,2,1.5,.3,2],
            "CAM":[1.5,3.5,3,2.3,.8,1],
            "CM":[1.5,1.5,3,2.5,2,2],
            "LM":[2,2,3,1.5,2,2],
            "RM":[2,2,3,1.5,2,2],
            "CB":[2,.3,.1,.5,4,3],
            "LB":[3,.5,1,1.5,3,2],
            "RB":[3,.5,1,1.5,3,2],
            "GK":[1,1,2,1,1,2]
        }
        weight_to_apply = weights.get(self.position)
        upg = random.choices(stats_to_upg, weights=weight_to_apply, k=1)[0]
        if self.fitness > 10:
            upgrade = random.choices([True, False], weights=[3,1], k=1)[0]
            if upgrade:
                setattr(self, upg, getattr(self, upg)+2)
                if getattr(self, upg) > 99:
                    setattr(self, upg, 99)
                    self.fitness -= 10
                    return f"+2 {upg}."
                
                return f"+2 {upg}."
            elif upgrade == False:
                self.fitness -= 15
                return f"{self.name}'s training sesh bore no fruits!"
            
        else:
            return f"{self.name} is too tired!"
    def calculate_ovr(self):
        weights = {
                    "LW":[3,3,2,4,.5,1],
                    "RW":[3,3,2,4,.5,1],
                    "ST":[3,4,2,1.5,.3,2],
                    "CAM":[1.5,3.5,3,2.3,.8,1],
                    "CM":[1.5,1.5,3,2.5,2,2],
                    "LM":[2,2,3,1.5,2,2],
                    "RM":[2,2,3,1.5,2,2],
                    "CB":[2,.3,.1,.5,4,3],
                    "LB":[3,.5,1,1.5,3,2],
                    "RB":[3,.5,1,1.5,3,2],
                    "GK":[1,1,2,1,1,2]
                }
        stats_to_upg = [self.pace,self.shooting,self.passing,self.dribbling,self.defending,self.physical]
        weight = weights.get(self.position)
        ovr_done = 0
        incr = 0
        for stat in stats_to_upg:
            ovr_done += stat * weight[incr]
            incr += 1
        self.ovr = round(ovr_done/sum(weight))


        

class Team:
    def __init__(self, team_objects):
        self.team_objects = team_objects



def init_player_obj():
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM starting_eleven''')
    eleven = reformat_tuple_list(cursor.fetchall())
    conn.close()
    obj_list = []
    for player in eleven:
        player_obj = Player(player.get("id"),player.get("name"),player.get("position"),player.get("pace"), player.get("shooting"),player.get("passing"),player.get("dribbling"),player.get("defending"), player.get("physical"), player.get("ovr"), player.get("value"), player.get("fitness"))
        obj_list.append(player_obj)
    team_obj = Team(obj_list)
    return team_obj



def save_players(classes):
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM starting_eleven")
    if classes != "":
        for player in classes.team_objects:
            cursor.execute('''INSERT INTO starting_eleven 
                                (id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)''',
                                (
                                    player.id,
                                    player.name,
                                    player.position,
                                    player.pace,
                                    player.shooting,
                                    player.passing,
                                    player.dribbling,
                                    player.defending,
                                    player.physical,
                                    player.ovr,
                                    player.value,
                                    player.fitness
                                ))
    conn.commit()
    conn.close()