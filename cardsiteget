import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {"User-Agent":
           "Mozilla/5.0  "}

def get_url():
    for j in range(1, 8):
        url = f"https://scrapingclub.com/exercise/list_basic/?page={j}"
        response = requests.get(url, headers = headers )
        soup = BeautifulSoup(response.text, "lxml") #html.parser
        data = soup.find_all("div", class_="w-full rounded border")
        for i in data:
            card_url = "https://scrapingclub.com" + i.find("a").get("href")
            yield card_url

def array():
    for card_url in get_url():

        response = requests.get(card_url, headers= headers)
        sleep(3)
        soup = BeautifulSoup(response.text,"lxml")
        data = soup.find("div", class_="my-8 w-full rounded border")

        name = data.find("h3").text
        price = data.find("h4").text
        text = data.find("p").text
        url_img = "https://scrapingclub.com" + data.find("img").get("src")
        yield name, price, text, url_img
