from aiohttp import ClientSession


class Info:
    def __init__(self, session: ClientSession, proxy: str):
        self._session = session
        self._proxy = proxy
