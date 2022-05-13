import requests
from bs4 import BeautifulSoup

real_url = "/mp4/adshort/20220509/cont-1761037-15876234_adpkg-ad_hd.mp4"

pear_url = "https://www.pearvideo.com/video_1761037"
cont_id = pear_url.split("_")[-1]


vedio_url = "https://www.pearvideo.com/videoStatus.jsp?contId=1761037&mrd=0.8150207082854097"

xhr = {
	"videos": {
		"hdUrl": "",
		"hdflvUrl": "",
		"sdUrl": "",
		"sdflvUrl": "",
		"srcUrl": "https://video.pearvideo.com/mp4/adshort/20220509/1652150119728-15876234_adpkg-ad_hd.mp4"
	}
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Referer": pear_url
}

resp = requests.get(vedio_url, headers=headers)
# print(resp.json())
dict = resp.json()
systemTime = dict["systemTime"]
srcUrl = dict["videoInfo"]["videos"]["srcUrl"]

# print(systemTime, srcUrl)
realsrcUrl = srcUrl.replace(systemTime, "cont-"+cont_id)
print(realsrcUrl)

resp.close()

with open("vedio/"+cont_id+".mp4", mode = "wb") as f:
    resp = requests.get(realsrcUrl)
    f.write(resp.content)
    resp.close


