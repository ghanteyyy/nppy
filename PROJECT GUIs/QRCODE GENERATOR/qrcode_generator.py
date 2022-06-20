import os
import io
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter import filedialog
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk


class QRCODE_GENERATOR:
    def __init__(self):
        self.DEFAULT_TEXT = 'QR Text Here ...'
        self.QR_DEFAULT_TEXT = 'https://github.com/ghanteyyy'
        self.ClearedDefault = False  # Track if user have inserted data

        self.master = Tk()
        self.master.withdraw()
        self.master.config(bg='white')
        self.master.title('QR CODE GENERATOR')

        self.IconImage = PhotoImage(file=self.ResourcePath('icon.png'))
        self.master.iconphoto(None, self.IconImage)

        self.message_box_style = ttk.Style()
        self.message_box_style.configure('MB.TEntry', foreground='grey')

        self.message_box_var = StringVar()
        self.message_box_var.set(self.DEFAULT_TEXT)
        self.message_box_var.trace('w', self.trace_var)

        self.message_box = ttk.Entry(self.master, width=60, textvariable=self.message_box_var, style='MB.TEntry', justify='center')
        self.message_box.pack(padx=5, ipady=5, pady=8)

        self.qr_label = Label(self.master, bd=0)
        self.qr_label.pack()

        self.info_label = Label(self.master, bd=0, fg='black', bg='white', text='Ctrl + S or Right Click to save', font=Font(size=8))
        self.info_label.pack(side=BOTTOM, ipady=5)

        self.make_QR(self.QR_DEFAULT_TEXT)
        self.InitialPosition()

        self.master.bind('<Button-1>', self.focus_here)
        self.message_box.bind('<FocusIn>', self.focus_in)
        self.message_box.bind('<FocusOut>', self.focus_out)
        self.master.bind_all('<Control-s>', self.SaveImage)
        self.master.bind_all('<Button-3>', self.RightClick)

        self.master.mainloop()

    def InitialPosition(self):
        '''Set window position to the center when program starts first time'''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width() // 2
        height = self.master.winfo_height() // 2
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.geometry(f'+{screen_width - width}+{screen_height - height}')
        self.master.deiconify()

    def focus_here(self, event=None):
        '''Focus to the clicked widget'''

        event.widget.focus_force()

    def focus_in(self, event=None):
        '''Remove default text when user clicks to entry widget'''

        if self.ClearedDefault is False:
            self.ClearedDefault = True
            self.message_box_var.set('')
            self.message_box_style.configure('MB.TEntry', foreground='black')

    def focus_out(self, event=None):
        '''Insert default text if user does not add any text to
           entry widget and changes the focus to other widget'''

        if not self.message_box_var.get():
            self.ClearedDefault = False
            self.message_box_var.set(self.DEFAULT_TEXT)
            self.message_box_style.configure('MB.TEntry', foreground='grey')

    def trace_var(self, *args):
        '''When user changes value in entry widget'''

        text = self.message_box_var.get().strip()

        if not (text and self.ClearedDefault):  # Checking if user have actually inserted text in the Entry widget
            text = self.QR_DEFAULT_TEXT

        self.make_QR(text)

    def make_QR(self, data):
        '''Make QR code based on the text inserted in the entry widget'''

        try:
            img = self.img = qrcode.make(data)

            if self.img.size[1] > 290:  # Resize generated QR-code image when its height exceeds 290
                img = self.img.resize((290, 290), Image.Resampling.LANCZOS)

            img = ImageTk.PhotoImage(image=img)

            self.qr_label.config(image=img)
            self.qr_label.image = img

        except qrcode.exceptions.DataOverflowError:
            messagebox.showinfo('ERR', 'Upto 2,394 characters are allowed')

            self.message_box_var.set('')
            self.master.focus()

    def SaveImage(self, event=None):
        '''Save QR code to the user selected location'''

        file_types = [('PNG', '*.png'), ('JPG', '*.jpg')]
        path = filedialog.asksaveasfilename(title='Save', filetypes=file_types, defaultextension=([file_types[0]]))

        if path:  # Save image only when user have given valid location
            self.img.save(path)

    def RightClick(self, event=None):
        '''When user right clicks to QR image'''

        if not isinstance(event.widget, ttk.Entry):  # When right-click is not invoked in Entry widget
            RightClickMenu = Menu(self.master, tearoff=0)
            RightClickMenu.add_command(label='Save QR', command=self.SaveImage)

            try:
                RightClickMenu.post(event.x_root, event.y_root)

            finally:
                RightClickMenu.grab_release()

    def ResourcePath(self, FileName):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'included_files', FileName)


if __name__ == '__main__':
    QRCODE_GENERATOR()
