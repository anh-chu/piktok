from collections import deque
from random import sample
from typing import List

import jmespath as jp
from aiohttp import ClientSession
from termcolor import colored

from .base import Base


class Suggested(Base):
    """
    Class to get suggested users, musics, and challenges.
    """

    _headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "accept-language": "en-US,en;q=0.9",
        "accept-encoding": "gzip",
    }

    _params = {
        "noUser": 0,
        "userCount": 30,
        "userId": "",
    }

    _url = "https://m.tiktok.com/node/share/discover"

    def __init__(self, session: ClientSession, proxy: str):
        super().__init__(session, proxy)

    @staticmethod
    def separate_results(results_list: list, no_user: bool) -> dict:
        """
        Transform the results of finding suggested users, musics, and challenges from list of lists to dict of lists

        :param results_list: list of lists (each child list corresponds to either user, challege, and music
        :param no_user: whether there is a list of users at the start of the list or not
        :return: converted dictionary
        """
        if no_user:
            return {"challenge": results_list[0], "music": results_list[1]}
        return {
            "user": results_list[0],
            "challenge": results_list[1],
            "music": results_list[2],
        }

    @classmethod
    def merge_crawl_results(cls, results_list: List[dict]) -> dict:
        """
        Merge together the results of crawling from a list of many dicts sharing the same keys to one dict with those keys

        :param results_list: list of dicts with 'users', 'challenges', and 'musics' keys
        :return: dict merged from the lists
        """
        users = challenges = musics = []
        for result_dict in results_list:
            users.extend(result_dict.get("user", []))
            challenges.extend(result_dict.get("challenge", []))
            musics.extend(result_dict.get("music", []))
        return cls.separate_results([users, challenges, musics], False)

    async def fetch(
        self, user_id: str = None, user_count: int = 30, no_user: bool = False, **kwargs
    ) -> dict:
        """
        Fetch suggested users, musics, and challenges.

        :param user_id: ID of the TikTok user for whom suggestions are made
        :param user_count: number of suggested users (only) to return from the call
        :param no_user: whether or not to return suggested users
        :param kwargs: any other path parameters
        :return: dict of the suggested elements
        """

        if user_count > 99:
            raise ValueError(colored("user_count must be < 100", "red"))

        url = self._url

        explicit_kwargs = {
            "user_id": user_id,
            "user_count": user_count,
            "no_user": int(no_user),
        }

        response = await self._get_data(
            url, self._headers, explicit_kwargs, self._proxy, **kwargs
        )

        return self.separate_results(
            jp.search("body[*].exploreList", response), no_user
        )

    async def crawl(
        self,
        depth: int = 1,
        choice_count: int = 1,
        user_id: str = None,
        user_count: int = 30,
        **kwargs
    ) -> dict:
        """
        Crawl many suggested elements by using a spider

        :param depth: the depth of crawling (depth * choice_count = number of calls made)
        :param choice_count: how many user IDs to sample from each result set to crawl on next
        :param user_id: starting user ID
        :param user_count: how many suggested users to return from each call
        :param kwargs: other path parameters
        :return: dict of crawled suggested elements
        """
        if user_count < choice_count or user_count < 10:
            raise ValueError(
                colored("user_count must be >= choice_count and >= 10", "red")
            )

        user_ids_queue = deque([user_id])
        limit = depth * choice_count
        level = 0
        results = []

        while len(user_ids_queue):
            next_user_id = user_ids_queue.popleft()

            items = await self.fetch(next_user_id, user_count, False, **kwargs)
            results.append(items)

            response_user_ids = [
                item["cardItem"]["id"] for item in items.get("user", [])
            ]

            if level < limit:
                user_ids_queue.extend(sample(response_user_ids, choice_count))
                level += 1

        return self.merge_crawl_results(results)
