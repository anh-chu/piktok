from aiohttp import ClientSession
from .verifier import Verifier
from .base import Base

# TODO: implement page scrolling


class TikTok(Base):
    _url = "https://m.tiktok.com/share/item/list?verifyFp="
    _params = {
        "secUid": "",
        "id": "",
        "type": '',
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

    _verifier: Verifier

    def __init__(self, verifier: Verifier):
        self._verifier = verifier
        super().__init__(verifier.session, verifier.proxy)

    async def __prep(self, url):
        headers = self._headers
        headers["path"] = url.split("tiktok.com")[1]

        explicit_kwargs = self._params
        verifiers = await self._verifier.get_verifiers(url)
        explicit_kwargs.update(verifiers)
        return headers, explicit_kwargs

    async def from_music(self, music_id: int, **kwargs):
        url = self._url

        headers, explicit_kwargs = await self.__prep(url)

        explicit_kwargs['type'] = 4
        explicit_kwargs["id"] = music_id

        return await self._get_data(
            url, headers, explicit_kwargs, self._proxy, **kwargs
        )

    async def from_user(self, user_id: int, **kwargs):
        url = self._url

        headers, explicit_kwargs = await self.__prep(url)

        explicit_kwargs['type'] = 1
        explicit_kwargs["id"] = user_id

        return await self._get_data(
            url, headers, explicit_kwargs, self._proxy, **kwargs
        )

    async def from_challenge(self, challenge_id: int, **kwargs):
        url = self._url

        headers, explicit_kwargs = await self.__prep(url)

        explicit_kwargs['type'] = 3
        explicit_kwargs["id"] = challenge_id

        return await self._get_data(
            url, headers, explicit_kwargs, self._proxy, **kwargs
        )
