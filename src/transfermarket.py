import random
import checkfile
import sqlite3
import rewrite as re
from pathlib import Path

root = Path(__file__).resolve().parent

def reformat_tuple_list(list_tuple_players:list) -> dict:
    player_list = []
    
    for player_tuple in list_tuple_players:
        player_dict = {
            "id":player_tuple[0],
            "name":player_tuple[1],
            "position":player_tuple[2],
            "pace":player_tuple[3],
            "shooting":player_tuple[4],
            "passing":player_tuple[5],
            "dribbling":player_tuple[6],
            "defending":player_tuple[7],
            "physical":player_tuple[8],
            "ovr":player_tuple[9],
            "value":player_tuple[10],
            "fitness":player_tuple[11],
            "club":player_tuple[12]

        }
        player_list.append(player_dict)
    return player_list

def show_transfer_market():
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()

    cursor.execute('''

    SELECT id FROM starting_eleven


''')
    all_players = cursor.fetchall()
    id_list_data = [spec_id[0] for spec_id in all_players]
    print(id_list_data)
    cursor.execute('''
    SELECT * FROM players

''')
    databse = reformat_tuple_list(cursor.fetchall())
    already = []
    for player in databse:
        if player.get("id") in id_list_data:
            already.append(player)
            print(f"{player.get("name")} removed from base.")
    for player in already:
        databse.remove(player)
    conn.close()
    return databse

def search(element):
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM starting_eleven''')
    id_list = [element[0] for element in cursor.fetchall()]
    cursor.execute('''SELECT * FROM players''')
    all_players = reformat_tuple_list(cursor.fetchall())
    search_dict = []
    for players in all_players:
        if element.lower() in players.get("name").lower():
            if players.get("id") in id_list:
                pass
            else:
                search_dict.append(players)
    conn.close()
    return search_dict


def find_in_eleven(player_to_buy):
    conn = sqlite3.connect(root/'config'/"players.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM starting_eleven''')
    all_players = reformat_tuple_list(cursor.fetchall())
    for players in all_players:
        if players.get('position') == player_to_buy.get('position'):
            print(players)
            conn.close()
            return players
    conn.close()

def rotate(player, reciprocate):
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM starting_eleven WHERE id=?",
        (reciprocate["id"],)
    )
    cursor.execute(f'''INSERT INTO "{player["club"]}" (id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness,club) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)''',
                            (reciprocate["id"],
                            reciprocate["name"],
                            reciprocate["position"],
                            reciprocate["pace"],
                            reciprocate["shooting"],
                            reciprocate["passing"],
                            reciprocate["dribbling"],
                            reciprocate["defending"],
                            reciprocate["physical"],
                            reciprocate["ovr"],
                            reciprocate["value"],
                            reciprocate["fitness"],
                            player["club"]))
    cursor.execute('''INSERT INTO starting_eleven 
                    (id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness,club)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)''',
                    (
                        player["id"],
                        player["name"],
                        player["position"],
                        player["pace"],
                        player["shooting"],
                        player["passing"],
                        player["dribbling"],
                        player["defending"],
                        player["physical"],
                        player["ovr"],
                        player["value"],
                        player["fitness"],
                        "starting_eleven"
                    ))
    cursor.execute("DELETE FROM players WHERE id=?", (reciprocate["id"],))
    cursor.execute("DELETE FROM players WHERE id=?", (player["id"],))
    cursor.execute("INSERT INTO players SELECT * FROM starting_eleven WHERE id=?", (player["id"],))
    cursor.execute(f'''INSERT INTO players SELECT * FROM "{player["club"]}" WHERE id=?''', (reciprocate["id"],))
    conn.commit()
    conn.close()
    

def return_pos(position):
        conn = sqlite3.connect(root/"config"/"players.db")
        cursor = conn.cursor()
        if position != "all positions":
            
            cursor.execute('''SELECT * FROM starting_eleven''')
            starting_eleven = reformat_tuple_list(cursor.fetchall())

            cursor.execute('''SELECT * FROM players WHERE position=?''', (position,))
            related_players = reformat_tuple_list(cursor.fetchall())
            already = []
            for player in related_players:
                if player in starting_eleven:
                    print(related_players)
                    already.append(player)
                    print(f"{player.get("name")} removed from specialized base.")
            for player in already:
                related_players.remove(player)
            conn.close()
            return related_players
        else:
            cursor.execute('''SELECT * FROM players''')
            full_list = reformat_tuple_list(cursor.fetchall())
            conn.close()
            return full_list
