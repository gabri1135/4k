from typing import List, Tuple
import re


class M3U8:

    def __init__(self, duration: str, url: str) -> None:
        self.duration = duration
        self.url = url

    @staticmethod
    def get(duration: str, url: str) -> M3U8:
        temp = M3U8(duration, url)
        return temp

    @staticmethod
    def getAll(self) -> Tuple[str, List[M3U8]]:
        data = open(".m3u8", 'r').read()

        key_url = re.findall(
            r'#EXT-X-KEY:METHOD=AES-128,URI="(.*)"', data)
        key = self.getFile(key_url[0])

        M3U8s = []

        for x in re.findall(r'#EXTINF:(.*),\s(.*)', data):
            M3U8s.append(M3U8.get(x[0], x[1]))

        return key, M3U8s
