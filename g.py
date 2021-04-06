from get_m3u8 import DownloadM3U8
from typing import List, Tuple
from data import Data
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from placeHolder import PlaceHolderEntry
import os
import re

from serie import Serie
from film import Film

from path import PathModel
from downloader import Downloader


class Home():
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry("221x135")
        self.root.title("4k Downloader")

        # input
        self.box = BooleanVar(value=False)
        self.outBool = BooleanVar(value=False)
        self.str = StringVar()
        self.m3u8Path = ''

        # variable text
        self.button = StringVar(value="Riprendi")
        self.entry = StringVar(value="Url film/serie")

        self.main = Frame(self.root)
        self.main.grid(column=0, columnspan=2, row=2)

        Label(self.root, text="Benvenuto nel 4k downloader").grid(
            row=0, column=0, columnspan=2, padx=5, sticky="WE")

        ttk.Radiobutton(self.root, text='Web', value=False, width=14, command=self._change,
                        variable=self.box).grid(column=0, row=1)
        ttk.Radiobutton(self.root, text='Local', value=True, width=14, command=self._change,
                        variable=self.box).grid(column=1, row=1)

        PlaceHolderEntry(
            self.main, self.entry, textvariable=self.str).grid(
                column=0, row=0, padx=2.5, pady=1, sticky="WE")

        ttk.Button(self.main, textvariable=self.button, command=self._load, width=25).grid(
            column=0, row=1, padx=2.5, pady=1, sticky="WE")

        ttk.Button(
            self.main, text="Start", command=self._start, width=6).grid(
                column=2, row=0, rowspan=3, padx=5, pady=1, sticky="NS")

        ttk.Checkbutton(self.main, text="Seleziona cartella output", variable=self.outBool,
                        onvalue=True, offvalue=False).grid(row=2, column=0, padx=5, pady=1, sticky="WE")

        Label(self.root, text="by Gabriele Martini").grid(
            row=3, column=0, columnspan=2, sticky="WE")

        self.root.mainloop()

    def _change(self):
        if self.box.get():
            self.button.set("M3U8 file")
            self.entry.set("Nome film")
        else:
            self.button.set("Riprendi")
            self.entry.set("Url film/serie")

    def _load(self) -> None:
        if self.box.get():
            self.m3u8Path = filedialog.askopenfilename(
                parent=self.root, filetypes=[('File m3u8', '*.m3u8')])
            print(self.m3u8Path)
        else:
            temp = filedialog.askdirectory(parent=self.root)
            print(temp)

    def _start(self):
        if not self.str.get() in ["Nome film", "Url film/serie"]:
            if self.box.get():
                self._localM3U8(self.str.get())
            else:
                self._networkM3U8(self.str.get())

    def _localM3U8(self, _name) -> None:
        if _name != '' and self.m3u8Path != '':
            outputPath = self.output().add(f'{_name}.mp4')
            initialized = Film.initialize(outputPath, PathModel(self.m3u8Path))
            if initialized=="created":
                self.root.destroy()
                Downloader(outputPath)
            else:
                print(initialized)

    def _networkM3U8(self, url: str) -> None:
        url = url.replace("www.", "").removeprefix("https://")
        filmName = re.findall(
            r"[altadefinizione\..*|altadefinizionecommunity\.net]\/(.*/)", url)
        serieName = re.findall(r"seriehd\..*\/(.*/)", url)

        if filmName != []:
            out = self.output()
            self.root.destroy()
            film = Film(filmName[0], out)

            if film.init[0]== 'created':
                Downloader(film.outputFile)
            elif film.init[0]=="continuare":
                messagebox.showinfo(
                    "4K Downloader", "Download già iniziato, verrà ripreso")
                Downloader(film.outputFile)
            elif film.init[0]=="sostituire":
                s = messagebox.askyesno("4K Downloader",
                                        "Nome già esistente ma i file sono diversi.\nSi -> Indicizza file\nNo -> Sostituisci file")

                if s:
                    film.outputFile = film.outputFile.duplicate()
                else:
                    film.outputFile.temp().remove()
                    Data.delete(film.outputFile.name)

                Film.initialize(film.outputFile, film.m3u8Path)
                Downloader(film.outputFile)
  #          elif film.init[0]=='outPath different':
                

 #       elif serieName != []:
 #           height = self.main.winfo_height()
 #           self.main.destroy()
 #           self.stagioni = StringVar()
 #           self.episodi = StringVar()
#
 #           self.serie = Serie(serieName[0])
#
 #           self.main = Frame(self.root, height=height)
 #           self.main.grid(column=0, columnspan=2, row=2)
#
 #           Label(self.main, text=self.serie.name).grid(column=0, row=0)
#
 #           PlaceHolderEntry(
 #               self.main, StringVar(self.root, value="Stagioni"), textvariable=self.stagioni, width=25).grid(
 #               column=0, row=1, padx=2.5, pady=1, sticky="WE")
#
 #           PlaceHolderEntry(
 #               self.main, StringVar(self.root, value="Episodi"), textvariable=self.episodi).grid(
 #               column=0, row=2, padx=2.5, pady=1, sticky="WE")
#
 #           ttk.Button(
 #               self.main, text="Start", command=self._serie, width=6).grid(
 #               column=2, row=0, rowspan=3, padx=5, pady=1, sticky="NS")
#
    def _serie(self) -> None:
        out = self.output()
        out = self.serie.init(out)

        stagioni = self.stagioni.get()
        episodi = self.episodi.get()

        lStagioni, all = self._n(stagioni)

        if len(lStagioni) == 1:
            lStagioni = lStagioni[0]
            lEpisodi, all = self._n(episodi)
            result = self.serie.check({lStagioni: lEpisodi},
                                      [lStagioni] if all else [])
        else:
            if all:
                for x in range(lStagioni[-1]+1, len(self.serie.all)):
                    lStagioni.append(x)

            result = self.serie.check({x: 0 for x in lStagioni}, lStagioni)

        self.root.destroy()
        DownloadM3U8().getSerie(out, self.serie.url, result)
        os.chdir(out.temp(space='').path)
        for episode in result:
            Downloader(out.add("%d_%d.mp4" % (
                episode[0]+1, episode[1]+1)), _tempFolder=out.add(".%d_%d" % (episode[0]+1, episode[1]+1)))

    def _n(self, input: str) -> Tuple[List[int], bool]:
        _list = input.replace(",-,", "-").split(",")

        _all = []
        for x in _list:
            temp = re.findall(r"(\d)-(\d?)", x)

            if len(temp) == 1:
                if temp[0][1] != '':
                    for k in range(int(temp[0][0])-1, int(temp[0][1])):
                        _all.append(k)
                else:
                    _all.append(int(temp[0][0])-1)
                    temp = list(set(_all))
                    temp.sort()
                    return temp, True
            else:
                _all.append(int(x)-1)

        temp = list(set(_all))
        temp.sort()
        return temp, False

    def output(self) -> PathModel:
        if self.outBool.get():
            return PathModel(filedialog.askdirectory(parent=self.root))
        else:
            return PathModel(os.getcwd())
