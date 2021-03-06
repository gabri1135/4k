import shutil
import os
import re

# from:  C:\Developer\Programmi\film\4k\film.mp4
# to:    C:\Developer\Programmi\film\4k\.film
# to:    .film


def tempFolder(path: str, all: bool = True) -> str:
    if path[-4:] == ".mp4":
        path = path.removesuffix(
            '.mp4')

    temp = re.split(r'\\|\/', path)

    temp[-1] = '.'+temp[-1]
    temp[-1].replace(' ', '_').replace(':', '-')

    if all:
        fullPath = ''
        for x in temp:
            fullPath += x+'\\'
        return fullPath.removesuffix('\\')
    else:
        return temp[-1]


def initializeFilm(name: str, m3u8Path: str) -> bool:
    temp = tempFolder(name)
    if os.path.exists(temp):
        return False

    os.mkdir(temp)
    if m3u8Path[-5:] != ".m3u8":
        m3u8Path += ".m3u8"
    shutil.move(m3u8Path, "%s\\.m3u8" % temp)
    return True


def initializeSerie(name: str, m3u8Path: str, season: int, episode: int) -> bool:
    temp = os.getcwd()+'\\%s' % name
    if not os.path.exists(temp):
        os.mkdir(temp)

    elif os.path.exists('%s\\.%d_%d' % (temp, season, episode)):
        return False

    os.mkdir('%s\\.%d_%d' % (temp, season, episode))
    if m3u8Path[-5:] != ".m3u8":
        m3u8Path += ".m3u8"
    shutil.move(m3u8Path, '%s\\.%d_%d\\.m3u8' % (temp, season, episode))
    return True


# from:  C:\Developer\Programmi\film\4k\.film
# to:    film.mp4
def fileName(path: str) -> str:
    tempPath = re.split(r"\\|\/", path)[-1]
    if tempPath[-4:] != ".mp4":
        tempPath += '.mp4'
    return tempPath.replace('_', ' ')


# from:  C:\Developer\Programmi\film\4k\.film
# from:  C:\Developer\Programmi\film\4k\film.mp4
# to:    C:\Developer\Programmi\film\4k\
def precFolder(path: str) -> str:
    temp = re.split(r"\\|\/", path)[-1]
    return path.removesuffix(temp)
