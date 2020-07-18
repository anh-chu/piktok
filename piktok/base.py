import orjson
from aiohttp import ClientSession
from humps import decamelize
from inflection import camelize


class Base:
    _session: ClientSession
    _headers: dict
    _params: dict
    _proxy: str
    _url: str
    _urls: list

    def __init__(self, session: ClientSession, proxy: str):
        self._session = session
        self._proxy = proxy

    @classmethod
    def get_default_params(cls):
        """
        :return: the default parameters to be used in music, user, and challenge
        """
        return decamelize(cls._params)

    @classmethod
    def __convert_options(cls, options: dict = None) -> dict:
        """
        Call .utils.options_to_params to convert keyword options to params

        :param options: keyword options to convert
        :return: dict of converted path parameters
        """
        new_options = {**cls._params, **options}
        return cls.__options_to_params(new_options)

    @staticmethod
    def __options_to_params(options: dict) -> dict:
        """
        Convert keywords options to a dict of RESTful parameters

        :param options: dict of keyword options
        :return: dict of parameterized options
        """
        params = {}
        for key, val in options.items():
            camel_key = camelize(key, uppercase_first_letter=False)
            params[camel_key] = "" if val is None else str(val)
        return params

    async def _get_data(
        self, url: str, headers, params: dict = None, proxy: str = None, **kwargs
    ) -> dict:
        """
        Async get URL and return a dict of results read using ORJSON and aiohttp

        :param url: url to get
        :param headers: dict of headers
        :param params: dict of path parameters
        :param proxy: http url of proxy server
        :return: response converted to dict
        """
        new_params = self.__convert_options({**params, **kwargs})
        params = {**self._params, **new_params}

        async with self._session.get(
            url, headers=headers, params=params, proxy=proxy
        ) as response:
            content = await response.content.read()
        print(content)
        return orjson.loads(content)
