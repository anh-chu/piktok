from aiohttp import ClientSession
from .base import Base


class Discover(Base):
    """
    Class to get users, musics, and challenges from the Discover page.
    """

    _session: ClientSession
    _proxy: str

    _headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip",
        "accept-language": "en-US,en;q=0.9",
    }

    _params = {
        "discoverType": 0,
        "needItemList": True,
        "keyWord": "",
        "offset": 0,
        "count": 30,
        "useRecommend": False,
        "language": "en",
    }

    _urls = {
        "music": "https://m.tiktok.com/api/discover/music/",
        "user": "https://m.tiktok.com/api/discover/user/",
        "challenge": "https://m.tiktok.com/api/discover/challenge/",
    }

    def __init__(self, session: ClientSession, proxy: str):
        super().__init__(session, proxy)

    async def music(self, **kwargs):
        """
        Return musics on the Discover page

        :param kwargs: any path_parameters. Experiment with
        [need_item_list, key_word, offset, count, use_recommend, language]
        :return: musics from the Discover page
        """
        url = self._urls.get("music")
        return await self._get_data(url, self._headers, kwargs, self._proxy)

    async def user(self, **kwargs):
        """
        Same as the music method, but for user
        """
        url = self._urls.get("user")
        return await self._get_data(url, self._headers, kwargs, self._proxy)

    async def challenge(self, **kwargs):
        """
        Same as the music method, but for challenge
        """
        url = self._urls.get("challenge")
        return await self._get_data(url, self._headers, kwargs, self._proxy)
