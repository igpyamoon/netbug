import requests
import json
import asyncio
import aiohttp
import aiofiles

novel_id = '4305630473'

# novel_url = f"http://dushu.baidu.com/pc/detail?gid={novel_id}"

# novel_catalog = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+ novel_id +'"}'

# chapter_url = "http://dushu.baidu.com/api/pc/getChapterContent?data={"book_id":"4305630473","cid":"4305630473|10566738","need_bookinfo":1}"

# ['data']['novel']['items'] ==> chapter
# ['data']['novel']['content'] ==> content

# download chapter
async def asy_download_chapter(book_id, title, cid):
    data = {
        'book_id': book_id,
        'cid': f"{book_id}|{cid}",
        'need_bookinfo': 1
    }
    data = json.dumps(data)
    chapter_url = f"http://dushu.baidu.com/api/pc/getChapterContent?data={data}"
    async with aiohttp.ClientSession() as session:
        async with session.get(chapter_url) as resp:
            dict = await resp.json()
            async with aiofiles.open(f'novel/悟空传/{title}.txt', mode="w", encoding="utf-8") as f:
                await f.write(dict['data']['novel']['content'])


# get chapter url
async def get_novel(book_id):
    book_url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"'+ book_id +'"}'
    with requests.get(book_url) as resp:
        dict = resp.json()
        tasks = []
        for item in dict['data']['novel']['items']:
            title = item['title']
            cid = item['cid']
            tasks.append(asyncio.create_task(asy_download_chapter(novel_id, title, cid)))
        await asyncio.wait(tasks)


if __name__ == '__main__':
    # print(novel_catalog)
    asyncio.run(get_novel(novel_id))

