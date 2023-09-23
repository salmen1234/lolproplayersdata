import requests
from bs4 import BeautifulSoup

def get_most_played_champion(url: str):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "lxml")
    
    texts = soup.findAll("h3")

    if texts == None:
        return
    
    most_played = None

    for text in texts:
        if "Most Played Champion" in text.text:
            parent_div = text.parent

            champion_text = parent_div.findNext("div").text
            most_played = champion_text
        break

    return most_played

def get_champion_kills(url: str):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "lxml")

    spans = soup.findAll("span")

    def is_not_infocell(div):
            return "infobox-description" not in div.get("class", [])
    
    championsKills = None

    #TODO Retrieve champion kills
    for span in spans:
        if "Champion Kills" in span.text:
            parent_div = span.parent.parent
            
            all_child_divs = parent_div.findAll("div")
            other_child_divs = list(filter(is_not_infocell, all_child_divs))

            for div in other_child_divs:
                newChildDiv = div.find("div")

                championsKills = newChildDiv.find("span").text

    return championsKills