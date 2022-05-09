import requests
import re
import csv

dytt_url = "https://m.dytt8.net/"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
}

# f = open("IMDB8.csv", mode='w')
# csvwriter = csv.writer(f)

resp = requests.get(dytt_url+"index2.htm", headers=headers)

resp.encoding = "gb2312"

obj = re.compile(r"<a href='(?P<imdb8>.*?)'>IMDB评分8分", re.S)

dytt_html = resp.text

result = obj.finditer(dytt_html)

for it in result:
    imdb8 = it.group("imdb8")
    break

imdb8_url = dytt_url + imdb8

resp.close()

# second url
resp = requests.get(imdb8_url, headers=headers)
resp.encoding = "gb2312"
imdb8_html = resp.text

obj1 = re.compile(r'IMDB评分8分.*?更新至.*?</p>(?P<content>.*?)<center>共2页', re.S)

result = obj1.finditer(imdb8_html)
for it in result:
    # print(it.group("year"))
    # print(it.group("type"))
    # print(it.group("name"))
    imdb8_content = it.group("content")
    break
    
obj2 = re.compile(r'<p>(?P<year>.*?)年(?P<type>.*?)《(?P<name>.*?)》', re.S)

result = obj2.finditer(imdb8_content)
for it in result:
    print(it.group("year"))
    print(it.group("type"))
    print(it.group("name"))
    # break

resp.close()