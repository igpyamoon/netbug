import asyncio
import aiohttp

urls = {
    "http://kr.shanghai-jiuxin.com/file/2020/0722/7ab9f5b8e61f268604e003cfbc6023f9.jpg",
    "https://tenfei03.cfp.cn/creative/vcg/800/new/VCG211252271916.jpg",
    "https://alifei01.cfp.cn/creative/vcg/800/new/VCG211224906182.jpg"
}

async def aio_img_download(url):
    img_name = url.split('/')[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.headers)
            with open("img/"+img_name, mode="wb") as f:
                f.write(await resp.content.read())
    print("download over", img_name)

async def main():
    tasks = []
    for url in urls:
        tasks.append(aio_img_download(url))

    await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(main())

