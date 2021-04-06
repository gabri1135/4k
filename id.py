class Id:
    def __init__(self, length: int, start: int):
        self.length = len(str(length))
        self.start = start

    def add(self) -> str:
        s = str(self.start)
        s = (self.length-len(str(s)))*'0'+s
        self.start += 1
        return s

    def get(self):
        s = str(self.start)
        s = (self.length-len(str(s)))*'0'+s
        return s
