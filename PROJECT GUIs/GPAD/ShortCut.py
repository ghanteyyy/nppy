from tkinter import *
from tkinter.font import Font


class ShortCut:
    def __init__(self, master):
        self.master = master
        self.font = Font(size=8)

    def ShowShortCut(self, button, text, rely=None):
        '''
        Show text aside of the button when the cursor enters to the button
        '''

        self.label = Label(self.master, text=text, border='1', relief='solid', font=self.font)

        if rely:
            self.id = self.master.after(800, lambda: self.label.place(in_=button, relx=0.7, x=0, rely=0))

        else:
            self.id = self.master.after(800, lambda: self.label.place(in_=button, relx=0, x=0, rely=1.0))

    def destroy(self):
        '''
        Remove text when the cursor leaves the button
        '''

        self.master.after_cancel(self.id)
        self.label.place_forget()
