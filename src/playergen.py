import random
from pathlib import Path
import sqlite3
import checkfile
import rewrite as re 

first_names = [
	"Aaron", "Abel", "Adrian", "Ahmed", "Alejandro", "Alex", "Alexander", "Alfredo", "Ali", "Amadou",
	"Ander", "Andre", "Andres", "Angel", "Antonio", "Arda", "Arthur", "Asier", "Augusto", "Axel",
	"Benjamin", "Bernardo", "Brahim", "Bruno", "Bukayo", "Callum", "Carlos", "Cesar", "Christian", "Christopher",
	"Ciro", "Cole", "Cristian", "Cristiano", "Dani", "Danilo", "David", "Dejan", "Denis", "Diego",
	"Dominic", "Dusan", "Eden", "Ederson", "Eduardo", "Elliot", "Emil", "Enzo", "Eric", "Erling",
	"Ethan", "Evan", "Fabian", "Federico", "Felipe", "Ferran", "Florian", "Francesco", "Francisco", "Gabriel",
	"Gavi", "Georginio", "Gerard", "Gianluca", "Giovanni", "Goncalo", "Granit", "Harry", "Hector", "Hugo",
	"Ibrahima", "Inaki", "Isco", "Ivan", "Jack", "James", "Jamie", "Jadon", "Jamal", "Jan",
	"Javier", "Jayden", "Joao", "Joel", "Johan", "John", "Jonathan", "Jorge", "Josko", "Jude",
	"Julian", "Kaka", "Kai", "Karim", "Kevin", "Kieran", "Kingsley", "Kylian", "Lautaro", "Lee",
	"Leon", "Leroy", "Liam", "Lionel", "Lorenzo", "Lucas", "Luis", "Luka", "Manuel", "Marc",
	"Marco", "Mario", "Martin", "Mason", "Matheus", "Matteo", "Matthew", "Memphis", "Michail", "Michael",
	"Mohamed", "Nabil", "Nani", "Neymar", "Nicolo", "Nicolas", "Noah", "Nuno", "Olivier", "Omar",
	"Oscar", "Ousmane", "Pablo", "Paulo", "Pedri", "Phil", "Pierre", "Rafael", "Raheem", "Randal",
	"Raphael", "Rasmus", "Richarlison", "Riyad", "Rodri", "Rodrigo", "Ruben", "Ryan", "Sadio", "Samuel",
	"Sandro", "Saul", "Scott", "Serge", "Sergio", "Simon", "Son", "Stefan", "Stefano", "Tariq",
	"Theo", "Thiago", "Thomas", "Timothy", "Toni", "Trent", "Tyler", "Victor", "Vinicius", "Virgil",
	"Vitor", "Wesley", "Wilfried", "William", "Xavi", "Yannick", "Youssef", "Zlatan", "Zeki", "Zinedine",
	"Abdoulaye", "Adama", "Alessandro", "Alexis", "Alvaro", "Andriy", "Ansu", "Armando", "Benjamin", "Boubacar",
	"Bryan", "Darwin", "Denzel", "Donyell", "Dylan", "Emmanuel", "Fikayo", "Gareth", "Iker", "Ismael",
	"Jeremie", "Joey", "Jonas", "Josip", "Kenneth", "Leandro", "Malik", "Mikel", "Moussa", "Ryan"
]

