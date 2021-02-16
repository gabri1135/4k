import hashlib
import os
import re
import requests
import shutil
from Crypto.Cipher import AES


class Downloader:
    def getIV(self):
        encoded_str = self.key.hex().encode()
        hash_obj = hashlib.sha1(encoded_str)
        iv = hash_obj.hexdigest()
        return bytes.fromhex(iv[0:32])

    def getFile(self, url):
        r = requests.get(url, stream=True)
        temp = b''

        for chunk in r.iter_content(32 * 1024):
            temp += chunk
        return temp

    def __init__(self, graphic_self, m3u8_file, output_file):
        temp_name = output_file.removesuffix(
            '.mp4').split('\\')[-1].replace(' ', '_')
        temp_folder = os.getcwd()+'\\.%s' % temp_name

        data = open(m3u8_file, 'r').read()

        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
            open('%s/data.txt' % temp_folder, 'w').write("%s\n%s" %
                                                         (m3u8_file, output_file))

        os.chdir(temp_folder)

        key_url = re.findall(
            '#EXT-X-KEY:METHOD=AES-128,URI="(.*)"', data)

        self.key = self.getFile(key_url[0])

        decryptor = AES.new(self.key, AES.MODE_CBC, IV=self.getIV())

        film_urls = re.findall(
            '#EXTINF:.*,\s(.*)', data)[0:10]

        l = len(film_urls)-1

        try:
            num = int(re.findall("file '.*_(.*).mp4",
                                 open('temp.txt', 'r').readlines()[-1])[0])+1
        except:
            num = 0

        try:
            for i in range(num, len(film_urls)):
                file_name = 'tmp_%d.mp4' % i
                print('Processing %d of %d' % (i+1, l))

                open(file_name, 'wb').write(
                    decryptor.decrypt(self.getFile(film_urls[i])))

                open('temp.txt', 'a').write("file '%s'\n" % file_name)

        except:
            graphic_self.error(
                "Errore download", "Errore nel download dei file\nRiprova in seguito")

        else:
            os.system("ffmpeg -f concat -i temp.txt -c copy output.mp4")
            shutil.move("output.mp4", output_file)
            if os.path.exists(output_file):
                os.chdir(temp_folder.removesuffix('/.%s' % temp_name))
                shutil.rmtree(temp_folder)
            else:
                graphic_self.error(
                    "Errore concatenamento", "Errore nella concatenazione dei file\n Riprova in seguito")
