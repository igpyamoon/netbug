
import re
import requests
import csv


url = "https://movie.douban.com/top250"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
}

params = {
    "Scheme": "https",
    "Host": "movie.douban.com",
    "Filename": "/top250",
    "start": 0,
    "filter": 0

}

f = open("movie.csv", mode='w')
csvwriter = csv.writer(f)

obj = re.compile(r'<li>.*?<em class="">(?P<num>.*?)</em>'
                r'.*?<span class="title">(?P<name>.*?)</span>'
                r'.*?导演: (?P<director>.*?)&nbsp;&nbsp;'
                r'.*?<br>(?P<year>.*?)&nbsp;'
                r'.*?<span class="inq">(?P<discrption>.*?)</span>', re.S)

#top 250 = 25 * 10
for i in range(0,8):
    params["start"] = i*25

    resp = requests.get(url, params=params, headers=headers)
    page_content = resp.text

    result = obj.finditer(page_content)

    for it in result:
        # print(it.group("name"))
        # print(it.group("director"))
        # print(it.group("year").strip())
        dict = it.groupdict()
        dict['year'] = dict['year'].strip()
        csvwriter.writerow(dict.values())

    resp.close()


f.close()
