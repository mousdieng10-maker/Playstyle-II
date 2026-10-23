import random
from pathlib import Path
import sqlite3
import checkfile
import rewrite as re 
import generateplayers
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
	"Jeremie", "Joey", "Jonas", "Josip", "Kenneth", "Leandro", "Malik", "Mikel", "Moussa", "Ryan",
	"Abraham", "Achraf", "Adrian", "Afonso", "Agustin", "Aitor", "Alberto", "Aleix", "Alessio", "Amine",
	"Anatoliy", "Andreas", "Andrej", "Antoine", "Arijanet", "Arnaut", "Ashley", "Aurelien", "Baptiste", "Bastian",
	"Benjamin", "Benoit", "Bilal", "Bobby", "Bradley", "Breel", "Caglar", "Casper", "Cesc", "Cheick",
	"Chidera", "Claudio", "Conor", "Cyril", "Daniil", "Dario", "Dele", "Dominik", "Duncan", "Edin",
	"Eljif", "Ellyes", "Enes", "Enock", "Eray", "Ethan", "Evan", "Fabio", "Faustino", "Federico",
	"Felix", "Fermin", "Fernando", "Filip", "Franck", "Franco", "Gabriel", "Garang", "Gianluigi", "Giorgio",
	"Giovani", "Goncalo", "Grady", "Guillermo", "Hakan", "Hamari", "Hannibal", "Harvey", "Heung-Min", "Hugo",
	"Ilaix", "Iliman", "Ismael", "Jamal", "Jarrad", "Javi", "Jhon", "Jo", "Jordan", "Jorginho",
	"Joselu", "Juan", "Julio", "Jurrien", "Kacper", "Kamil", "Karlo", "Kasey", "Kelechi", "Kenny",
	"Khvicha", "Koke", "Konrad", "Lamine", "Lazar", "Leonardo", "Lewis", "Luka", "Maarten", "Malo",
	"Marcelo", "Marcos", "Marquinhos", "Martial", "Mateo", "Mathys", "Max", "Maxence", "Mehdi", "Mikayil",
	"Mohammed", "Morgan", "Nicolas", "Nicolai", "Nico", "Odilon", "Oliver", "Orkun", "Pau", "Pedro",
	"Quentin", "Rayan", "Renato", "Rico", "Roberto", "Romain", "Samu", "Sebastian", "Sehrou", "Shinji",
	"Stefan", "Sven", "Tanguy", "Tarek", "Teun", "Thilo", "Tim", "Tom", "Wahbi", "Wilfred",
	"Xherdan", "Yacine", "Yangel", "Yann", "Yehor", "Yunus", "Zeki", "Zekiye", "Zeno", "Zian",
	"Abner", "Adil", "Ainsley", "Alfie", "Amadou", "Anderson", "Anwar", "Armando", "Bafode", "Bartosz",
	"Calvin", "Cameron", "Clement", "Dawid", "Eberechi", "Emerson", "Facundo", "Florentino", "Gerson", "Giuliano",
	"Halil", "Ibrahim", "Jean", "Jesper", "Kurt", "Lukas", "Mats", "Nacer", "Orel", "Piero",
	"Rafinha", "Salvatore", "Timo", "Valentin", "Wataru", "Yuki", "Zeki", "Abdou", "Boubacar", "Cheick",
	"Diego", "Elias", "Francisco", "Gustavo", "Ibrahim", "Joaquin", "Khalil", "Lorenzo", "Mohamed", "Nicolas",
	"Osman", "Patson", "Rafael", "Santiago", "Thierry", "Umar", "Victor", "Xavier", "Yuri", "Zayd"
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
	"Solanke", "Szoboszlai", "Tagliafico", "Tomori", "Tonali", "Trossard", "Upamecano", "Vlahovic", "Ward-Prowse", "Zubimendi",
	"Aboubakar", "Acerbi", "Ait-Nouri", "Akanji", "Akpom", "Almiron", "Andrich", "Andre", "Asensio", "Aubameyang",
	"Bailey", "Bakker", "Baldock", "Bamford", "Barcola", "Bard", "Barnes", "Bassey", "Baturina", "Bellerin",
	"Berardi", "Bergwijn", "Beto", "Boly", "Borja", "Boufal", "Boulaye", "Boye", "Bremer", "Broja",
	"Bueno", "Buendia", "Cairney", "Calvert-Lewin", "Capoue", "Castro", "Cavaminga", "Chukwueze", "Coady", "Correa",
	"Cristante", "Daka", "Daland", "Danjuma", "Darmian", "Dawson", "Delaney", "Dendoncker", "Deulofeu", "Dewsbury-Hall",
	"Diaby", "Dier", "Doku", "Doucoure", "Doyle", "Duran", "Emerson", "Eze", "Ferguson", "Fofana",
	"Gallagher", "Garnacho", "Gibbs", "Gilmour", "Giroud", "Godfrey", "Gomes", "Gordon", "Guehi", "Gvardiol",
	"Gyokeres", "Henderson", "Hickey", "Hincapie", "Hojbjerg", "Holgate", "Hutchinson", "Iwobi", "Jorgensen", "Kalajdzic",
	"Kamada", "Kamada", "Kessie", "Kluivert", "Kone", "Kudus", "Lallana", "Lemar", "Lerma", "Lindelof",
	"Livramento", "Lo Celso", "Lukaku", "Lukebakio", "Mane", "Marmoush", "Mateta", "Mavididi", "McGinn", "Meite",
	"Merino", "Mings", "Moffi", "Monreal", "Morris", "Mudryk", "Murillo", "Ndombele", "Nmecha", "Norgaard",
	"Olise", "Onyeka", "Openda", "Paqueta", "Pavard", "Pedro", "Pereira", "Petrovic", "Pino", "Pinnock",
	"Ramsey", "Rashica", "Raya", "Ream", "Rensch", "Retegui", "Richards", "Rincon", "Roca", "Rodon",
	"Rutter", "Sangare", "Sarr", "Savio", "Scamacca", "Schade", "Schlotterbeck", "Sensi", "Shaqiri", "Simakan",
	"Sinisterra", "Smalling", "Soucek", "Stanisic", "Stankovic", "Summerville", "Sutalo", "Taremi", "Theate", "Tielemans",
	"Udogie", "Undav", "Vazquez", "Veiga", "Veretout", "Walker-Peters", "Weghorst", "Werner", "White", "Willock",
	"Wilson", "Yates", "Zaniolo", "Zaroury", "Zinchenko", "Aarons", "Abraham", "Ait-Nouri", "Almada", "Amadou",
	"Arnautovic", "Aursnes", "Badiashile", "Bailly", "Bakayoko", "Balde", "Bamba", "Benzia", "Berge", "Bernat",
	"Beundia", "Bissaka", "Bonaventura", "Borges", "Borre", "Boufal", "Brahimi", "Cacace", "Cambiasso", "Carmo",
	"Carrasco", "Casteels", "Cervi", "Chalobah", "Cherki", "Chukwueze", "Cisse", "Colak", "Corluka", "Cunha",
	"Danilo", "Dendoncker", "Djalo", "Dumfries", "Elmas", "Embolo", "Estupinan", "Fares", "Fellaini", "Fresneda",
	"Gerson", "Gouiri", "Gravenberch", "Guendouzi", "Haller", "Hwang", "Isco", "Joao Mario", "Kabak", "Kamada",
	"Karsdorp", "Kimpembe", "Kostic", "Lazovic", "Malen", "Mandragora", "Maripan", "Milenkovic", "Milenkovic-Savic", "Mina",
	"Ndicka", "Nianzou", "Paredes", "Pellegrini", "Pirola", "Politano", "Rrahmani", "Sanches", "Singo", "Skov Olsen"
]


