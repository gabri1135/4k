from data import Data
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from downloader import *
from get_m3u8 import M3U8


# messagebox.askyesno("Account checker","Errore!\n"+str(err)+" combos non sono state scritte correttamente!\nVolete modificarle?")):
#messagebox.showinfo("Account cheker","Inizio controllo combos")
#messagebox.showerror("Account checker","Inserire combos")


# def control():
#    stop=0
#    clear()
#    text_input['height']='5'
#    progress = ttk.Progressbar(window, mode = 'determinate',orient="horizontal",length=350)
#    progress.grid(row=6,column=0,columnspan=3,sticky="NW",padx=5,pady=5)
#    clear_button.destroy();start_button.destroy()
#    out=tk.Label(window,textvariable=text)
#    out.grid(row=3,column=1,rowspan=2,pady=5)
#    load_button['text']='Stop';window.update()
#    for i in range(len(mail)):
#        window.update()
#        if stop==1: break
#        time.sleep(1)
#        ok.append(mail[i]+":"+pas[i])
#        text_input.insert(tk.END,mail[i]+":"+pas[i]+"\n")
#        text.set("Checked: "+str(i+1)+" su "+str(len(mail))+"\nFree: "+" su "+str(i+1)+"\nLoad: "+str(int((i+1)/len(mail)*100))+"%")
#        progress['value']=int((i+1)/len(mail)*100);window.update()
#    if len(ok)!=0:
#        if messagebox.askyesno("Account checker","Sono stati recuperati "+str(len(ok))+" account\nVolete salvarli?"):
#            account=open(filedialog.asksaveasfilename(filetypes=[('File di testo','*.txt')],defaultextension='.txt'),"w")
#            for line in ok:
#                account.write(line+"\n")
#            account.close()
#    else:
#        messagebox.showinfo("Account checker","Non sono stati recuperati account")
#    window.destroy()
class Graphic:

    def __init__(self, data: Data):
        self.data = data
        self.m3u8File=False

        self.window = Tk()

        self.window.geometry("258x135")
        self.window.title("4K downloader")

        label = Label(
            self.window, text="Benvenuto nel 4k downloader per scaricare film")
        label.grid(row=0, column=0, columnspan=3, sticky="WE")

        self.url_label = Entry(
            self.window, text="Url altadefinizione")
        self.url_label.grid(row=1, column=0, columnspan=2, sticky="WE", padx=5, pady=2.5)

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

    def load(self):
        self.m3u8_file = filedialog.askopenfilename(
            parent=self.window, filetypes=[('File m3u8', '*.m3u8')])
        self.resume_button.config(state='disabled')
        self.m3u8_file=True
        name = self.name_label.get()
        if name != '':
            initialize(name)
            #self.data.create(name)
            Downloader(self, self.data, name)

    def start(self):
        name=self.name_label.get()
        url=self.url_label.get()
        if url!='':
            name=M3U8().get(url)
            #self.data.create(name)
            Downloader(self, self.data, name)
        elif self.m3u8File and name!='':
            initialize(name, self.m3u8_file)
            self.data.create(name)
            Downloader(self, self.data, name)

    def resume(self):
        temp = filedialog.askdirectory(parent=self.window)
        temp = temp.split('\\')[-1]
        #progress = self.data.progressing[temp]["progress"]
        #path = self.data.progressing[temp]["path"]
        temp=temp.split('/')[-1]
        path=realPath(temp)
        Downloader(self, self.data, path)

    def error(self, title, message):
        messagebox.showerror(title, message)
