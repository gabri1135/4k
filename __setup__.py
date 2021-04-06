import os

libs = [
    "requests",
    "selenium",
    "pycryptodome"
]

os.system("python -m pip install --upgrade pip")

for lib in libs:
    os.system("python -m pip install {}".format(lib))
