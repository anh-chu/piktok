from aiohttp import ClientSession
from .base import Base


# TODO: implement offsets


class Discover(Base):
    """
    Class to get users, musics, and challenges from the Discover page.
    """

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

        Args:
            **kwargs: any path_parameters
        Notes:
            Experiment with parameters [need_item_list, key_word, offset, count, use_recommend, language]
        Returns:
            dict: musics from the Discover page

        """
        url = self._urls.get("music")
        return await self._get_data(url, self._headers, kwargs, self._proxy)

    async def user(self, **kwargs):
        """
        Return users on the Discover page

        Args:
            **kwargs: any path_parameters
        Notes:
            Experiment with parameters [need_item_list, key_word, offset, count, use_recommend, language]
        Returns:
            dict: users from the Discover page

        """
        url = self._urls.get("user")
        return await self._get_data(url, self._headers, kwargs, self._proxy)

    async def challenge(self, **kwargs):
        """
        Return challenges on the Discover page

        Args:
            **kwargs: any path_parameters
        Notes:
            Experiment with parameters [need_item_list, key_word, offset, count, use_recommend, language]
        Returns:
            dict: challenges from the Discover page

        """
        url = self._urls.get("challenge")
        return await self._get_data(url, self._headers, kwargs, self._proxy)
