import requests
from bs4 import BeautifulSoup

def get_most_played_champion(url: str):
    res = requests.get(url)

    soup = BeautifulSoup(res.text, "lxml")