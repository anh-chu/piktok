from .verifier import Verifier
from .base import Base

# TODO: implement page scrolling


class TikToks(Base):
    """
    Class to fetch tiktoks owned by an user, music, or challenge
    """

    _url = "https://m.tiktok.com/share/item/list?verifyFp="
    _params = {
        "secUid": "",
        "id": "",
        "type": "",
        "count": 30,
        "minCursor": 0,
        "maxCursor": 0,
        "shareUid": "",
        "lang": "en",
        "verifyFp": "",
    }

    _headers = {
        "authority": "m.tiktok.com",
        "method": "GET",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "referrer": "https://www.tiktok.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.0 Safari/537.36)",
        "path": "",
    }

    def __init__(self, verifier: Verifier):
        self._verifier = verifier
        super().__init__(verifier.session, verifier.proxy)

    async def __prep(self, url):
        """
        Sign the url with fingerprint

        Args:
            url (str): url to sign

        Returns:
            tuple: signed headers & parameters

        """
        headers = self._headers.copy()
        headers["path"] = url.split("tiktok.com")[1]

        verifiers = await self._verifier.get_verifiers(url)
        explicit_kwargs = self._params.copy()
        explicit_kwargs.update(verifiers)
        return headers, explicit_kwargs

    async def __fetch_and_scroll(
        self,
        total: int,
        url: str,
        headers: dict,
        explicit_kwargs: dict,
        proxy: str,
        **kwargs
    ):
        """
        Get any number of tiktoks by implementing scrolling cursors
        Args:
            total (int): total number of tiktoks wanted
            url (str): url
            headers (dict): headers
            explicit_kwargs (dict): parameters
            proxy (str): proxy
            **kwargs (dict): any other path parameters

        Returns:
            list: list of tiktoks fetched

        """
        results: list = []
        max_cursor: int = 0
        has_more = True
        count = total

        while len(results) < total and has_more:
            explicit_kwargs = {
                **explicit_kwargs,
                **dict(count=count, minCursor=0, maxCursor=max_cursor),
            }
            r = await self._get_data(url, headers, explicit_kwargs, proxy, **kwargs)
            results.extend(r["body"]["itemListData"])
            max_cursor = r["body"]["maxCursor"]
            count = total - len(results)
            has_more = r["body"]["hasMore"]

        return results

    async def from_music_id(self, music_id: int, total: int = 30, **kwargs):
        """
        Get tiktoks owned by a music

        Args:
            music_id (int): numeric id of the music
            total (int): total number of tiktoks wanted
            **kwargs: any other path paramters

        Returns:
            list: list of tiktoks owned by the music

        """
        url = self._url

        headers, explicit_kwargs = await self.__prep(url)

        explicit_kwargs["type"] = 4
        explicit_kwargs["id"] = music_id

        return await self.__fetch_and_scroll(
            total, url, headers, explicit_kwargs, self._proxy, **kwargs
        )

    async def from_user_id(self, user_id: int, total: int = 30, **kwargs):
        """
        Get tiktoks owned by a user

        Args:
            user_id (int): numeric id of the user
            total (int): total number of tiktoks wanted
            **kwargs: any other path paramters

        Returns:
            list: list of tiktoks owned by the user

        """
        url = self._url

        headers, explicit_kwargs = await self.__prep(url)

        explicit_kwargs["type"] = 1
        explicit_kwargs["id"] = user_id

        return await self.__fetch_and_scroll(
            total, url, headers, explicit_kwargs, self._proxy, **kwargs
        )

    async def from_challenge_id(self, challenge_id: int, total: int = 30, **kwargs):
        """
        Get tiktoks owned by a challenge

        Args:
            challenge_id (int): numeric id of the hashtag challenge
            total (int): total number of tiktoks wanted
            **kwargs: any other path paramters

        Returns:
            list: list of tiktoks owned by the challenge

        """
        url = self._url

        headers, explicit_kwargs = await self.__prep(url)

        explicit_kwargs["type"] = 3
        explicit_kwargs["id"] = challenge_id

        return await self.__fetch_and_scroll(
            total, url, headers, explicit_kwargs, self._proxy, **kwargs
        )
