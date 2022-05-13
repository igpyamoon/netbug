# get vedio 某科学的超电磁炮 from bilibili by yamoon on 2022-05-12

import os
import requests
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup

origin_url = "https://www.bilibili.com"

railgun_url = "https://www.bilibili.com/bangumi/play/ss425/"
referer_url = railgun_url

season_url = "https://api.bilibili.com/pgc/view/web/season?ep_id=84340"

# referer_url = "https://www.bilibili.com/bangumi/play/ss425/"

PATH = 'video/'
EXTENS = '.m4s'

#1st
episode_00_url = "https://api.bilibili.com/pgc/player/web/playurl?avid=3934631&cid=432126871&qn=64&fnver=0&fnval=4048&fourk=1&ep_id=84340&session=2bdb5b20af4d5922e58e02efabe13b92"
#18th
episode_18_url = "https://api.bilibili.com/pgc/player/web/playurl?avid=634374044&cid=432132639&qn=64&fnver=0&fnval=4048&fourk=1&ep_id=84357&session=1018e356a098b04cfc9a790ce1d7b7cd"


oprate_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Origin": origin_url,
    "Referer": referer_url
}

"""get every epsode url from requests of season url"""
def get_epsode_url(url):
    episode_urls = []
    with requests.get(url, headers=oprate_headers) as resp:
        # print(resp.json()['result'])
        for episode in resp.json()['result']['episodes']:
            # print(episode)
            aid = episode['aid']
            cid = episode['cid']
            short_link = episode['short_link']
            ep_id = short_link.split('/')[-1].split('p')[-1]
            # print(aid, cid, ep_id)
            episode_url = f"https://api.bilibili.com/pgc/player/web/playurl?avid={aid}&cid={cid}&qn=64&fnver=0&fnval=4048&fourk=1&ep_id={ep_id}&session=2bdb5b20af4d5922e58e02efabe13b92"
            episode_urls.append(episode_url)
    return episode_urls

# def url_download(url):
async def url_download(url, session, filename):
    async with session.get(url, headers=oprate_headers) as resp:
        async with aiofiles.open(filename, mode='wb') as f:
            await f.write(await resp.content.read())
            await asyncio.sleep(0)
            print("file download complete!!! --", filename)

# def video_parse_url(url, headers):
#     resp = requests.get(url, headers=headers)
#     dict = resp.json()
#     video_url = dict['data']['dash']['video'][0]['baseUrl']
#     # print(video_url)
#     audio_url = dict['data']['dash']['audio'][0]['baseUrl']
#     resp.close()
#     return video_url, audio_url

async def season_download(season_url, filename):
    # get episode url
    async with aiohttp.ClientSession() as session:
        async with session.get(season_url, headers=oprate_headers) as resp:
            dict = await resp.json()
            # print('-----------------------')
            # print(dict['result'])
            # print('-----------------------')
            video_url = dict['result']['dash']['video'][0]['baseUrl']
            audio_url = dict['result']['dash']['audio'][0]['baseUrl']
            video_name = PATH + 'video_' + filename + EXTENS
            audio_name = PATH + 'audio_' + filename + EXTENS
            tasks = []
            timeout = aiohttp.ClientTimeout(total=60*60, sock_read=240)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                tasks.append(asyncio.create_task(url_download(video_url, session, video_name)))
                tasks.append(asyncio.create_task(url_download(audio_url, session, audio_name)))
                await asyncio.wait(tasks)
                await asyncio.sleep(0)


def video_decrypto():
    pass

# def video_merge(video_name, audio_name, new_name):
def video_merge(filename):
    video_name = PATH + 'video_' + filename + EXTENS
    audio_name = PATH + 'audio_' + filename + EXTENS
    new_name = PATH + filename + '.mp4'
    os.system(f'ffmpeg -i "{video_name}" -i "{audio_name}" -c copy "{new_name}"')
    os.remove(video_name)
    os.remove(audio_name)
    

async def main():

    # episode_names = []

    # 1. get epsode url total 24
    urls = get_epsode_url(season_url)
    tasks = []
    i = 0
    for url in urls:
        # print(url)
        episode_name = f'railgin_episode_{i}'
        # episode_names.append(episode_name)
        i += 1
        # print(url)
        season_download(url, episode_name)
        
        video_decrypto()

        video_merge(episode_name)

    # await asyncio.wait(tasks)

   


if __name__ == '__main__':
    asyncio.run(main())


