import json
from typing import Dict
import urllib3
from bs4 import BeautifulSoup


class Serie:
    def __init__(self, _url: str) -> None:
        http = urllib3.PoolManager()
        page = BeautifulSoup(http.request(
            'GET', _url, preload_content=False), 'html.parser')

        self.name = page.h1.string
        self.url = page.iframe['src']

        _nSeasons = self._getSeasons(http)

        self.all = []
        for x in range(_nSeasons):
            _episodes = self._getEpisodes(http, x)
            self.all.append(_episodes)

    def _getSeasons(self, http) -> int:
        _page = BeautifulSoup(http.request(
            'GET', self.url, preload_content=False), 'html.parser')

        _seasons = _page.find_all('ul')[1].find_all('li')
        return len(_seasons)

    def _getEpisodes(self, http, id: int) -> int:
        _page = BeautifulSoup(http.request(
            'GET', "%s?season=%d" % (self.url, id), preload_content=False), 'html.parser')

        _episodes = _page.ul.find_all('li')
        return len(_episodes)

# season:    from 0 to all.lenght-1
# episode:   from 0 to all[s]-1      già ordinati
    def check(self, input: dict, last: list) -> list(tuple):
        _all = []
        for id in input:
            id, episodes = int(id), list(input[id])
            # check season exist
            if id >= len(self.all):
                print("Season %d out of range" % id)
                break

            while episodes[-1] >= self.all[id]:
                print("Removed episode %d, max is %d" %
                      (episodes.pop()+1, self.all[id]))

            if id in last:
                [_all.append((id, x))
                 for x in range(episodes.pop(), self.all[id])]

            for e in episodes:
                _all.append((id, e))

        _all = list(set(_all))
        _all.sort()
        for x in _all:
            print(x)
        return _all
