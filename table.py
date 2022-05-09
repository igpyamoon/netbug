import requests
from bs4 import BeautifulSoup

url = ""
resp = requests.get(url)

page = BeautifulSoup(resp.text, "html.parser")

# table = page.find("table", class_="he_table")
table = page.find("table", attrs={"class": "hp_table"})

trs = table.find_all("tr")[1:]

for tr in trs:
    tds = tr.find_all("td")
    name = tds[0].text
    id = tds[1].text

resp.close()

