import os
import sys
import socket
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, font
import pygame
import requests


class Image_Downloader:
    '''
    Image Downloader, a simple script written in Python that let you
    image from any website just by its address.

    Q. How to copy image address?
        1. Click on image.
        2. Right click on any part of the image.
        3. Click on copy image address.
    '''

    def __init__(self):
        self.ErrorTimer = None
        self.extensions = ([('PNG', '*.png'), ('JPG', '*.jpg')])
        self.icon_path = self.ResourcePath('icon.ico')
        self.main_path = self.ResourcePath('main.png')
        self.download_path = self.ResourcePath('download.png')

        if sys.platform == 'win32':
            self.ErrAudioPath = self.ResourcePath('WinErrSound.wav')

        else:
            self.ErrAudioPath = self.ResourcePath('LinuxErrSound.wav')

        pygame.mixer.init()
        pygame.mixer.music.load(self.ErrAudioPath)

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Image Downloader')
        self.master.iconbitmap(self.icon_path)

        self.main_obj = PhotoImage(file=self.main_path)
        self.label_image = Label(self.master, image=self.main_obj, bd=0)
        self.label_image.grid(row=0, column=0, padx=5, sticky='w')

        self.style = ttk.Style()
        self.style.configure('E.TEntry', foreground='grey')

        self.container = Frame(self.master, bg='white')
        self.link_var = StringVar()
        self.link_var.set('Image Address')

        self.link_entry = ttk.Entry(self.container, width=48, justify='center', textvariable=self.link_var, style='E.TEntry')
        self.link_entry.grid(row=0, column=0, padx=5, pady=15, ipady=5)

        self.download_image_obj = PhotoImage(file=self.download_path)
        self.download_image_label = Label(self.container, image=self.download_image_obj, bg='white', cursor='hand2', takefocus=True)
        self.download_image_label.grid(row=0, column=1)
        self.container.grid(row=1, column=0)

        self.InitialPosition()

        self.MessageVar = StringVar()

        self.master.bind('<Button-1>', self.MasterBindings)
        self.download_image_label.bind('<Button-1>', self.DownloadImage)
        self.link_entry.bind('<FocusIn>', self.EntryBindings)
        self.download_image_label.bind('<FocusIn>', self.EntryBindings)
        self.master.config(bg='white')
        self.master.mainloop()

    def InitialPosition(self, event=None):
        '''Set position of the window to the center of the screen when user open the program'''

        width, height = 340, 361
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2

        self.master.geometry(f'+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.after(100, self.master.deiconify)
        self.master.resizable(0, 0)

    def MasterBindings(self, event=None, widget=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        if widget is None:
            widget = event.widget

        if widget != self.link_entry:
            if not self.link_var.get().strip():
                self.link_var.set('Image Address')
                self.style.configure('E.TEntry', foreground='grey')

            self.master.focus()

    def EntryBindings(self, event=None):
        '''When focus changes in or out of the entry widget'''

        widget = event.widget

        if widget == self.link_entry:
            if self.link_var.get().strip() == 'Image Address':
                self.link_var.set('')
                self.style.configure('E.TEntry', foreground='black')

        else:
            self.MasterBindings(widget=self.master)

    def DownloadImage(self, event=None):
        '''Download image from the given URL'''

        if self.CheckInternet():
            url = self.link_var.get().strip()

            response = requests.get(url)

            if response.headers['content-type'] in ("image/png", "image/jpeg", "image/jpg"):  # Validate if provided URL contains image file
                file_name = filedialog.asksaveasfilename(title='Save', filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

                if file_name:
                    with open(file_name, 'wb') as f:
                        f.write(response.content)

                    self.ShowMessage('Download Completed !!', 'green')
                    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
                    self.master.after(50, lambda: subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(file_name)]))

                    self.link_var.set('Image Address')
                    self.style.configure('E.TEntry', foreground='grey')

            else:
                self.ShowMessage('Provided URL does not contain any image')

        else:
            self.ShowMessage('No Internet Connection')

    def CheckInternet(self):
        '''Check if the user is connected to internet'''

        try:
            socket.create_connection(("1.1.1.1", 53))
            return True

        except OSError:
            pass

        return False

    def ShowMessage(self, msg, fg='red'):
        '''
        Show any error message that user have encounter while
        downloading image or show download successful message
        '''

        self.MessageVar.set(msg)
        pygame.mixer.music.play()

        if self.ErrorTimer is None:
            self.ErrLabel = Label(self.master, textvariable=self.MessageVar, bg='white', fg=fg, font=font.Font(size=10, weight='bold'))
            self.ErrLabel.grid(row=2, column=0, pady=(0, 10))

            self.ErrorTimer = self.master.after(1600, self.RemoveErrorMessage)

        else:
            self.master.after_cancel(self.ErrorTimer)
            self.ErrorTimer = None
            self.master.after(0, lambda: self.ShowMessage(msg, fg))

    def RemoveErrorMessage(self):
        '''Remove the error messages after 1600 ms'''

        self.ErrLabel.grid_forget()
        self.ErrorTimer = None

    def ResourcePath(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    Image_Downloader()
