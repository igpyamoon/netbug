import string
import requests
import time
from bs4 import BeautifulSoup

main_url = "https://www.umei.cc/bizhitupian/weimeibizhi/"

resp = requests.get(main_url)
resp.encoding = 'utf-8'

main_page = BeautifulSoup(resp.text, features="html.parser")

lists = main_page.find("div", class_="swiper mySwiper").find_all("li")
for list in lists:
    href = list.find("a").get('href')
    img_name = href.split('/')[-1]
    # print(img_name)
    child_resp = requests.get(main_url+img_name)
    child_page = BeautifulSoup(child_resp.text, features="html.parser")
    img_src = child_page.find("section", class_="img-content").find("img").get("src")
    img_resp = requests.get(img_src)
    with open("img/"+img_name.split('.')[0]+".jpg", mode="wb") as f:
        f.write(img_resp.content)
    print("download over!!!", img_name.split('.')[0])
    child_resp.close()
    time.sleep(1)

resp.close
