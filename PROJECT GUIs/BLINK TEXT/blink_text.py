import os
import sys

try:
    from tkinter import *

except (ImportError, ModuleNotFoundError):
    from Tkinter import *


class Blink:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('included files/icon.ico'))
        self.master.title('Blinking Text')
        self.master.geometry('365x115+{}+{}'.format(self.master.winfo_screenwidth() // 2 - 365 // 2, self.master.winfo_screenheight() // 2 - 115 // 2))

        self.frame = Frame(self.master, bg='#422a91')
        self.frame.pack()

        self.entry = Entry(self.frame, width=15, font=('Courier', 15, 'bold'), fg='grey', justify='center')
        self.entry.insert(END, 'TEXT')
        self.entry.pack(pady=10, side=LEFT)

        self.add = Button(self.frame, text='ADD', fg='white', bg='#422a91', activebackground='#422a91', activeforeground='white', relief=GROOVE, cursor='hand2', command=self.add_button_command)
        self.add.pack(side=LEFT, padx=10, ipadx=15, ipady=3)

        self.text = Label(self.master, text='Blink', fg='white', bg='#422a91', font=('Courier', 20))  # Creating label object
        self.text.pack(pady=10)

        self.blink()

        self.entry.bind('<Return>', lambda e: self.add_button_command())
        self.entry.bind('<Button-1>', lambda e: self.button_1_command())
        self.entry.bind('<Leave>', lambda e: self.leave())

        self.master.config(bg='#422a91')

    def button_1_command(self):
        '''Binding function for left click'''

        if self.entry.get() == 'TEXT':
            self.entry.delete(0, END)
            self.entry.config(fg='black')

    def leave(self):
        '''Binding function when the cursor leaves the entry box'''

        if not self.entry.get().strip():
            self.entry.delete(0, END)
            self.entry.insert(END, 'TEXT')
            self.entry.config(fg='grey')
            self.master.focus()

    def blink(self):
        '''Change color of text between #422a91 and white every 100 milliseconds'''

        if self.text['fg'] == '#422a91':
            self.text['fg'] = 'white'

        else:
            self.text['fg'] = '#422a91'

        self.master.after(100, self.blink)

    def add_button_command(self):
        '''Function for "ADD" button'''

        get_from_entry = self.entry.get().strip()

        if get_from_entry:
            self.text.config(text=get_from_entry)

        else:
            self.text.config(text='Blink')

        self.entry.delete(0, END)
        self.leave()

    def resource_path(self, relative_path):
        """ Get absolute path to resource from temporary directory

        In development:
            Gets path of photos that are used in this script like in icons and title_image from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of photos that are used in this script like in icons and title image from temporary directory"""

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path in _MEIPASS

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    root = Tk()
    Blink(root)
    root.mainloop()
