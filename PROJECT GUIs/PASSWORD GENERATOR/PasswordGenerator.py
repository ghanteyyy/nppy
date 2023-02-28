import os
import sys
import string
import random
import pyperclip
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


class PasswordGenerator:
    def __init__(self):
        self.bg = "#0F0E0E"
        self.PrevKeySym = []
        self.ClearedDefault = False
        self.DEFAULT_TEXT = 'Number of Character'

        self.master = Tk()
        self.master.withdraw()
        self.master.config(bg=self.bg)
        self.master.title('Password GENERATOR')
        self.master.iconphoto(False, PhotoImage(file=self.ResourcePath("icon.png")))

        self.image = PhotoImage(file=self.ResourcePath('title_image.png'))
        self.ImageLabel = Label(self.master, image=self.image, bg=self.bg)
        self.ImageLabel.pack(pady=5, padx=20)

        self.NumberBoxVar = StringVar()
        self.NumberBoxStyle = ttk.Style()
        self.NumberBoxStyle.configure('N.TEntry', foreground='grey', font=('Calibri', 12))
        self.NumberBoxEntry = ttk.Entry(self.master, width=35, textvariable=self.NumberBoxVar, style='N.TEntry', justify='center')
        self.NumberBoxVar.set(self.DEFAULT_TEXT)
        self.NumberBoxEntry.pack(pady=5, ipady=3)

        self.CheckBoxFrame = Frame(self.master, bg=self.bg)
        self.CheckBoxItems = ['UPPERCASE', 'LOWERCASE', 'NUMBERS', 'SPECIAL CHARACTERS', 'ALL']  # Options for generating password

        self.UpperVar, self.LowerVar, self.NumVar, self.SpecialVar, self.AllVar = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        self.vars = [self.UpperVar, self.LowerVar, self.NumVar, self.SpecialVar, self.AllVar]

        self.CheckBoxStyle = ttk.Style()
        self.CheckBoxStyle.configure('C.TCheckbutton', font=('Calibri', 12), background=self.bg, foreground='white')

        for index, value in enumerate(self.CheckBoxItems):  # Creating Check-buttons as per name in "self.CheckBoxItems" and variables as per in self.vars
            self.CheckBox = ttk.Checkbutton(self.CheckBoxFrame, text=value, variable=self.vars[index], cursor='hand2', style='C.TCheckbutton')
            self.CheckBox.grid(row=index, column=0, sticky='w')

        self.CheckBoxFrame.pack(pady=10)

        self.GeneratePasswordButton = Button(self.master, text='Generate Password', bg='Green', fg='white', activeforeground='white', activebackground='Green', font=('Calibri', 12), relief=FLAT, cursor='hand2', command=self.GenerateButtonCommand)
        self.GeneratePasswordButton.pack(pady=10, ipadx=5, ipady=5)

        self.BottomFrame = Frame(self.master, bg=self.bg)
        self.BottomFrame.pack(side=BOTTOM, expand=True, fill='both')
        self.PasswordLabel = Label(self.BottomFrame, font=('Calibri', 20), bg=self.bg, fg='white')
        self.CopyButton = Button(self.BottomFrame, text='Copy', bd=0, bg='Green', fg='white', activeforeground='white', activebackground='Green', relief=FLAT, cursor='hand2', command=self.CopyToClipboard)

        self.master.bind('<Button-1>', self.FocusHere)
        self.NumberBoxEntry.bind('<FocusIn>', self.FocusIn)
        self.NumberBoxEntry.bind('<FocusOut>', self.FocusOut)
        self.master.bind('<Control-c>', self.CopyToClipboard)
        self.master.bind('<Control-C>', self.CopyToClipboard)
        self.NumberBoxEntry.bind('<KeyPress>', self.KeyPressed)
        self.NumberBoxEntry.bind('<KeyRelease>', self.KeyReleased)
        self.NumberBoxEntry.bind('<Return>', self.GenerateButtonCommand)
        self.GeneratePasswordButton.bind('<Return>', self.GenerateButtonCommand)

        self.VarTrace()
        self.InitialPosition()

        self.master.mainloop()

    def InitialPosition(self):
        '''
        Placing window at the center of screen when the GUI starts at first
        '''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width() // 2
        height = self.master.winfo_height() // 2
        ScreenWidth = self.master.winfo_screenwidth() // 2
        ScreenHeight = self.master.winfo_screenheight() // 2

        WIN_X = ScreenWidth - width
        WIN_Y = ScreenHeight - height

        self.master.geometry(f'+{WIN_X}+{WIN_Y}')
        self.master.deiconify()

    def FocusHere(self, event=None):
        '''
        Focus to the clicked widget
        '''

        if isinstance(event.widget, ttk.Checkbutton):
            self.master.focus()

        else:
            event.widget.focus_force()

    def FocusIn(self, event=None):
        '''
        Remove default text when user clicks to entry widget
        '''

        get = self.NumberBoxVar.get().strip()

        if self.ClearedDefault is False and get == self.DEFAULT_TEXT:
            self.NumberBoxVar.set('')
            self.ClearedDefault = True
            self.NumberBoxStyle.configure('N.TEntry', foreground='black')

    def FocusOut(self, event=None):
        '''
        Remove focus from Entry widget when already focused and still user
        presses TAB key
        '''

        get = self.NumberBoxVar.get().strip()

        if not get:
            self.ClearedDefault = False
            self.NumberBoxVar.set(self.DEFAULT_TEXT)
            self.NumberBoxStyle.configure('N.TEntry', foreground='grey')

    def VarTrace(self):
        '''
        Continuously check if the last value in number_box_var is not digit. If
        found TRUE then set this var without that non-digit value
        '''

        VarGet = self.NumberBoxVar.get()

        if VarGet and self.ClearedDefault is True and VarGet[-1].isdigit() is False:
            if self.NumberBoxEntry.selection_present():
                self.NumberBoxVar.set(VarGet[:-1])
                self.NumberBoxEntry.event_generate('<Control-a>')

            else:
                self.NumberBoxVar.set(VarGet[:-1])

        self.master.after(1, self.VarTrace)

    def KeyPressed(self, event=None):
        '''
        When user presses any key in keyboard
        '''

        num = event.keysym

        if num.startswith('Control') or num.startswith('Shift') or num.startswith('Alt'):
            self.PrevKeySym.append(num)

        if self.NumberBoxEntry.selection_present() and not self.PrevKeySym and num.isdigit() is False:
            return 'break'

    def KeyReleased(self, event=None):
        '''
        When user releases any pressed key in keyboard
        '''

        num = event.keysym

        if num in self.PrevKeySym:
            self.PrevKeySym.remove(num)

    def GenerateRandomPassword(self, string_combination, lengths):
        '''
        Generating random generated password
        '''

        return ''.join([random.SystemRandom().choice(string_combination) for _ in range(lengths)])

    def CopyToClipboard(self, event=None):
        '''
        Copy Generated Password to the clipboard
        '''

        text = self.PasswordLabel['text']

        if text:
            pyperclip.copy(text)
            self.CopyButton.config(text='Copied!')

            self.master.after(1000, self.ForgetCopyWidget)

        else:
            messagebox.showerror('ERROR', 'Not yet generated password')

    def ForgetCopyWidget(self):
        '''
        Delete copy_button widget from the screen after 1000ms
        '''

        self.CopyButton.config(text='Copy')
        self.CopyButton.pack_forget()

    def GenerateButtonCommand(self, event=None):
        '''
        Command when user clicks generate button
        '''

        get_var = [var.get() for var in self.vars]
        num_get = self.NumberBoxVar.get().strip()

        # Set the value of entry-widget to 8 if its value is same as the value
        # in self.DEFAULT_TEXT
        if num_get == self.DEFAULT_TEXT:
            num_get = '8'
            self.NumberBoxVar.set('8')
            self.NumberBoxStyle.configure('N.TEntry', foreground='black')

        # Selecting the last check-buttons if user have not selected one
        if not any(get_var):
            get_var[-1] = 1
            self.AllVar.set(1)

        lengths = int(num_get)
        string_combo = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation, string.printable[:94]]

        string_combination = ''.join({string_combo[index] for index, value in enumerate(get_var) if value == 1})
        password = self.GenerateRandomPassword(string_combination, lengths)

        self.PasswordLabel.config(text=password)
        self.PasswordLabel.pack(pady=(0, 10))

        self.CopyButton.pack(side=RIGHT, ipadx=5, ipady=5)

    def ResourcePath(self, FileName):
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
            BasePath = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            BasePath = os.path.dirname(__file__)

        return os.path.join(BasePath, 'assets', FileName)


if __name__ == '__main__':
    PasswordGenerator()
