import os
import sys

try:
    from tkinter import *

except (ImportError, ModuleNotFoundError):
    from Tkinter import *


class Blink:
    '''Show and hide the given text such that it appears as blinking'''

    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.after(0, self.master.deiconify)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))
        self.master.title('Blinking Text')

        self.width, self.height = 302, 99
        self.master.geometry(f'{self.width}x{self.height}+{self.master.winfo_screenwidth() // 2 - self.width // 2}+{self.master.winfo_screenheight() // 2 - self.height // 2}')

        self.frame = Frame(self.master, bg='#422a91')
        self.frame.pack()

        self.entry_var = StringVar()
        self.entry = Entry(self.frame, width=15, font=('Courier', 15, 'bold'), fg='grey', justify='center', textvariable=self.entry_var)
        self.entry_var.set('TEXT')
        self.entry.pack(pady=10, ipady=2, side=LEFT)

        self.add_button = Button(self.frame, text='ADD', fg='white', bg='#422a91', activebackground='#422a91', activeforeground='white', relief=GROOVE, cursor='hand2', command=self.add_button_command)
        self.add_button.pack(side=LEFT, padx=10, ipadx=15, ipady=3)

        self.text = Label(self.master, text='Blink', fg='white', bg='#422a91', font=('Courier', 20))
        self.text.pack(pady=2)

        self.entry.bind('<FocusIn>', self.bind_keys)
        self.master.bind('<Button-1>', self.bind_keys)
        self.add_button.bind('<FocusIn>', self.bind_keys)
        self.entry.bind('<Return>', self.add_button_command)
        self.add_button.bind('<Return>', self.add_button_command)

        self.master.after(0, self.blink)
        self.master.config(bg='#422a91')
        self.master.mainloop()

    def bind_keys(self, event):
        '''Commands when user clicks in and out of the entry widget'''

        entry_get = self.entry.get().strip()

        if event.widget == self.entry:
            if entry_get == 'TEXT':
                self.entry_var.set('')
                self.entry.config(fg='black')

        else:
            if not entry_get:
                self.entry_var.set('TEXT')
                self.entry.config(fg='grey')

        if event.widget in [self.master, self.text]:
            self.master.focus()

    def blink(self):
        '''Change color of text between #422a91 and white every 100 milliseconds'''

        if self.text['fg'] == '#422a91':
            self.text['fg'] = 'white'

        else:
            self.text['fg'] = '#422a91'

        self.master.after(100, self.blink)

    def add_button_command(self, event=None):
        '''Command for "ADD" button'''

        get_from_entry = self.entry.get().strip()

        if get_from_entry:
            self.text.config(text=get_from_entry)

        else:
            self.text.config(text='Blink')

        self.master.focus()
        self.entry.delete(0, END)
        self.entry_var.set('TEXT')
        self.entry.config(fg='grey')

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS.

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Blink()
