import shutil
import os


def tempFolder(path, all=True):
    if path[-4:] == ".mp4":
        path = path.removesuffix(
            '.mp4')
    tempName = path.split('\\')[-1].replace(' ', '_').replace(':','-')
    if all:
        return '%s\\.%s' % (os.getcwd(), tempName)
    else:
        return '.%s' % tempName


def initialize(name, m3u8Path):
    try:
        temp = tempFolder(name)
        os.mkdir(temp)
    except: None

    if m3u8Path[-5:] != ".m3u8":
        m3u8Path += ".m3u8";
    shutil.move(m3u8Path, "%s\\.m3u8" % temp)

def realPath(tempPath):
    tempPath=tempPath[1:]
    return tempPath.replace('_', ' ')


def dir(path):
    temp=path.split('\\')[-1]
    return path.removesuffix(temp)
