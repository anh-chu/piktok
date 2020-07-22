import asyncio
import random
import string
from contextlib import suppress

from aiohttp import ClientSession
from pyppeteer import launch

from .stealth import stealth


class Verifier:
    """
    Class for verifying TikTok fingerprint
    """

    browser = None
    page = None
    redirect_url: str

    def __init__(
        self, session: ClientSession, proxy: str = "", find_redirect: bool = False
    ):
        self._session = session
        self._proxy = proxy
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.0 Safari/537.36)"
        self.args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            "--window-position=0,0",
            "--ignore-certifcate-errors",
            "--ignore-certifcate-errors-spki-list",
            "--user-agent=" + self.user_agent,
        ]

        if proxy and "@" in proxy:
            self.args.append(
                "--proxy-server="
                + proxy.split(":")[0]
                + "://"
                + proxy.split("://")[1].split(":")[1].split("@")[1]
                + ":"
                + proxy.split("://")[1].split(":")[2]
            )
        else:
            self.args.append("--proxy-server=" + proxy)

        self.options = {
            "args": self.args,
            "headless": True,
            "ignoreHTTPSErrors": True,
            "userDataDir": "./tmp",
            "handleSIGINT": False,
            "handleSIGTERM": False,
            "handleSIGHUP": False,
        }

        self.find_redirect = find_redirect

        asyncio.get_event_loop().create_task(self.start_up())

    @property
    def session(self):
        return self._session

    @property
    def proxy(self):
        return self._proxy

    async def start_up(self):
        self.browser = await launch(self.options)
        self.page = await self.browser.newPage()

        await self.page.evaluateOnNewDocument(
            """() => {
             delete navigator.__proto__.webdriver;
         }"""
        )

        # Check for user:pass proxy
        if self._proxy and "@" in self._proxy:
            await self.page.authenticate(
                {
                    "username": self._proxy.split("://")[1].split(":")[0],
                    "password": self._proxy.split("://")[1].split(":")[1].split("@")[0],
                }
            )

        await stealth(self.page)

    async def get_verifiers(self, url: str) -> dict:
        if self.find_redirect:
            await self.go_find_redirect(url)

        # might have to switch to a tiktok url if they improve security
        await self.page.goto("about:blank", {"waitUntil": "load"})

        self.user_agent = await self.page.evaluate(
            """() => {return navigator.userAgent; }"""
        )

        verify_fp = "".join(
            random.choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits
            )
            for _ in range(16)
        )

        await self.page.evaluate("() => { " + await self.__get_js() + " }")

        signature = await self.page.evaluate(
            '''() => {
            var url = "'''
            + url
            + "&verifyFp="
            + verify_fp
            + """"
            var token = window.byted_acrawler.sign({url: url});
            return token;
        }"""
        )

        return {"verifyFp": verify_fp, "_signature": signature}

    async def go_find_redirect(self, url: str):
        with suppress(Exception):
            await self.page.goto(url, {"waitUntil": "load"})

            self.redirect_url = self.page.url

        await self.browser.close()

    async def __get_js(self):
        r = await self._session.get(
            "https://sf16-muse-va.ibytedtos.com/obj/rc-web-sdk-gcs/acrawler.js",
            proxy=self._proxy,
        )
        return await r.text()
