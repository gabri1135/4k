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

    def __init__(self, graphic_self, m3u8Path, path, progress=0):

        tempPath = tempFolder(path)

        if os.path.exists(tempPath):
            os.mkdir(tempPath)

        os.chdir(tempPath)

        data = open(m3u8Path, 'r').read()

        key_url = re.findall(
            '#EXT-X-KEY:METHOD=AES-128,URI="(.*)"', data)
        key = self.getFile(key_url[0])

        dec = Decrypt(data)

        film_urls = re.findall(
            '#EXTINF:.*,\s(.*)', data)

        l = len(film_urls)

        try:
            for i in range(progress, l):
                file_name = 'tmp_%d.mp4' % i
                print('Processing %d of %d' % (i+1, l))

                open(file_name, 'wb').write(
                    Decrypt.get(self.getFile(film_urls[i])))

                open('temp.txt', 'a').write("file '%s'\n" % file_name)

        except:
            graphic_self.error(
                "Errore download", "Errore nel download dei file\nRiprova in seguito")

        else:
            os.system("ffmpeg -f concat -i temp.txt -c copy output.mp4")
            shutil.move("output.mp4", path)
            if os.path.exists(path):
                os.chdir(tempPath.split('\\')[:-1])
                shutil.rmtree(tempPath)
            else:
                graphic_self.error(
                    "Errore concatenamento", "Errore nella concatenazione dei file\n Riprova in seguito")
