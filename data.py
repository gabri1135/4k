import json
import os
from re import A
from utils import tempFolder


class Data:
    def __init__(self):
        if not os.path.exists('data.json'):
            open('data.json', 'w').write(json.dumps({"progressing": {},
                                          "complete": {}}))

        data = json.loads(open('data.json', 'r').read())
        self.progressing = data["progressing"]
        self.complete = data["complete"]

    def create(self, path):
        tempName = tempFolder(path,all=False)
        temp={tempName:{"path": path, "progress": 0}}
        self.progressing.update(temp)
        self.write

    def update(self, tempName, progress):
        self.progressing[tempName]["progress"] = progress
        self.write

    def done(self, tempName, name):
        self.complete.append(name)
        del self.progressing[tempName]
        self.write

    def write(self):
        temp = json.dumps({"progressing": self.progressing,
                          "complete": self.complete})
        open('data.json', 'w').write(temp)
