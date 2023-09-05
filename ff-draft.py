import os
import requests
import xml.etree.ElementTree as ET

class Player:
    def __init__(self, rank=None, points=None, name: str=None, team=None, bye=None, defense=False):
        self.rank = rank
        self.points = points
        if not defense and ", " not in name:
            name_list = name.split(" ")
            name_list.reverse()
            self.name = ", ".join(name_list)
        else:
            self.name = name
        self.team = team
        self.bye = bye

    def __repr__(self) -> str:
        return f"{self.rank} {self.name} {self.points} {self.team} {self.bye}"
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

USER = os.getenv("FF_USER")
PASSWORD = os.getenv("FF_PASSWORD")

LEAGUE_ID = "74603"
API_URL = "https://api.myfantasyleague.com/2023"
CONFIG_PATH = 'config.txt'
PLAYER_DATA_PATH = "player-data.xml"

def parse_pasted_huddle_data():
    positions = ["QUARTERBACKS", "KICKERS", "RUNNING BACKS" , "DEFENSE", "WIDE RECEIVERS + TIGHT ENDS"]
    current_position = ""
    position_dict = {}
    with open("huddle-data.txt", "r") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            if line in positions:
                current_position = line
                position_dict[current_position] = []
                next(f)
            else:
                line1 = line.strip().split("\t")
                line = next(f)
                line2 = line.strip().split("\t")
                position_dict[current_position].append(Player(*line1, *line2, current_position == "DEFENSE"))
    return position_dict

def login():
    if os.path.exists(f"./{CONFIG_PATH}"):
        print("already have mfl user id")
        with open(CONFIG_PATH, "r") as f:
            return {"MFL_USER_ID": f.readline().strip()}
    print("attempting to login")
    login_url = f"{API_URL}/login?USERNAME={USER}&PASSWORD={PASSWORD}&XML=1"
    resp = requests.post(login_url)
    print(f"login response: {resp}")
    with open(CONFIG_PATH, "a") as f:
        f.write(ET.fromstring(resp.content).attrib["MFL_USER_ID"])
    return {"MFL_USER_ID": ET.fromstring(resp.content).attrib["MFL_USER_ID"]}

def get_player_info(cookies):
    if os.path.exists(f"./{PLAYER_DATA_PATH}"):
        print("already have player data")
        return
    print("attempting to get player data")
    url = f"{API_URL}/export?TYPE=players&L={LEAGUE_ID}"
    resp = requests.post(url, cookies=cookies)
    print(f"player data response: {resp}")
    with open(PLAYER_DATA_PATH, "a") as f:
        f.write(resp.content.decode())

def get_draft_data(cookies):
    print("attempting to get draft data")
    url = f"{API_URL}/export?TYPE=draftResults&L={LEAGUE_ID}"
    resp = requests.post(url, cookies=cookies)
    print(f"draft data response {resp}")

    tree = ET.parse(PLAYER_DATA_PATH)
    root = tree.getroot()

    draft_data = ET.fromstring(resp.content)
    drafted_players = []
    for player_tag in draft_data.findall(".//draftPick[@player!='']"):
        p = root.find(f'player[@id=\'{player_tag.attrib["player"]}\']')
        drafted_players.append(Player(name=p.attrib['name']))
    return drafted_players


if __name__ == "__main__":
    position_dict = parse_pasted_huddle_data()
    # print(position_dict)
    login_cookie = login()
    get_player_info(login_cookie)
    drafted_players = get_draft_data(login_cookie)
    for position, players in position_dict.items():
        print(position)
        for p in [p for p in players if Player(name=p.name) not in drafted_players][:10]:
            print(p)
