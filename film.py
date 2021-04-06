from typing import Literal, Tuple
import urllib3
from bs4 import BeautifulSoup
from get_m3u8 import DownloadM3U8
from data import Data
from path import PathModel


class Film:
    def __init__(self, _url: str, outputPath: PathModel) -> None:
        self.http = urllib3.PoolManager()
        page = BeautifulSoup(self.http.request(
            'GET', self.newSite()+_url, preload_content=False), 'html.parser')

        self.name = str(
            page.find("span", attrs={"class": "breadcrumb_last"}).string).replace(':', '')
        self.url = page.iframe['src']

        self.m3u8Path = DownloadM3U8().getFilm(self.url)
        self.outputFile = outputPath.add(f"{self.name}.mp4")
        self.init = Film.initialize(self.outputFile, self.m3u8Path)

    def newSite(self) -> str:
        page = BeautifulSoup(self.http.request(
            'GET', "https://altadefinizione-nuovo.click/", preload_content=False), 'html.parser')
        return page.a["href"]

    @staticmethod
    def initialize(_outputFile: PathModel, m3u8Path: PathModel) -> Tuple[Literal['created', 'continuare', 'sostituire', 'outPath different'], str | None, str | None]:
        _temp = _outputFile.temp()

        data = Data.create(_outputFile)
        if data == 'created':
            _temp.create()
            m3u8Path.move(_temp.add(".m3u8"))
            _temp.add("temp.txt").write("ffconcat version 1.0\n\n", "w")
            return data, None, None
        elif data == 'exist':
            if m3u8Path.read() == _temp.add(".m3u8").read():
                if m3u8Path.path != _temp.add(".m3u8").path:
                    m3u8Path.remove()
                return "continuare", None, None
            else:
                return "sostituire", None, None
        else:
            return data, _outputFile.path, m3u8Path.path
