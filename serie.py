from data import Data
from path import PathModel
from typing import Dict, List
import urllib3
from bs4 import BeautifulSoup


class Serie:
    def __init__(self, _url: str) -> None:
        self.http = urllib3.PoolManager()
        page = BeautifulSoup(self.http.request(
            'GET', self.newSite()+_url, preload_content=False), 'html.parser')

        self.name = str(page.h1.string).replace(':', '')
        self.url = page.iframe['src']

        self.all = self._getEpisodes()

    def newSite(self) -> str:
        page = BeautifulSoup(self.http.request(
            'GET', "https://nuovoindirizzo.info/seriehd/", preload_content=False), 'html.parser')
        return page.a["href"]

    def _getEpisodes(self) -> List[int]:
        _page = BeautifulSoup(self.http.request(
            'GET', self.url, preload_content=False), 'html.parser')
        _seasons = _page.find_all('ul')[1].find_all('li')

        all = []
        for x in range(len(_seasons)):
            _page = BeautifulSoup(self.http.request(
                'GET', "%s?season=%d" % (self.url, x), preload_content=False), 'html.parser')

            _episodes = _page.ul.find_all('li')
            all.append(len(_episodes))
        return all

# season:    from 0 to all.lenght-1
# episode:   from 0 to all[s]-1      già ordinati
    def check(self, input: Dict[int, List[int]], last: List[int]) -> List[tuple]:
        _all = []
        for id in input:
            episodes = input[id]
            # check season exist
            if id >= len(self.all):
                print("Season %d out of range" % id)
                break

            while episodes[-1] >= self.all[id]:
                print("Removed episode %d, max is %d" %
                      (episodes.pop()+1, self.all[id]))

            if id in last:
                for x in range(episodes.pop(), self.all[id]):
                    _all.append((id, x))

            for e in episodes:
                _all.append((id, e))

        _all = list(set(_all))
        _all.sort()
        for x in _all:
            print(x)
        return _all

    def init(self, out: PathModel) -> PathModel:
        out = out.add(self.name)
        if Data.create(out):
            out.temp(space='').create()
        return out

    @staticmethod
    def initialize(detail: tuple, _outputFolder: PathModel, m3u8Path: PathModel) -> None:
        temp = _outputFolder.temp(space='').add(
            '.%d_%d' % (detail[0]+1, detail[1]+1))
        if temp.exist():
            m3u8Path.remove()
            return

        temp.create()
        m3u8Path.move(temp.add(".m3u8"))

        temp.add("temp.txt").write("ffconcat version 1.0\n\n", "w")
