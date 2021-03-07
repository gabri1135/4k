from os import path as Path, getcwd, mkdir, remove
import shutil
import re

# from:  film
# from:  film.mp4
# to:    C:\Developer\Programmi\film\4k\.film


def tempFolder(_name: str) -> str:
    if _name[-4:] == '.mp4':
        _name = _name.removesuffix('.mp4')

    _name = '.'+_name
    _name.replace(' ', '_').replace(':', '-')

    return getcwd()+'\\'+_name


def initializeFilm(name: str, m3u8Path: str) -> bool:
    _temp = tempFolder(name)
    if Path.exists(_temp):
        remove(m3u8Path)
        return False

    mkdir(_temp)
    shutil.move(m3u8Path, "%s\\.m3u8" % _temp)
    open("%s\\temp.txt" % _temp, 'w').write("ffconcat version 1.0\n\n")
    return True


def initializeSerie(name: str, m3u8Path: str, detail: tuple) -> bool:
    temp = getcwd()+'\\%s' % name
    if not Path.exists(temp):
        mkdir(temp)

    temp += '\\.%d_%d' % (detail[0]+1, detail[1]+1)

    if Path.exists(temp):
        remove(m3u8Path)
        return False

    mkdir(temp)
    shutil.move(m3u8Path, '%s\\.m3u8' % temp)

    open("%s\\temp.txt" % temp,
         'w').write("ffconcat version 1.0\n\n")
    return True


# from:  C:\Developer\Programmi\film\4k\.film
# to:    film.mp4
def fileName(_path: str) -> str:
    tempPath = Path.basename(_path)
    if Path.isdir(_path):
        tempPath += '.mp4'
    return tempPath[1:].replace('_', ' ')
