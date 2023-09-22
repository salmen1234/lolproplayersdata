from settings import DATAJSON_PATH
import json

def get_average_age(console: bool = True):
    players = None
    
    with open(DATAJSON_PATH, "r", encoding="utf-8") as file:
        players = json.load(file)[0]["players"]
    
    full_ages = 0

    for player in players:
        age = player["age"]  
            
        full_ages += int(age)
        
    if console == True:
        print(f"\n>> Fetching average age for {len(players)} players")
        
    average_age = round(full_ages / (len(players)))
    
    return average_age

def get_average_earnings(console: bool = True):      
    players = None
    
    with open(DATAJSON_PATH, "r", encoding="utf-8") as file:
        players = json.load(file)[0]["players"]
    
    earnings = 0

    for player in players:
        earn = player["careerEarnings"]  
            
        earnings += int(earn.replace("$", "").replace(",", ""))
        
    if console == True:
        print(f"\n>> Fetching average earnings for {len(players)} players")
            
    average = round(earnings / (len(players)))
    formatted_number = '{:,}'.format(average)
         
    average_earnings = f"${formatted_number}"
    
    return average_earnings

print(get_average_earnings())