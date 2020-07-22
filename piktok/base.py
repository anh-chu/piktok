import colored
import orjson
from aiohttp import ClientSession
from colored import stylize
from humps import decamelize
from inflection import camelize


SUCCESS = colored.fg("light_green") + colored.attr("bold")
INFO = colored.fg("aquamarine_3")
ERROR = colored.fg("red")


def s_print(text: str, style: colored):
    """
    Print text with style in the terminal

    Args:
        text (str): text to print
        style (colored): style to print with

    Returns:
        None: None
    """
    print(stylize(text, style))


class Base:
    _headers: dict = {}
    _params: dict = {}
    _proxy: str = ""
    _url: str = ""
    _urls: list = []
    _session: ClientSession = None

    @classmethod
    def init_class(cls, session: ClientSession, proxy: str):
        if cls._session is None:
            cls._session = session
        if not cls._proxy:
            cls._proxy = proxy

    def __init__(self, session: ClientSession, proxy: str):
        self.init_class(session, proxy)

    @classmethod
    def get_default_params(cls):
        """
        Returns:
            dict: the default parameters to be used in music, user, and challenge

        """
        return decamelize(cls._params)

    @classmethod
    def __convert_options(cls, options: dict = None) -> dict:
        """
        Call .utils.options_to_params to convert keyword options to params

        Args:
            options (dict): keyword options to convert

        Returns:
            dict: dict of converted path parameters

        """
        new_options = {**cls._params, **options}
        return cls.__options_to_params(new_options)

    @staticmethod
    def __options_to_params(options: dict) -> dict:
        """
        Convert keywords options to a dict of RESTful parameters

        Args:
            options (dict): dict of keyword options

        Returns:
            dict: dict of parameterized options

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

        Args:
            url (str): url to get
            headers (dict): dict of headers
            params (dict): dict of path parameters
            proxy (str): http url of proxy server
            **kwargs:

        Returns:
            dict: response converted to dict

        """
        converted_params = self.__convert_options({**params, **kwargs})
        async with self._session.get(
            url, headers=headers, params=converted_params, proxy=proxy
        ) as response:
            content = await response.content.read()
        return orjson.loads(content)