# player appending to sqlite3 and generating random names and stats
root = Path(__file__).resolve().parent
def populate():
    data = checkfile.read(root/"config"/"saved.json")
    if data.get("saved") == True:
        print("save already created")
        return
    elif data.get("saved") == False:
        player_list = []
        for i in range(396):
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
        dict_keys = list(position_dict.keys())
        def check_pos():
            availalable_positions = [pos for pos in dict_keys if position_dict[pos] < 36]
            try:
                position = random.choice(availalable_positions)
            except IndexError:
                position = random.choice(dict_keys)
            position_dict[position] += 1
            return position
        for player in player_list:
            player_position = check_pos()
            
            
            print(position_dict)
            player_dict = {
                            "name": player,
                            "position": player_position,
                            "pace": 0,
                            "shooting": 0,
                            "passing": 0,
                            "dribbling": 0,
                            "defending": 0,
                            "physical": 0,
                            "ovr": 0,
                            "value":0,
                            "fitness": 100
                        }
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
            ind_weight = weights[player_position]
            stats = ["pace", "shooting", "passing", "dribbling", "defending", "physical"]
            for weight, stat in zip(ind_weight, stats):
                mean = round(63 + 7.5*weight)
                value = round(random.gauss(mean, 13))
                if value < 50:
                    value = 50
                elif value > 99:
                    value = 99
                player_dict[stat] = value
            stats_values = [player_dict.get("pace"), player_dict.get("shooting"), player_dict.get("passing"), player_dict.get("dribbling"), player_dict.get("defending"), player_dict.get("physical")]
            full_amount = sum(stats_values)
            player_dict["ovr"] = round(full_amount/6)
            fovr = player_dict["ovr"]
            player_dict["value"] = round(1000000*fovr + 10**(fovr-(fovr-2)+(fovr/15)))

            
            new_player_list.append(player_dict)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
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
        incr = 1
        for player in new_player_list:
            cursor.execute(f''' INSERT INTO players (id, name, position, pace, shooting, passing, dribbling, defending, physical, ovr, value, fitness) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''', (incr, player["name"], player["position"], player["pace"], player["shooting"], player["passing"], player["dribbling"], player["defending"], player["physical"], player["ovr"], player["value"], player["fitness"]))
            incr +=1 
        
        conn.commit()
        re.write(root/"config"/"saved.json", {"saved":True, "budget":1500000})
        conn.close()
