from m3u8 import M3U8
import os
import re
import requests
import shutil
from decrypt import Decrypt
from path import PathModel
from id import Id


class Downloader:

    @staticmethod
    def getFile(url: str) -> bytes:
        r = requests.get(url, stream=True)
        temp = b''

        for chunk in r.iter_content(32 * 1024):
            temp += chunk
        return temp

    def __init__(self, _outputFile: PathModel, _tempFolder: PathModel = None) -> None:
        if _tempFolder is None:
            _tempFolder = _outputFile.temp()
        os.chdir(_tempFolder.path)

        try:
            progress = int(re.findall("file tmp_(.*).mp4",
                                      open('temp.txt', 'r').readlines()[-3])[0])+1
        except:
            progress = 0

        key, M3U8s = M3U8.getAll(self)

        dec = Decrypt(key)

        l = len(M3U8s)
        id = Id(l, progress)

        try:
            for i in range(progress, l):
                file_name = 'tmp_%s.mp4' % id.add()
                print('Processing %d of %d' % (i+1, l))

                url = M3U8s[i].url
                url = "http" + url.removeprefix("https")

                open(file_name, 'wb').write(
                    dec.get(self.getFile(url)))

                open('temp.txt', 'a').write(
                    "file %s\nduration %s\n\n" % (file_name, M3U8s[i].duration))

        except:
            print("Errore nel download dei file\nRiprova in seguito")

        else:
            #            size = 0
            #            st = os.stat_result.
            #            free = st.f_bavail * st.f_frsize
            #            for file_name in os.listdir(tempPath):
            #                size += os.path.getsize(file_name)
            #
            #            if free >= size:
            self._concatenateAll()
#            else:
#                self._concatenateProgress(l)

            os.chdir(_tempFolder.dir)

            shutil.move("%s\\output.mp4" % _tempFolder.name, _outputFile.path)
            shutil.rmtree(_tempFolder.path)

    def _concatenateAll(self) -> None:
        os.system("ffmpeg -f concat -i temp.txt -c copy output.mp4")

    def _concatenateProgress(self, l: int) -> None:
        all = []

        for file in os.listdir():
            name = re.findall("tmp_(.*).mp4", file)
            if len(name) != 0:
                all.append(int(name[0]))
                if name[0] == '0':
                    self._rename(name[0])

        all.sort()

        for file in all:
            os.system("ffmpeg -f concat -i temp.txt -c -y copy output.mp4")
            os.remove("tmp_%.mp4")

    def _rename(self, num: str) -> None:
        os.rename("tmp_%s.mp4" % num, "output.mp4")
