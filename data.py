import json
import os
from typing import Literal
from path import PathModel


class Data:
    def __init__(self) -> None:
        if os.path.exists('data.json'):
            self.out = dict(json.loads(open('data.json', 'r').read()))
        else:
            self.out = {}

    @staticmethod
    def create(_outputFile: PathModel) -> Literal['created', 'exist', 'outPath different']:
        self = Data()
        if not _outputFile.name in self.out.keys():
            self.out[_outputFile.name] = _outputFile.path
            self.write()
            return 'created'

        if self.out[_outputFile.name] == _outputFile.path:
            return 'exist'

        return 'outPath different'

    @staticmethod
    def update(_outputFolder: PathModel) -> None:
        self = Data()
        self.out.update({_outputFolder.name: _outputFolder.path})

        self.write()

    @staticmethod
    def delete(name: str) -> None:
        self = Data()
        if name in self.out.keys():
            self.out.pop(name)
            self.write()

    @staticmethod
    def get(name: str) -> PathModel | None:
        self = Data()
        if name in self.out.keys():
            return PathModel(self.out.get(name))
        return None

    def write(self):
        temp = json.dumps(self.out)
        open('data.json', 'w').write(temp)
