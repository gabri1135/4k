from serie import Serie
from tkinter import filedialog
from tkinter import *
from os import path as Path, getcwd, listdir
import re

from get_m3u8 import M3U8
from downloader import *


class Graphic:

    def __init__(self) -> None:
        self.m3u8Bool = False

        self.window = Tk()

        self.window.geometry("258x135")
        self.window.title("4K downloader")

        label = Label(
            self.window, text="Benvenuto nel 4k downloader per scaricare film")
        label.grid(row=0, column=0, columnspan=3, sticky="WE")

        self.url_label = Entry(
            self.window, text="Url altadefinizione")
        self.url_label.grid(row=1, column=0, columnspan=2,
                            sticky="WE", padx=5, pady=2.5)

        self.load_button = Button(
            self.window, text="File m3u8", command=self.load)
        self.load_button.grid(row=2, column=0, sticky="WE", padx=5, pady=2.5)

        self.name_label = Entry(
            self.window, text="Output file")
        self.name_label.grid(row=2, column=1, sticky="WE", padx=5, pady=2.5)

        self.resume_button = Button(
            self.window, text="Riprendi download", command=self.resume)
        self.resume_button.grid(
            row=3, column=0, columnspan=2, sticky="WE", padx=5, pady=2.5)

        self.start_button = Button(
            self.window, text="Start", command=self.start)
        self.start_button.grid(row=1, column=2, rowspan=3,
                               sticky="NSWE", padx=5, pady=2.5)

        by = Label(self.window, text="by Gabriele Martini")
        by.grid(row=4, column=0, columnspan=3, sticky="WE")

        self.window.mainloop()

    def start(self) -> None:
        if not self._networkM3U8():
            self._localM3U8()

    def load(self) -> None:
        self.m3u8_file = filedialog.askopenfilename(
            parent=self.window, filetypes=[('File m3u8', '*.m3u8')])
        self.resume_button.config(state='disabled')
        self.url_label.config(state='disabled')
        self.m3u8Bool = True
        self._localM3U8()

    def resume(self) -> None:
        temp = filedialog.askdirectory(parent=self.window)

        if Path.basename(temp)[0] == '.':
            if Path.dirname(Path.abspath(temp)) == getcwd():
                _path = fileName(temp)
            else:
                os.chdir(Path.dirname(temp))
                _path = Path.basename(temp)[1:]
        else:
            os.chdir(temp)
            _path = []
            for file in listdir():
                if Path.basename(file)[0] == '.':
                    _path.append(Path.basename(file)[1:])

        self.window.destroy()
        for path in list(_path):
            Downloader(path)

    def _localM3U8(self) -> None:
        name = self.name_label.get()
        if name != '' and self.m3u8bool:
            initializeFilm(name, self.m3u8_file)
            self.window.destroy()
            Downloader(name)
            return True
        return False

    def _networkM3U8(self) -> bool:
        url = self.url_label.get()
        if url == '':
            return False
        if re.match(r'.*altadefinizionecommunity\.net\/.*', url) != None:
            self.window.destroy()
            name = M3U8().getFilm(url)
            # self.data.create(name)
            Downloader(name)

        elif re.match(r".*seriehd\..*", url) != None:
            self.window.destroy()
            serie = Serie(url)
            #seasons = self._n(input("Seasons: "))
            # if len(seasons) == 1:
            #    episodes = self._n(input("Episodes: "))
            # else:
            #    episodes = {}
            dict = {5: [0]}
            last = [5]
            all = serie.check(dict, last)
            M3U8().getSerie(serie.name, serie.url, all)

            os.chdir("%s\\%s" % (os.getcwd(), serie.name))
            for episode in all:
                Downloader("%d_%d" % (episode[0]+1, episode[1]+1))

        return True

    def _n(self, input: str) -> set(int):
        if input == '':
            return {}

        prec = False
        list = input.split(',')

        for i in range(len(list)):
            if list[i] == '...':
                prec = True
            elif prec:
                list[i] = int(list[i])-1
                [list.append(item) for item in range(list[i-2], list[i])]
                prec = False
            else:
                list[i] = int(list[i])-1
        ep = set(list)
        try:
            ep.remove('...')
        except:
            None
        return ep
