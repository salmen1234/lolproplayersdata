import json
from liquipedia import get_player_urls, get_player_informations
from settings import CONSOLE

def write_player(path: str, playerInformations):
    try:
        with open(path, "r", encoding="utf-8") as file:
            old_json = json.load(file)
    except FileNotFoundError:
        old_json = [{"players": []}]
    
    new_player = {
        "name": playerInformations["name"],
        "age": playerInformations["age"],
        "nation": playerInformations["nation"],
        "status": playerInformations["status"],
        "team": playerInformations["team"],
        "role": playerInformations["role"],
        "careerEarnings": playerInformations["earnings"],
    }
    
    if "players" not in old_json[0]:
        old_json[0]["players"] = []
        
    old_json[0]["players"].append(new_player)
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(old_json, file, indent=4, ensure_ascii=False)
        
def write_data_json(path: str):
    data = {"players": []}
    
    plrs_url = get_player_urls(console=CONSOLE)
    
    for plr_url in plrs_url:
        plr_info = get_player_informations(plr_url)
        
        if plr_info:
            data["players"].append(plr_info)
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump([data], file, indent=4, ensure_ascii=False)