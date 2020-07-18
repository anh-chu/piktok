import asyncio
import atexit

from aiohttp import ClientSession, TCPConnector
from termcolor import colored

from .discover import Discover
from .suggested import Suggested
from .tiktoks import TikTok
from .verifier import Verifier


class App:
    """
    Main application class. Initialize with app = App() to start.
    """

    _session: ClientSession
    _proxy: str

    discover: Discover
    suggested: Suggested

    def __init__(self, proxy: str = None):
        self._session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self._proxy = proxy

        self.discover = Discover(self._session, self._proxy)
        self.suggested = Suggested(self._session, self._proxy)
        self.tiktoks = TikTok(Verifier(self._session, self._proxy))

        atexit.register(self.cleanup)

        print(colored("Initialized app!", "green"))

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: str):
        self._proxy = proxy

    async def close(self):
        await self._session.close()

    def cleanup(self):
        """
        Cleanup application by closing the aiohttp client session
        """
        loop = asyncio.get_event_loop()
        print(colored("Closing async session...", "yellow"))
        loop.create_task(self.close())
