import hashlib
import os
import re
import requests
import sys
import asyncio
from Crypto.Cipher import AES

def getIV(key):
    encoded_str = key.hex().encode()
    hash_obj = hashlib.sha1(encoded_str)
    iv = hash_obj.hexdigest()
    return bytes.fromhex(iv[0:32])

def decrypt(data, key):
    decryptor = AES.new(key, AES.MODE_CBC, IV=getIV(key))
    return decryptor.decrypt(data)

def getDecryptFile(url, out_file, key):
    r = requests.get(url, stream=True)

    with open(out_file, 'wb') as f:
        for chunk in r.iter_content(32 * 1024):
            f.write(chunk)
            #dec_data = decrypt(chunk, key)
            # f.write(dec_data)
    with open(out_file, 'rb') as f:
        dec_data = decrypt(f.read(), key)
        # f.write(dec_data)
    with open(out_file, 'wb') as f:
        # f.write(chunk)
        #dec_data = decrypt(chunk, key)
        f.write(dec_data)

def concatenate(file, file2):
    if file!=None:
        os.system("ffmpeg -i %s.mp4 -c copy -y %s.ts" % (file, file))
        os.system("del %s.mp4" % file)
    if file2!=None and file2!="output":
        os.system("copy /b output.ts+%s.ts output.ts" % file2)
        os.system("del %s.ts" % file2)

def main(filename, output_folder):
    with open(filename, 'r') as f:
        data = f.read()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    key_url = re.findall(
        '#EXT-X-KEY:METHOD=AES-128,URI="(.*)"', data)
    for chunk in requests.get(key_url[0]):
        key = chunk

    urls = re.findall(
        '#EXTINF:.*,\s(.*)', data)

#    getDecryptFile(urls[0], os.path.join(output_folder, 'output.mp4'), key)
#    os.system("cd %s" % output_folder)
#    prec="output"
#    prec2=None
#    urls.pop(0)

    #temp
    urls=urls[952:]
    prec=None
    prec2=None

    for data_url in urls:
        file_name = os.path.basename(data_url).split('?')[0].split('.')[0]
        print('Processing %s' % re.findall('output_(.*)', file_name)[0])

        out_file = os.path.join(output_folder, '%s.mp4' % file_name)

        getDecryptFile(data_url, out_file, key)
        
        concatenate(prec,prec2)
        prec2=prec
        prec=file_name
    concatenate(prec,prec2)
    concatenate(None,prec)
    os.system("ffmpeg -i output.ts -acodec copy -vcodec copy output.mp4")
    os.system("del output.ts")


if __name__ == '__main__':
    filename = "C://Users//marti//OneDrive//Desktop//programmi//film//4k//gg.m3u8"
    output_folder = "C://Users//marti//OneDrive//Desktop//programmi//film//4k"
    main(filename, output_folder)
