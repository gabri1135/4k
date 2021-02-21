import os

def tempFolder(path):
    if path[-4:4] == ".mp4":
        path = path.removesuffix(
            '.mp4')
    tempName = path.split('\\')[-1].replace(' ', '_')
    return '%s\\.%s' % (os.getcwd(), tempName)
