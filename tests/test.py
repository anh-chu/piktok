from piktok import App
from pprint import pprint
import asyncio
import json

from aiomisc import entrypoint
from aiomisc.service import Profiler


# proxy = "http://123.122.68.1:88"
#proxy = None


async def main():
    r1 = await app.discover.user()
    r2 = await app.discover.music()
    r3 = await app.suggested.fetch()
    r4 = await app.info.user_by_name('fpgezekatz')
    r5 = await app.tiktoks.from_user_id(6834564640216974341, total=300)
    r6 = await app.suggested.crawl(7, 3, user_id=143273922984189952, user_count=30)
    print(len(r1), len(r2), len(r3), len(r4))
    print(len(r5), len(set([item['itemInfos']['id'] for item in r5])))
    print(len(r6['user']))

loop = asyncio.get_event_loop()
# with entrypoint(Profiler(interval=0.1, top_results=5)) as loop:
app = App(proxy)
# r = loop.run_until_complete(app.suggested.crawl(10, 2, user_id=None, user_count=30))
loop.run_until_complete(main())
# with open('out.json', 'w+') as f:
#     json.dump(r, f)
