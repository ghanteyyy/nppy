import os
import sys
import uuid
import json
import calendar
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as messagebox
from PIL import Image


class BirthdayReminder:
    def __init__(self):
        self.ImagePath = ''
        self.NameEntryDefaultText = True
        self.MonthNames = list(calendar.month_abbr)[1:]
        self.ImageDirPath = self.ResourcePath('images')
        self.FILE = os.path.abspath(os.path.join('.', 'data.json'))

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Birthday Reminder')

        self.BirthdayQuoteImage = Image.open(self.ResourcePath('image.png'))
        width, height = self.BirthdayQuoteImage.size
        self.BirthdayQuoteImage = PhotoImage(file=self.ResourcePath('image.png'))

        self.BirthdayQuoteLabel = Label(self.master, image=self.BirthdayQuoteImage, width=width-10, height=height-2)
        self.BirthdayQuoteLabel.pack(padx=0, pady=0)

        self.NameEntryVar = StringVar()
        self.NameEntryVar.set('Name')
        self.NameEntry = Entry(self.master, width=35, textvariable=self.NameEntryVar, foreground='grey', justify='center')
        self.NameEntry.pack(ipady=3, pady=20)

        self.ComboFrame = LabelFrame(self.master, bg='dark green', text='Date of Birth', fg='white')
        self.ComboFrame.pack(pady=(0, 20))
        self.MonthCombo = ttk.Combobox(self.ComboFrame, values=self.MonthNames, width=12, height=12)
        self.MonthCombo.set('Select Month')
        self.MonthCombo.grid(row=0, column=0, padx=15, pady=15)
        self.DateCombo = ttk.Combobox(self.ComboFrame, values=list(range(1, 32)), width=10, height=12)
        self.DateCombo.set('Select Date')
        self.DateCombo.grid(row=0, column=1, padx=(0, 15))

        self.ChooseImageButton = Button(self.master, text='Choose Image', fg='white', activeforeground='white', bg='#004503', activebackground='#004503', bd=0, width=30, cursor='hand2', command=self.ChooseImageButtonCommand)
        self.ChooseImageButton.pack(pady=(0, 20), ipady=10)

        self.RadioVar = IntVar()
        self.style = ttk.Style()
        self.style.configure('R.TRadiobutton', background='dark green', foreground='white')

        self.RadioFrame = Frame(self.master, bg='dark green')
        self.AddRadioButton = ttk.Radiobutton(self.RadioFrame, text='Add', value=1, variable=self.RadioVar, style='R.TRadiobutton', cursor='hand2')
        self.DeleteRadioButton = ttk.Radiobutton(self.RadioFrame, text='Delete', value=2, variable=self.RadioVar, style='R.TRadiobutton', cursor='hand2')
        self.AddRadioButton.grid(row=0, column=0, padx=10)
        self.DeleteRadioButton.grid(row=0, column=1)
        self.RadioFrame.pack(pady=(0, 20))

        self.SubmitButton = Button(self.master, text='SUBMIT', fg='white', bg='#039e05', activebackground='#039e05', activeforeground='white', cursor='hand2', font=('Courier', 12), width=16, height=3, bd=0, relief=GROOVE, command=self.SubmitCommand)
        self.SubmitButton.pack(pady=(0, 20))

        self.DateCombo.bind('<Return>', self.SubmitCommand)
        self.NameEntry.bind('<Return>', self.SubmitCommand)
        self.master.bind('<Button-1>', self.MasterBindings)
        self.NameEntry.bind('<FocusIn>', self.EntryFocusIn)
        self.NameEntry.bind('<FocusOut>', self.EntryFocusOut)
        self.NameEntry.bind('<Shift-BackSpace>', self.BulkDelete)

        self.InitialPosition()
        self.master.config(bg='dark green')

        self.master.mainloop()

    def InitialPosition(self):
        '''
        Set GUI window to the center of the screen when it starts
        '''

        self.master.update()

        width = self.master.winfo_width()// 2
        height = self.master.winfo_height() // 2
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.resizable(0, 0)
        icon_photo = PhotoImage(file=self.ResourcePath('icon.png'))
        self.master.iconphoto(False, icon_photo)

        self.master.geometry(f'+{screen_width - width}+{screen_height - height}')
        self.master.after(0, self.master.deiconify)

    def EntryFocusIn(self, event=None):
        '''
        Remove the default text when user clicks to the entry widget
        '''

        if self.NameEntryDefaultText:
            self.NameEntryVar.set('')
            self.NameEntryDefaultText = False
            self.NameEntry.config(foreground='black')

    def EntryFocusOut(self, event=None):
        '''
        Re-insert the default text to entry widget when user clicks outside of
        the entry widget without entering any value in it
        '''

        if not self.NameEntryVar.get().strip():
            self.NameEntryVar.set('Name')
            self.NameEntryDefaultText = True
            self.NameEntry.config(foreground='grey')

    def MasterBindings(self, event=None):
        '''
        When user clicks outside of the Entry box
        '''

        if event.widget not in [self.NameEntry, self.MonthCombo, self.DateCombo]:
            if not self.MonthCombo.get().strip():
                self.MonthCombo.set('Select Month')

            if not self.DateCombo.get().strip():
                self.DateCombo.set('Select Date')

            if not self.NameEntryVar.get().strip():
                self.NameEntryDefaultText = False

            self.master.focus()

    def BulkDelete(self, event=None):
        '''
        Delete last word of the value in entry widget
        '''

        if self.NameEntryDefaultText is False:
            from_entry = self.NameEntryVar.get().split()
            from_entry = ' '.join(from_entry[:-1])
            self.NameEntryVar.set(from_entry)

            return 'break'

    def ChooseImageButtonCommand(self):
        '''
        Command for ChooseImageButton to select an image
        '''

        extensions = ([('All', '*png *jpg *jpeg'), ('PNG', '*png'), ('JPG', '*jpg *jpeg')])
        self.ImagePath = filedialog.askopenfilename(title='Select an Image', defaultextension=extensions, filetypes=extensions)

        if self.ImagePath:
            self.ChooseImageButton.config(text=os.path.basename(self.ImagePath))

    def SubmitCommand(self, event=None):
        '''
        Command for submit button
        '''

        var = self.RadioVar.get()
        day = self.DateCombo.get().strip()
        month = self.MonthCombo.get().strip()
        name = self.NameEntry.get().strip().upper()

        if self.NameEntryDefaultText:
            messagebox.showerror('No Input', 'Please enter the valid name')

        elif month not in self.MonthNames:
            messagebox.showerror('Invalid Month', 'Month was expected between Jan-Dec')

        elif not day.isdigit() or not 0 < int(day) <= 32:
            messagebox.showerror('Invalid Date', 'Date was expected between 1-32')

        elif var not in [1, 2]:
            messagebox.showerror('Invalid Option', 'Either Add or Remove button was expected')

        elif not self.ImagePath.strip():
            messagebox.showerror('Invalid Image', 'Please select a valid image')

        else:
            day = day.zfill(2)
            id = uuid.uuid4().hex
            month = str(self.MonthNames.index(month) + 1).zfill(2)

            # Create assets/images directory if not exists
            if os.path.exists(self.ImageDirPath) is False:
                os.mkdir(self.ImageDirPath)

            # Generating new_path with respect to assets/images directory for the selected image
            random_image_name = f"{id}.{self.ImagePath.split('.')[-1]}"
            new_path = os.path.join(self.ImageDirPath, random_image_name)

            # Copying image to assets/images
            with open(self.ImagePath, "rb") as rb, open(new_path, 'wb') as wb:
                contents = rb.read()
                wb.write(contents)

            # Saving details
            contents = {
                id:{
                    'name': name,
                    'date': f'{month}-{day}',
                    'has_seen': False,
                    'image': new_path
                }
            }

            self.WriteJSON(contents)

            self.RadioVar.set(0)
            self.NameEntryVar.set('')
            self.EntryFocusOut()
            self.DateCombo.set('Select Date')
            self.MonthCombo.set('Select Month')
            self.ChooseImageButton.config(text='Choose Image')

    def ReadJSON(self):
        '''
        Reading data from the .json file
        '''

        try:
            with open(self.FILE, 'r') as f:
                contents = json.load(f)

        except FileNotFoundError:
            with open(self.FILE, 'w'):
                contents = {}

        except json.decoder.JSONDecodeError:
            contents = {}

        return contents

    def WriteJSON(self, contents):
        '''
        Storing data to the .json file
        '''

        from_file = self.ReadJSON()
        from_file.update(contents)

        with open(self.FILE, 'w') as f:
            json.dump(from_file, f, indent=4)

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
    BirthdayReminder()
