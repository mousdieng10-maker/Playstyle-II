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
            "value":player_tuple[10]

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
    cursor.execute('''
    SELECT * FROM players

''')
    databse = reformat_tuple_list(cursor.fetchall())
    for player in databse:
        if player.get("id") in id_list_data:
            databse.remove(player)
            print(f"{player.get("name")} removed from base.")
    return databse

def search(element):
    conn = sqlite3.connect(root/"config"/"players.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM players''')
    all_players = reformat_tuple_list(cursor.fetchall())
    search_dict = []
    for players in all_players:
        if element.lower() in players.get("name").lower():
            search_dict.append(players)
    return search_dict


