from data import Data
import os
import re
import requests
import shutil
from utils import *
from decrypt import Decrypt


class Downloader:

    def getFile(self, url):
        r = requests.get(url, stream=True)
        temp = b''

        for chunk in r.iter_content(32 * 1024):
            temp += chunk
        return temp

    def __init__(self, dat: Data, path, progress=0):
        if path[-4:] != ".mp4":
            path += '.mp4'

        tempPath = tempFolder(path)
        os.chdir(tempPath)

        try:
            progress = int(re.findall("file '.*_(.*).mp4",
                                      open('temp.txt', 'r').readlines()[-1])[0])+1
        except:
            open("temp.txt", "w").write('')

        data = open(".m3u8", 'r').read()

        key_url = re.findall(
            '#EXT-X-KEY:METHOD=AES-128,URI="(.*)"', data)
        key = self.getFile(key_url[0])

        dec = Decrypt(key)

        film_urls = re.findall(
            '#EXTINF:.*,\s(.*)', data)

        l = len(film_urls)

        try:
            for i in range(progress, l):
                file_name = 'tmp_%d.mp4' % i
                print('Processing %d of %d' % (i+1, l))

                open(file_name, 'wb').write(
                    dec.get(self.getFile(film_urls[i])))

                open('temp.txt', 'a').write("file '%s'\n" % file_name)

        except:
            print("Errore nel download dei file\nRiprova in seguito")

        else:
            os.system("ffmpeg -f concat -i temp.txt -c copy output.mp4")
            os.chdir(dir(tempPath))
            shutil.move("%s\\output.mp4" % tempPath, path)
            if os.path.exists(path):
                shutil.rmtree(tempPath)
            else:
                print("Errore nella concatenazione dei file\n Riprova in seguito")
