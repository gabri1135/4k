from tkinter import filedialog
from tkinter import *
import re

from get_m3u8 import M3U8
from downloader import *
from data import Data


class Graphic:

    def __init__(self, data: Data) -> None:
        self.data = data
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
        self.m3u8Bool = True
        self._localM3U8()

    def resume(self) -> None:
        temp = filedialog.askdirectory(parent=self.window)
        #progress = self.data.progressing[temp]["progress"]
        #path = self.data.progressing[temp]["path"]
        if re.split(r"\\|\/", temp)[-1][0] != '.':
            path = fileName(temp)
        else:
            os.chdir(precFolder(temp))
            path = re.split(r"\\|\/", temp)[-1][1:]

        self.window.destroy()
        Downloader(self.data, path, True)

    def _localM3U8(self) -> None:
        name = self.name_label.get()
        if name != '' and self.m3u8bool:
            initializeFilm(name, self.m3u8_file)
            # self.data.create(name)
            self.window.destroy()
            Downloader(self.data, name, False)
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
            Downloader(self.data, name, False)

        elif re.match(r".*seriehd\..*", url) != None:
            self.window.destroy()
            seasons = self._n('1')
            episodes = self._n('9')
            name = M3U8().getSerie(url, seasons, episodes)

            os.chdir("%s\\%s" % (os.getcwd(), name))
            for season in seasons:
                for episode in episodes:
                    Downloader(self.data, "%d_%d" %
                               (season+1, episode+1), False)
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
