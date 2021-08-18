import os
import sys
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox
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
        self.extensions = ([('PNG', '*.png'), ('JPG', '*.jpg')])
        self.icon_path = self.resource_path('included_files\\icon.ico')
        self.main_path = self.resource_path('included_files\\main.png')
        self.download_path = self.resource_path('included_files\\download.png')

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

        self.master.after(0, self.initial_position)

        self.master.bind('<Button-1>', self.master_binding)
        self.download_image_label.bind('<Button-1>', self.download_image)
        self.link_entry.bind('<FocusIn>', self.entry_binding)
        self.download_image_label.bind('<FocusIn>', self.entry_binding)
        self.master.config(bg='white')
        self.master.mainloop()

    def initial_position(self, event=None):
        '''Set position of the window to the center of the screen when user open the program'''

        width, height = 340, 361
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2

        self.master.geometry(f'+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.deiconify()
        self.master.resizable(0, 0)

    def master_binding(self, event=None, widget=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        if widget is None:
            widget = event.widget

        if widget != self.link_entry:
            if not self.link_var.get().strip():
                self.link_var.set('Image Address')
                self.style.configure('E.TEntry', foreground='grey')

            self.master.focus()

    def entry_binding(self, event=None):
        '''When focus changes in or out of the entry widget'''

        widget = event.widget

        if widget == self.link_entry:
            if self.link_var.get().strip() == 'Image Address':
                self.link_var.set('')
                self.style.configure('E.TEntry', foreground='black')

        else:
            self.master_binding(widget=self.master)

    def download_image(self, event=None):
        '''Download image from the given URL'''

        try:
            url = self.link_var.get().strip()

            response = requests.get(url)

            if response.headers['content-type'] in ("image/png", "image/jpeg", "image/jpg"):  # Validate if provided URL contains image file
                file_name = filedialog.asksaveasfilename(title='Save', filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

                if file_name:
                    with open(file_name, 'wb') as f:
                        f.write(response.content)

                    messagebox.showinfo('Complete', 'Download Completed !!')
                    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
                    self.master.after(50, lambda: subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(file_name)]))

                    self.link_var.set('Image Address')
                    self.style.configure('E.TEntry', foreground='grey')

            else:
                messagebox.showerror('ERR', 'Provided URL does not contain any image')

        except requests.ConnectionError:
            messagebox.showinfo('ERR', 'No Internet Connection')

        except requests.exceptions.MissingSchema:
            messagebox.showerror('ERR', 'Provided URL does not contain any image')

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            path = sys.argv

            if path:
                base_path = os.path.split(path[0])[0]

            else:
                base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Image_Downloader()
