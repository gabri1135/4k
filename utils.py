import shutil
import os
from enum import Enum


def tempFolder(path, all=True):
    if path[-4:] == ".mp4":
        path = path.removesuffix(
            '.mp4')
    tempName = path.split('\\')[-1].replace(' ', '_')
    if all:
        return '%s\\.%s' % (os.getcwd(), tempName)
    else:
        return '.%s' % tempName


def initialize(name, m3u8Path):
    try:
        temp = tempFolder(name)
        os.mkdir(temp)
    except: None
    shutil.move("%s.m3u8" % m3u8Path, "%s\\.m3u8" % temp)

def realPath(tempPath):
    tempPath=tempPath[1:]
    return tempPath.replace('_', ' ')
