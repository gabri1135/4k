from tkinter import StringVar, ttk

class PlaceHolderEntry(ttk.Entry):
    def __init__(self, root, placeholder:StringVar, *args, **kwargs) -> None:
        super().__init__(root, *args, **kwargs)
        self.placeholder = placeholder
        placeholder.trace_add("write",self._reset)

        self._reset()

    def on_click(self, e):
        self.configure(state="normal")
        self.delete(0, "end")

        # make the callback only work once
        self.unbind('<Button-1>', self.on_click_id)

    def _reset(self,*args):
        self.delete(0, "end")
        self.insert("0", self.placeholder.get())
        self.on_click_id = self.bind('<Button-1>', self.on_click)
