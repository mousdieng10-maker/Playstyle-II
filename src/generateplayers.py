import json
from pathlib import Path
import sqlite3
import random
import checkfile
import rewrite as re
import playergen
root = Path(__file__).resolve().parent


def select_team_first_time():
    from transfermarket import reformat_tuple_list
    
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    full_player_database = cursor.fetchall()
    reformatted_list = []
    position_list = ["GK", "CB", "LB", "RB", "CM", "CAM", "LM", "RM", "LW", "RW", "ST"]
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
            "ovr": player_tuple[9],
            "value":player_tuple[10],
            "fitness":player_tuple[11]
        }
        reformatted_list.append(player_dict)

    player_list = []
    def check_is_there(playing:list, database:list):
        player_to_add = random.choice(playing)
        if player_to_add["position"] in database:
            database.remove(player_to_add["position"])
            player_list.append(player_to_add)
            return player_to_add
        else:
            return check_is_there(playing, database)

    for i in range(11):
        check_is_there(reformatted_list, position_list)


    cursor.execute('''CREATE TABLE IF NOT EXISTS starting_eleven 
                
                    (
                    id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    pace INTEGER NOT NULL,
                    shooting INTEGER NOT NULL,
                    passing INTEGER NOT NULL,
                    dribbling INTEGER NOT NULL,
                    defending INTEGER NOT NULL,
                    physical INTEGER NOT NULL,
                    ovr INTEGER NOT NULL,
                    value INTEGER NOT NULL,
                    fitness INTEGER NOT NULL,
                    club TEXT
                    )
               
                    ''')  
    for starters in player_list:
        
        cursor.execute(f''' INSERT INTO starting_eleven (id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness, club) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ''', (starters["id"],starters["name"], starters["position"], starters["pace"], starters["shooting"], starters["passing"], starters["dribbling"], starters["defending"], starters["physical"], starters["ovr"], starters["value"], starters["fitness"], "starting_eleven"))
    new_list = player_list.copy()
    
    conn.commit()
    remainder_player = reformat_tuple_list(full_player_database)
    team_names = [
        "FC Javascript",
        "PHP United",
        "Python Nation",
        "C++ Saint Germain",
        "Rust Rovers",
        "Java City",
        "Ruby Athletic",
        "The Go Wanderers",
        "TypeScript Town",
        "Kotlin County",
        "Swift Albion",
        "Dartford FC",
        "Lua Lakes",
        "Perl City",
        "Fortran Forest",
        "Haskell Hotspur",
        "Scala Sporting",
        "Objective-C United",
        "Ruby on Rails FC",
        "Node.js Athletic",
        "React Rovers",
        "Angular City",
        "Vue United",
        "GitHub Wanderers",
        "Docker Town",
        "Linux Albion",
        "Ubuntu FC",
        "Fedora County",
        "Debian Dynamo",
        "Arch City",
        "Kubernetes FC",
        "Mongo City",
        "SQL Sporting",
        "Git United",
        "API Athletic",
    ]
    player_list = []
    immutable = [
        "FC Javascript",
        "PHP United",
        "Python Nation",
        "C++ Saint Germain",
        "Rust Rovers",
        "Java City",
        "Ruby Athletic",
        "The Go Wanderers",
        "TypeScript Town",
        "Kotlin County",
        "Swift Albion",
        "Dartford FC",
        "Lua Lakes",
        "Perl City",
        "Fortran Forest",
        "Haskell Hotspur",
        "Scala Sporting",
        "Objective-C United",
        "Ruby on Rails FC",
        "Node.js Athletic",
        "React Rovers",
        "Angular City",
        "Vue United",
        "GitHub Wanderers",
        "Docker Town",
        "Linux Albion",
        "Ubuntu FC",
        "Fedora County",
        "Debian Dynamo",
        "Arch City",
        "Kubernetes FC",
        "Mongo City",
        "SQL Sporting",
        "Git United",
        "API Athletic",
    ]
    cursor.execute('SELECT * FROM starting_eleven')
    everything = reformat_tuple_list(cursor.fetchall())
    everything_list = [player_id.get("id") for player_id in everything]
    team_list = []
    conclude_list = [every for every in remainder_player if every.get("id") not in everything_list]
    for i in range(35):
        pos_list = ["GK", "CB", "LB", "RB", "CM", "CAM", "LM", "RM", "LW", "RW", "ST"]
        name_of_team = random.choice(team_names)
        team_names.remove(name_of_team)
        players = [check_is_there(conclude_list,pos_list) for j in range(11)]
        conclude_list = [p for p in conclude_list if p not in players]
        teams_populate = {
            "name":name_of_team,
            "players":players
            }
            
                
        team_list.append(teams_populate)
    for team in team_list:
        teamname = team.get("name")
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS "{teamname}"
        
            (
            id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            pace INTEGER NOT NULL,
            shooting INTEGER NOT NULL,
            passing INTEGER NOT NULL,
            dribbling INTEGER NOT NULL,
            defending INTEGER NOT NULL,
            physical INTEGER NOT NULL,
            ovr INTEGER NOT NULL,
            value INTEGER NOT NULL,
            fitness INTEGER NOT NULL,
            club TEXT 
            
            )
        
''')    
        conn.commit()
        for player in team.get("players"):
            cursor.execute(f'''INSERT INTO "{teamname}" (id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness, club) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ''', (player["id"],player["name"], player["position"], player["pace"], player["shooting"], player["passing"], player["dribbling"], player["defending"], player["physical"], player["ovr"], player["value"], player["fitness"],teamname))
        conn.commit()
    cursor.execute('''DELETE FROM players''')
    for teams in immutable:
        cursor.execute(f'''INSERT INTO players SELECT * FROM "{teams}"''')
    cursor.execute(f'''INSERT INTO players SELECT * FROM starting_eleven''')
    conn.commit()


        
    conn.close()
    return new_list
