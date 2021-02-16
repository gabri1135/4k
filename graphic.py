from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from v3 import *


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

    def __init__(self):
        self.m3u8_bool=False
        self.output_bool=False

        self.window = Tk()

        self.window.geometry("258x106")
        self.window.title("4K downloader")

        label = Label(
            self.window, text="Benvenuto nel 4k downloader per scaricare film")
        label.grid(row=0, column=0, columnspan=3, sticky="WE")

        load_button = Button(text="File m3u8", command=self.load)
        load_button.grid(row=1, column=0, sticky="WE", padx=5, pady=2.5)
        
        save_button = Button(text="Output file", command=self.save)
        save_button.grid(row=1, column=1, sticky="WE", padx=5, pady=2.5)

        resume_button = Button(text="Riprendi download", command=self.resume)
        resume_button.grid(row=2, column=0,columnspan=2, sticky="WE", padx=5, pady=2.5)

        self.start_button = Button(text="Start", command=self.start,state='disabled')
        self.start_button.grid(row=1, column=2,rowspan=2, sticky="NSWE", padx=5, pady=2.5)

        by = Label(self.window, text="by Gabriele Martini")
        by.grid(row=3, column=0, columnspan=3, sticky="WE")

        self.window.mainloop()

    def load(self):
        self.m3u8_file = filedialog.askopenfilename(
            parent=self.window, filetypes=[('File m3u8', '*.m3u8')])
        self.m3u8_bool=True
        self.check()

    def save(self):
        self.output_file = filedialog.asksaveasfilename(
            parent=self.window, filetypes=[('File MP4', '*.mp4')])
        try:
            if(self.output_file[-4:] != ".mp4"):
                self.output_file += ".mp4"
        except:
            self.output_file += ".mp4"
        self.output_bool=True
        self.check()
    
    def resume(self):
        temp=filedialog.askdirectory(parent=self.window)
        data=open("%s/data.txt"%temp).read().split()
        self.m3u8_file=data[0]
        self.output_file=data[1]
        self.m3u8_bool=True
        self.output_bool=True
        self.check()

    def start(self):
        Downloader(self, self.m3u8_file, self.output_file)
    
    def error(self, title, message):
        messagebox.showerror(title,message)

    def check(self):
        if(self.m3u8_bool and self.output_bool):
            self.start_button.config(state='active')

if __name__ == "__main__":
    Graphic()
