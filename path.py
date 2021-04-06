import os
import re
import shutil


class PathModel:
    def __init__(self, _path: str) -> None:
        self.path = os.path.abspath(_path)
        self.isFile = self.path.split('.')[-1] in ['mp4', 'm3u8', 'json']
        self.name = os.path.basename(self.path)
        self.dir = os.path.dirname(self.path)

    def create(self) -> bool:
        if not self.isFile and not os.path.exists(self.path):
            os.mkdir(self.path)
            return True
        return False

    def add(self, _folder) -> PathModel:
        if not self.isFile:
            return PathModel(self.path+'\\'+_folder)
        return self

    def exist(self) -> bool:
        return os.path.exists(self.path)

    def remove(self) -> None:
        if self.isFile:
            os.remove(self.path)
        else:
            shutil.rmtree(self.path)

    def move(self, to: PathModel) -> None:
        shutil.move(self.path, to.path)

    def read(self) -> str:
        return open(self.path, "r").read()

    def write(self, text: str, type: str) -> None:
        open(self.path, type).write(text)

    def duplicate(self) -> PathModel:
        temp = re.findall(r"(.*)\.(.*)", self.name)[0]
        id = 1
        while PathModel(self.dir).add(f"{temp[0]}({id}).{temp[1]}").temp().exist():
            id += 1

        return PathModel(self.dir).add(f"{temp[0]}({id}).{temp[1]}")

    def temp(self, space='.') -> PathModel:
        if self.name[-4:] == '.mp4':
            _name = self.name.removesuffix('.mp4')
        else:
            _name = self.name

        return PathModel(os.getcwd()).add(f"{space}{_name}")
