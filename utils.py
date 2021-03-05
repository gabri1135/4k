import shutil
import os

# from:  C:\Developer\Programmi\film\4k\film.mp4
# to:    C:\Developer\Programmi\film\4k\.film
# to:    .film


def tempFolder(path: str, all: bool = True) -> str:
    if path[-4:] == ".mp4":
        path = path.removesuffix(
            '.mp4')
    temp = path.split('\\')
    temp[-1]='.'+temp[-1]
    temp[-1].replace(' ', '_').replace(':', '-')

    if all:
        fullPath=''
        for x in temp:fullPath+=x+'\\'
        return fullPath.removesuffix('\\')
    else:
        return temp[-1]


def initializeFilm(name: str, m3u8Path: str) -> None:
    try:
        temp = tempFolder(name)
        os.mkdir(temp)
    except:
        None

    if m3u8Path[-5:] != ".m3u8":
        m3u8Path += ".m3u8"
    shutil.move(m3u8Path, "%s\\.m3u8" % temp)


def initializeSerie(name: str, m3u8Path: str, season: int, episode: int) -> None:
    try:
        temp = os.getcwd()+'\\%s'%name
        if not os.path.exists(temp):
            os.mkdir(temp)
        os.mkdir('%s\\.%d_%d' % (temp, season, episode))
    except:
        None

    if m3u8Path[-5:] != ".m3u8":
        m3u8Path += ".m3u8"
    shutil.move(m3u8Path, '%s\\.%d_%d\\.m3u8' % (temp, season, episode))


# from:  C:\Developer\Programmi\film\4k\.film
# to:    film.mp4
def fileName(path: str) -> str:
    tempPath = path.split('\\')[-1]
    if tempPath[-4:] != ".mp4":
        tempPath += '.mp4'
    return tempPath.replace('_', ' ')


# from:  C:\Developer\Programmi\film\4k\.film
# from:  C:\Developer\Programmi\film\4k\film.mp4
# to:    C:\Developer\Programmi\film\4k\
def precFolder(path: str) -> str:
    temp = path.split('\\')[-1]
    return path.removesuffix(temp)
