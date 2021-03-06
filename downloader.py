from data import Data
import os
import re
import requests
import shutil
from utils import *
from decrypt import Decrypt


class Downloader:

    def getFile(self, url: str) -> bytes:
        r = requests.get(url, stream=True)
        temp = b''

        for chunk in r.iter_content(32 * 1024):
            temp += chunk
        return temp

    def __init__(self, dat: Data, path: str, resume: bool) -> None:
        if path[-4:] != ".mp4":
            path += '.mp4'

        tempPath = os.getcwd()+'\\'+tempFolder(path)
        os.chdir(tempPath)

        if resume:
            progress = int(re.findall("file tmp_(.*).mp4",
                                      open('temp.txt', 'r').readlines()[-3])[0])+1
        else:
            progress = 0
            open("temp.txt", "w").write('')

        data = open(".m3u8", 'r').read()

        key_url = re.findall(
            '#EXT-X-KEY:METHOD=AES-128,URI="(.*)"', data)
        key = self.getFile(key_url[0])

        dec = Decrypt(key)

        film_urls = re.findall(
            r'#EXTINF:(.*),\s(.*)', data)

        l = 5

        try:
            for i in range(progress, l):
                file_name = 'tmp_%d.mp4' % i
                print('Processing %d of %d' % (i+1, l))

                open(file_name, 'wb').write(
                    dec.get(self.getFile(film_urls[i][1])))

                open('temp.txt', 'a').write(
                    "file %s\nduration %s\n\n" % (file_name, film_urls[i][0]))

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

            os.chdir(precFolder(tempPath))

            if os.path.exists(path):
                x = 1
                while True:
                    if not os.path.exists("%s(%d).mp4" % (path[:-4], x)):
                        path = "%s(%d).mp4" % (path[:-4], x)
                        break

            shutil.move("%s\\output.mp4" % tempPath, path)
            shutil.rmtree(tempPath)

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
