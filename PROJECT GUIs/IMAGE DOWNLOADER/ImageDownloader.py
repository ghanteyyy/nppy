import os
import sys
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, font
import pygame
import requests
import pyperclip


class ImageDownloader:
    '''
    Image Downloader, a simple script written in Python that let you image
    from any website just by its address.

    Q. How to copy image address?
        1. Click on image.
        2. Right click on any part of the image.
        3. Click on copy image address.
    '''

    def __init__(self):
        self.IsDefault = True
        self.ErrorTimer = None
        self.extensions = ([('PNG', '*.png'), ('JPG', '*.jpg')])
        self.IconImagePath = self.ResourcePath('icon.ico')
        self.MainImagePath = self.ResourcePath('main.png')
        self.DownloadImagePath = self.ResourcePath('download.png')

        if sys.platform == 'win32':
            self.ErrAudioPath = self.ResourcePath('WinErrSound.wav')

        else:
            self.ErrAudioPath = self.ResourcePath('LinuxErrSound.wav')

        pygame.mixer.init()
        pygame.mixer.music.load(self.ErrAudioPath)

        self.Window = Tk()
        self.Window.withdraw()
        self.Window.title('Image Downloader')
        self.Window.iconbitmap(self.IconImagePath)

        self.MessageVar = StringVar()

        self.main_obj = PhotoImage(file=self.MainImagePath)
        self.LabelImage = Label(self.Window, image=self.main_obj, bd=0)
        self.LabelImage.grid(row=0, column=0, padx=5, sticky='w')

        self.style = ttk.Style()
        self.style.configure('E.TEntry', foreground='grey')

        self.container = Frame(self.Window, bg='white')
        self.LinkVar = StringVar()
        self.LinkVar.set('Image Address')

        self.LinkEntry = ttk.Entry(self.container, width=48, justify='center', textvariable=self.LinkVar, style='E.TEntry')
        self.LinkEntry.grid(row=0, column=0, padx=5, pady=15, ipady=5)

        self.DownloadImageObj = PhotoImage(file=self.DownloadImagePath)
        self.DownloadImageLabel = Label(self.container, image=self.DownloadImageObj, bg='white', cursor='hand2', takefocus=True)
        self.DownloadImageLabel.grid(row=0, column=1)
        self.container.grid(row=1, column=0)

        self.InitialPosition()

        self.LinkEntry.bind('<FocusIn>', self.FocusIn)
        self.Window.bind('<Button-3>', self.RightClick)
        self.LinkEntry.bind('<FocusOut>', self.FocusOut)
        self.Window.bind('<Button-1>', self.MasterBindings)
        self.DownloadImageLabel.bind('<Button-1>', self.DownloadImage)

        self.Window.config(bg='white')
        self.Window.mainloop()

    def InitialPosition(self, event=None):
        '''
        Set position of the window to the center of the screen when user open
        the program
        '''

        width, height = 340, 361
        ScreenWidth, ScreenHeight = self.Window.winfo_screenwidth() // 2, self.Window.winfo_screenheight() // 2

        self.Window.geometry(f'+{ScreenWidth - width // 2}+{ScreenHeight - height // 2}')
        self.Window.after(100, self.Window.deiconify)
        self.Window.resizable(0, 0)

    def MasterBindings(self, event=None):
        '''
        Focus to clicked widget
        '''

        event.widget.focus()

    def FocusOut(self, event=None, widget=None):
        '''
        When user clicks anywhere outside of entry boxes and buttons
        '''

        entry_get = self.LinkEntry.get().strip()

        if widget != self.DownloadImageLabel and not entry_get:
            self.IsDefault = True
            self.LinkVar.set('Image Address')
            self.style.configure('E.TEntry', foreground='grey')

    def FocusIn(self, event=None):
        '''
        When focus changes in or out of the entry widget
        '''

        if self.IsDefault:
            self.LinkVar.set('')
            self.IsDefault = False
            self.style.configure('E.TEntry', foreground='black')

    def DownloadImage(self, event=None):
        '''
        Download image from the given URL
        '''

        if self.IsDefault:
            self.ShowMessage('Provide valid URL')
            return

        if self.CheckInternet() is False:
            self.ShowMessage('No Internet Connection')
            return

        url = self.LinkVar.get().strip()

        try:
            response = requests.get(url)

        except requests.exceptions.MissingSchema:
            self.ShowMessage('Provide valid URL')
            return

        if response.headers['content-type'] not in ("image/png", "image/jpeg", "image/jpg"):  # Checking if provided link contains image file
            self.ShowMessage('Provided URL does not contain any image')
            return

        file_name = filedialog.asksaveasfilename(title='Save', filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

        if not file_name:
            return

        with open(file_name, 'wb') as f:
            f.write(response.content)

        self.ShowMessage('Download Completed !!', 'green')
        FILE_BROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        self.Window.after(50, lambda: subprocess.run([FILE_BROWSER_PATH, '/select,', os.path.normpath(file_name)]))

        self.LinkVar.set('Image Address')
        self.style.configure('E.TEntry', foreground='grey')

    def CheckInternet(self):
        '''
        Check if the user is connected to internet
        '''

        try:
            requests.get('http://www.google.com')

            return True

        except requests.ConnectionError:
            return False

    def ShowMessage(self, msg, fg='red'):
        '''
        Show any error message that user have encounter while downloading image
        or show download successful message
        '''

        self.MessageVar.set(msg)
        pygame.mixer.music.play()

        if self.ErrorTimer is None:
            self.ErrLabel = Label(self.Window, textvariable=self.MessageVar, bg='white', fg=fg, font=font.Font(size=10, weight='bold'))
            self.ErrLabel.grid(row=2, column=0, pady=(0, 10))

            self.ErrorTimer = self.Window.after(1600, self.RemoveErrorMessage)

        else:
            self.Window.after_cancel(self.ErrorTimer)
            self.ErrorTimer = None
            self.Window.after(0, lambda: self.ShowMessage(msg, fg))

    def RemoveErrorMessage(self):
        '''
        Remove the error messages after 1600 ms
        '''

        self.ErrLabel.grid_forget()
        self.ErrorTimer = None

    def RightClick(self, event):
        '''
        When user right clicks to Entry widget
        '''

        self.LinkEntry.focus()

        try:
            x, y = self.Window.winfo_pointerxy()

            RightClickMenu = Menu(self.Window, tearoff=0)
            RightClickMenu.add_command(label='Paste', accelerator='Ctrl+V', command=self.PasteFromClipBoard)

            RightClickMenu.post(x, y)

        finally:
            RightClickMenu.grab_release()

    def PasteFromClipBoard(self):
        '''
        Insert clipboard text to Entry widget
        '''

        ClipBoardText = pyperclip.paste()
        self.LinkVar.set(ClipBoardText)

    def ResourcePath(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    ImageDownloader()
