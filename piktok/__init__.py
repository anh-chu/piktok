import asyncio
import atexit

from aiohttp import ClientSession, TCPConnector
from .base import INFO, SUCCESS, s_print
from .discover import Discover
from .suggested import Suggested
from .tiktoks import TikToks
from .info import Info
from .verifier import Verifier


class App:
    """
    Main application class. Initialize with app = App(proxy) to start.
    """

    _session: ClientSession = None

    @classmethod
    def __create(cls):
        if cls._session is None:
            cls._session = ClientSession(connector=TCPConnector(verify_ssl=False))

    def __init__(self, proxy: str = None):
        """
        Args:
            proxy (str): proxy server url
        """
        App.__create()
        s_print("HTTP session connected", INFO)

        self._proxy = ""
        if proxy:
            s_print(f"Connecting to proxy at {proxy}", INFO)
            self._proxy = proxy

        self.discover = Discover(self._session, self._proxy)
        self.suggested = Suggested(self._session, self._proxy)
        verifier_object = Verifier(self._session, self._proxy)
        self.tiktoks = TikToks(verifier_object)
        self.info = Info(verifier_object)

        s_print("Started component apps", INFO)

        atexit.register(App.cleanup)

        s_print("Initialized app!", SUCCESS)

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: str):
        self._proxy = proxy

    @classmethod
    def cleanup(cls):
        s_print("Closing HTTP session...", INFO)
        if cls._session:
            asyncio.get_event_loop().create_task(cls._session.close())
        s_print("App shut down.", SUCCESS)
