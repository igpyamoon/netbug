import requests


# url = "https://www.baidu.com/?query=python"
# url = "https://fanyi.baidu.com/sug"
url = "https://movie.douban.com//j/chart/top_list"

param = {
    "type": "24",
    "interval_id": "100:90",
    "action": "",
    "start": 0,
    "limit": 20
}

# s = input("please input the keyword:")

# dat = {
#     "kw": s
# }

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0"
}

# resp = requests.get(url, headers=headers)
# resp = requests.post(url, data=dat)
resp = requests.get(url, params=param, headers=headers)

print(resp)
print(resp.request.url)
print(resp.json())

print(resp.cookies())

