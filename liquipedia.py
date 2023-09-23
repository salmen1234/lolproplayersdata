import requests
from bs4 import BeautifulSoup
import re
from factorgg import get_most_played_champion, get_champion_kills
from settings import BASE_URL

def get_player_urls(console: bool = True):
    urls = []
    
    res = requests.get("https://liquipedia.net/leagueoflegends/Portal:Players")

    soup = BeautifulSoup(res.text, "lxml")

    boxes = soup.findAll("div", {"class": "template-box"})

    for box in boxes:
        ul = box.select("ul")[0]
        
        for li in ul.findAll("li"):            
            spans = li.find_all("span")
            if len(spans) >= 2:
                second_span = spans[1]
                href = second_span.find("a")["href"]

                url = BASE_URL+href           
                if console == True:
                    print(">> Fetching url..")
                    print(url)
                    print("------------------------------------")
                urls.append(url)
                
    print("Urls fetched successfully")
    return urls

def get_player_informations(url: str, playerNumber: int, console: bool = True, number: int = 0):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text, "lxml")
    infocells = soup.findAll("div", {"class": "infobox-cell-2 infobox-description"})
    informations = {"team": None} 
    username = soup.find("span", {"dir": "auto"}).text

    for infocell in infocells:
        text = infocell.get_text(strip=True)
        parent_div = infocell.parent
        all_child_divs = parent_div.find_all("div")
        
        def is_not_infocell(div):
            return "infobox-description" not in div.get("class", [])
        
        other_child_divs = list(filter(is_not_infocell, all_child_divs))

        if text == "Born:":
            for child_div in other_child_divs:
                age_text = child_div.get_text(strip=True)
                age = re.findall(r'\d+', age_text).pop()
                informations["age"] = age
        elif text == "Name:":
            for child_div in other_child_divs:
                name_text = child_div.get_text(strip=True)
                informations["name"] = name_text
        elif text == "Nationality:":
            for child_div in other_child_divs:
                nation_text = child_div.find("a").get("title")
                informations["nation"] = nation_text
        elif text == "Status:":
            for child_div in other_child_divs:
                status_text = child_div.get_text(strip=True)
                informations["status"] = status_text
        elif text == "Team:":
            team_text = parent_div.find("a")
            if team_text:
                informations["team"] = team_text.get_text(strip=True)
            else:
                informations["team"] = "None"
        elif text == "Romanized Name:":
            for child_div in other_child_divs:
                name_text = child_div.get_text(strip=True)
                informations["name"] = name_text
        elif text == "Role:":
            for child_div in other_child_divs:
                role_text = child_div.find("a").text
                
            informations["role"] = role_text
        elif text == "Approx. Total Winnings:":
            for child_div in other_child_divs:
                earns_text = child_div.text
                
            informations["careerEarnings"] = earns_text
            
    informations["wonTournaments"] = get_won_tournaments(url)
    informations["username"] = username

    informations["links"] = get_social_medias(url)

    mostPlayedChamp = None

    if informations["links"]:
        if informations["links"]["factor"]:
            factor = informations["links"]["factor"]

            mostPlayedChamp = get_most_played_champion(factor)
            championKills = get_champion_kills(factor)

    informations["mostPlayedChamp"] = mostPlayedChamp
    informations["championKills"] = championKills
    
    if console == True:
        print(f">> Fetching {username} informations.. ({number}/{playerNumber})")

    return informations

def get_won_tournaments(url: str):
    newUrl = url+"/Results"

    res = requests.get(newUrl)

    soup = BeautifulSoup(res.text, "lxml")
    
    table = soup.find("tbody")

    if table == None:
        return

    wins = {}
    tournamentName = None

    for tr in soup.find_all("tr"):
        placement_td = tr.find("td", class_="placement-1")
        if placement_td and "1st" in placement_td.text:
            tournament_name = placement_td.find_next("td").find("a").text
            if tournament_name in wins:
                wins[tournament_name] += 1
            else:
                wins[tournament_name] = 1
                
    return wins

def get_social_medias(url: str):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "lxml")

    links_div = soup.find("div", {"class": "infobox-center infobox-icons"})
    links = {}
    
    if links_div == None:
        return

    for social_media in links_div.findAll("a"):
        link = social_media.get("href")

        if "youtube" in str(link):
            links["youtube"] = link
        elif "facebook" in str(link):
            links["facebook"] = link
        elif "instagram" in str(link):
            links["instagram"] = link
        elif "twitter" in str(link):
            links["twitter"] = link
        elif "factor" in str(link):
            links["factor"] = link
        elif "twitch" in str(link):
            links["twitch"] = link
    
    return links