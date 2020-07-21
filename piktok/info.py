from .verifier import Verifier
from .base import Base
from requests.models import PreparedRequest


class Info(Base):
    """
    Class for getting information about a single user, music, or challenge
    """

    _urls = {
        "music": "https://m.tiktok.com/api/music/detail/",
        "user": "https://m.tiktok.com/api/user/detail/",
        "challenge": "https://m.tiktok.com/api/challenge/detail/",
    }

    _params = {"language": "en"}

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

    async def __mid_prep(self, url: str, explicit_kwargs: dict):
        """
        Prep headers and parameters by signing the url and adding headers

        Args:
            url (str): url to sign
            explicit_kwargs (str): parameters to add for signing

        Returns:
            tuple: signed url & signed headers

        """
        req = PreparedRequest()
        req.prepare_url(url, explicit_kwargs)
        req.prepare_url(req.url, await self._verifier.get_verifiers(req.url))
        headers = self._headers.copy()
        headers["path"] = req.url.split("tiktok.com")[1]
        return req.url, headers

    async def music(self, music_id: int, **kwargs):
        """
        Get music info by id

        Args:
            music_id (int): numeric id of music to get
            **kwargs: any other path parameters

        Returns:
            dict: music info

        """
        explicit_kwargs = self._params.copy()
        explicit_kwargs["musicId"] = str(music_id)

        url, headers = await self.__mid_prep(self._urls["music"], explicit_kwargs)

        return await self._get_data(url, headers, kwargs, self._proxy)

    async def challenge_by_id(self, challenge_id: int, **kwargs):
        """
        Get challenge info by id

        Args:
            challenge_id (int): numeric id of challenge to get
            **kwargs: any other path parameters

        Returns:
            dict: challenge info

        """
        explicit_kwargs = self._params.copy()
        explicit_kwargs["challengeId"] = str(challenge_id)

        url, headers = await self.__mid_prep(self._urls["challenge"], explicit_kwargs)

        return await self._get_data(url, headers, kwargs, self._proxy)

    async def challenge_by_name(self, challenge_name: str, **kwargs):
        """
        Get challenge info by id

        Args:
            challenge_name (str): name of the hastag challenge to get (without #)
            **kwargs: any other path parameters

        Returns:
            dict: challenge info

        """
        explicit_kwargs = self._params.copy()
        explicit_kwargs["challengeName"] = challenge_name

        url, headers = await self.__mid_prep(self._urls["challenge"], explicit_kwargs)

        return await self._get_data(url, headers, kwargs, self._proxy)

    async def user_by_name(self, user_name: str, **kwargs):
        """
        Get user info by id

        Args:
            user_name (str): name of the user to get (unique name)
            **kwargs: any other path parameters

        Returns:
            dict: user info

        """
        explicit_kwargs = self._params.copy()
        explicit_kwargs["uniqueId"] = user_name

        url, headers = await self.__mid_prep(self._urls["user"], explicit_kwargs)

        return await self._get_data(url, headers, kwargs, self._proxy)

    async def user_by_id(self, user_id: int, **kwargs):
        """
        Get user info by id

        Args:
            user_id (int): numeric id of user to get
            **kwargs: any other path parameters

        Returns:
            dict: user info

        """
        explicit_kwargs = self._params.copy()
        explicit_kwargs["userId"] = str(user_id)

        url, headers = await self.__mid_prep(self._urls["user"], explicit_kwargs)

        return await self._get_data(url, headers, kwargs, self._proxy)