last_names = [
	"Adams", "Aguero", "Alaba", "Alonso", "Anderson", "Arnold", "Azpilicueta", "Bale", "Barella", "Bellingham",
	"Benzema", "Bernardo", "Boateng", "Bonucci", "Brandt", "Bruno", "Cancelo", "Casemiro", "Cavani", "Chilwell",
	"Chiesa", "Coman", "Conte", "Courtois", "Coutinho", "Cucurella", "Davis", "De Bruyne", "De Gea", "Dembele",
	"Dias", "Digne", "Donnarumma", "Drogba", "Dumfries", "Ederson", "Eriksen", "Estevao", "Evans", "Fabinho",
	"Foden", "Fofana", "Frimpong", "Gakpo", "Gavi", "Gerrard", "Gibbs-White", "Gomez", "Grealish", "Griezmann",
	"Guimaraes", "Hakimi", "Haaland", "Havertz", "Hernandez", "Herrera", "Hojlund", "Iniesta", "Isak", "James",
	"Kane", "Kante", "Kimmich", "Kluivert", "Kovacic", "Kroos", "Kulusevski", "Lahm", "Laporte", "Lewandowski",
	"Lloris", "Lozano", "Mane", "Marquinhos", "Martinez", "Mason", "Mata", "Mbappe", "McTominay", "Mendes",
	"Messi", "Militao", "Modric", "Mount", "Musiala", "Navas", "Neuer", "Nkunku", "Nunez", "Oblak",
	"Odegaard", "Onana", "Osimhen", "Palmer", "Paredes", "Pedri", "Pepe", "Perisic", "Pique", "Pogba",
	"Pulisic", "Rashford", "Rice", "Rivaldo", "Ronaldo", "Rooney", "Rudiger", "Saka", "Salah", "Saliba",
	"Sancho", "Silva", "Son", "Sterling", "Stones", "Suarez", "Szoboszlai", "Tchouameni", "Thiago", "Torres",
	"Trippier", "Umtiti", "Valverde", "Van Dijk", "Vardy", "Varane", "Vazquez", "Veratti", "Vinicius", "Walker",
	"Wirtz", "Yamal", "Zaha", "Zidane", "Ziyech", "Zouma", "Ake", "Alvarez", "Amrabat", "Anguissa",
	"Bastoni", "Bissouma", "Brozovic", "Calhanoglu", "Camavinga", "Carvajal", "Castagne", "Ceballos", "Clauss", "Colwill",
	"Darder", "De Ligt", "Dybala", "Elanga", "En-Nesyri", "Fati", "Fernandes", "Gundogan", "Gusto", "Ings",
	"Kamada", "Keane", "Kounde", "Kvaratskhelia", "Lavia", "Locatelli", "Maddison", "Maguire", "Mahrez", "Maignan",
	"Malen", "Milik", "Mitoma", "Morata", "Muriel", "Nketiah", "Partey", "Pavard", "Pellegrini", "Rabiot",
	"Reguilon", "Reus", "Riquelme", "Rogers", "Romero", "Sabitzer", "Savic", "Schick", "Shaw", "Skhiri",
	"Solanke", "Szoboszlai", "Tagliafico", "Tomori", "Tonali", "Trossard", "Upamecano", "Vlahovic", "Ward-Prowse", "Zubimendi"
]


# player appending to sqlite3 and generating random names and stats
root = Path(__file__).resolve().parent
def populate():
    data = checkfile.read(root/"config"/"saved.json")
    if data.get("saved") == True:
        print("save already created")
        return
    else:
        player_list = []
        for i in range(200):
            player_list.append(f"{first_names[i]} {last_names[i]}")
        print(player_list)
        conn = sqlite3.connect(root/"config"/"players.db")
        cursor = conn.cursor()
        position_dict = {
            "GK":0,
            "CB":0,
            "LB":0,
            "RB":0,
            "CM":0,
            "CAM":0,
            "LM":0,
            "RM":0,
            "LW":0,
            "RW":0,
            "ST":0
        }
        new_player_list = []
        for player in player_list:
            dict_keys = list(position_dict.keys())
            position = random.choice(dict_keys)
            while position_dict[position] >= 18:
                position = random.choice(dict_keys)
                position_dict[position] += 1
            print(position_dict)
            pace , shooting, passing, dribbling, defending, physical = random.randint(50, 100), random.randint(50, 100), random.randint(50, 100), random.randint(50, 100), random.randint(50, 100), random.randint(50, 100)
            ovr = (pace + shooting + passing + dribbling + defending + physical) // 6
            
            player_dict = {
                "name": player,
                "position": position,
                "pace": pace,
                "shooting": shooting,
                "passing": passing,
                "dribbling": dribbling,
                "defending": defending,
                "physical": physical,
                "ovr": ovr
            }
            new_player_list.append(player_dict)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
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
        for player in new_player_list:
            cursor.execute(f''' INSERT INTO players (name, position, pace, shooting, passing, dribbling, defending, physical, ovr) VALUES (?,?,?,?,?,?,?,?,?) ''', (player["name"], player["position"], player["pace"], player["shooting"], player["passing"], player["dribbling"], player["defending"], player["physical"], player["ovr"]))

        
        conn.commit()
        re.write(root/"config"/"saved.json", {"saved":True})

