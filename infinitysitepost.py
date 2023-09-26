from requests import Session
from bs4 import BeautifulSoup
from time import sleep

headers = {"User-Agent":
           "Mozilla/5.0  "}

work = Session()

work.get("https://quotes.toscrape.com/", headers=headers)

response = work.get("https://quotes.toscrape.com/login", headers=headers)

soup = BeautifulSoup(response.text, "lxml")

token = soup.find("form").find("input").get("value")

data = {"csrf_token": token, "username": "123", "password": "123"}

result = work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True)


page = 1
while page > 0:
    response = work.get(f"https://quotes.toscrape.com/page/{page}/", headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all("div",class_="quote")
    if data == []:
        break
    page += 1
    n_in_page = 0
    for count in data:
        n_in_page += 1
        quote = count.find("span", class_="text").text
        author = count.find("small", class_="author").text

        print(f"{page - 1}.{n_in_page}. Quote: {quote}, Author: {author}" + "\n")
