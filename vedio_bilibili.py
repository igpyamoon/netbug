# get vedio from bilibili by yamoon on 2022-05-12
import os
import requests
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
refer_url = ""

site_url = "https://www.bilibili.com/video/BV1e5411t7Yt?p=1"

oprate_url = "https://api.bilibili.com/x/player/playurl?cid=179750567&bvid=BV1e5411t7Yt&qn=64&type=&otype=json&fourk=1&fnver=0&fnval=4048&session=df20d4edb5aa4f7629470c9ffc70bacf"


oprate_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Origin": "https://www.bilibili.com",
    "Referer": site_url
}


def video_parse_url(url, headers):
    resp = requests.get(url, headers=headers)
    dict = resp.json()
    video_url = dict['data']['dash']['video'][0]['baseUrl']
    # print(video_url)
    audio_url = dict['data']['dash']['audio'][0]['baseUrl']
    resp.close()
    return video_url, audio_url


# def video_download(url):
async def video_download(url, headers, session, filename):
    async with session.get(url, headers=headers) as resp:
        async with aiofiles.open(filename, mode='wb') as f:
            await f.write(await resp.content.read())
    

def video_decrypto():
    pass

def video_merge(video_name, audio_name, new_name):
    os.system(f'ffmpeg -i "{video_name}" -i "{audio_name}" -c copy "{new_name}"')
    

async def main():
    url = oprate_url
    headers = oprate_headers
    # 1. parse url
    video_url, audio_url = video_parse_url(url, headers)
    video_name = 'video/' + video_url.split('?')[0].split('/')[-1]
    audio_name = 'video/' + audio_url.split('?')[0].split('/')[-1]
    # 2. get vedio
    # print(video_url, audio_url)
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.append(asyncio.create_task(video_download(video_url,headers, session, video_name)))
        tasks.append(asyncio.create_task(video_download(audio_url,headers, session, audio_name)))
        await asyncio.wait(tasks)

    # 3. decryto if nessessily
    video_decrypto()

    # 4. merge vedio()
    new_name = 'video/first.mp4'
    video_merge(video_name, audio_name, new_name)
    


if __name__ == '__main__':
    asyncio.run(main())


