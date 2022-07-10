import os
import sys
import ctypes
import winsound
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import font, scrolledtext


def IsAdmin():
    '''Check if program is executed with administrator privilege'''

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()

    except:
        return False


class WebsiteBlocker:
    def __init__(self):
        self.PreviousText = ''
        self.PreviousEntry = None
        self.LocalHost = '127.0.0.1 '
        self.DefaultAddress = 'https://github.com/ghanteyyy'
        self.HostFile = r'C:\Windows\System32\drivers\etc\hosts'

        self.BlockerWindow = Tk()
        self.BlockerWindow.withdraw()
        self.BlockerWindow.iconbitmap(self.ResourcePath('icon.ico'))
        self.BlockerWindow.title('Website Blocker')

        self.AddImage = PhotoImage(file=self.ResourcePath('Add.png'))
        self.DeleteImage = PhotoImage(file=self.ResourcePath('Remove.png'))
        self.RenameImage = PhotoImage(file=self.ResourcePath('Rename.png'))

        self.TopFrame = Frame(self.BlockerWindow)
        self.TopFrame.pack(side=TOP)

        self.style = ttk.Style()
        self.EntryVar = StringVar()
        self.EntryVar.set(self.DefaultAddress)
        self.style.configure('Ent.TEntry', foreground='grey')

        self.WebsiteEntry = ttk.Entry(self.TopFrame, textvariable=self.EntryVar, width=66, justify='center', font=font.Font(size=10), style='Ent.TEntry')
        self.WebsiteEntry.grid(row=0, column=0, ipady=5)

        self.AddButton = Button(self.TopFrame, image=self.AddImage, bd=0, cursor='hand2', command=lambda event=Event: self.AddDetails(event=event))
        self.AddButton.grid(row=0, column=1, ipadx=5, ipady=5)

        self.DisplayBlockedSites = scrolledtext.ScrolledText(self.BlockerWindow, spacing2=6, bd=0, width=60, bg='#e4ede9', cursor='arrow')
        self.DisplayBlockedSites.pack(pady=3)

        self.StartUpInsert()

        self.WebsiteEntry.bind('<FocusIn>', self.FocusIn)
        self.WebsiteEntry.bind('<Return>', self.AddDetails)
        self.WebsiteEntry.bind('<FocusOut>', self.FocusOut)
        self.BlockerWindow.bind('<Button-1>', self.ForbidDefaultBindings)
        self.DisplayBlockedSites.bind('<Button-1>', self.ForbidDefaultBindings)

        self.StartAtCenter()
        self.BlockerWindow.mainloop()

    def ForbidDefaultBindings(self, event=None):
        '''When user clicks Text Widget'''

        try:
            wid = event.widget.winfo_parent().winfo_parent()[0]

        except AttributeError:
            wid = event.widget

        if self.PreviousEntry and self.PreviousEntry != event.widget:
            self.RenameInsideFile()

        if not self.EntryVar.get().strip():  # Inserting default text in Entry Widget if no text is found in it
            self.BlockerWindow.focus()
            self.EntryVar.set(self.DefaultAddress)
            self.style.configure('Ent.TEntry', foreground='grey')

        if self.PreviousEntry:
            if wid.winfo_parent() != self.PreviousEntry.winfo_parent():
                self.PreviousEntry.config(state='disabled', cursor='arrow')
                self.PreviousEntry = None

        return 'break'

    def FocusIn(self, event=None):
        '''When user clicks to the Entry widget to add new Address'''

        if self.EntryVar.get().strip() == self.DefaultAddress:
            self.EntryVar.set('')
            self.style.configure('Ent.TEntry', foreground='black')

    def FocusOut(self, event=None):
        '''When user clicks other widget'''

        if not self.EntryVar.get().strip():
            self.EntryVar.set(self.DefaultAddress)
            self.style.configure('Ent.TEntry', foreground='grey')
            self.BlockerWindow.focus()

    def AddDetails(self, event=None, default=None):
        '''When user clicks + button'''

        if event:
            text = self.EntryVar.get().strip()

        else:
            text = default

        if text and text != self.DefaultAddress:
            contents = self.ReadContents()
            text = f'{self.LocalHost}{text.strip(self.LocalHost)}\n'

            if default is None and text in contents:
                winsound.MessageBeep()
                return

            InnerWidget = Frame(self.DisplayBlockedSites, bg='#e4ede9')

            SavedEntry = ttk.Entry(InnerWidget, width=70, cursor='arrow')
            SavedEntry.grid(row=0, column=0, ipady=5)
            SavedEntry.insert(0, text.strip(self.LocalHost).strip())
            SavedEntry.config(state='disabled', cursor='arrow')

            ButtonsAttr = {'bd': 0, 'cursor': 'hand2', 'bg': '#e4ede9', 'activebackground': '#e4ede9'}
            RenameButton = Button(InnerWidget, image=self.RenameImage, **ButtonsAttr, command=lambda widget=SavedEntry: self.RenameDetails(widget=widget))
            RenameButton.grid(row=0, column=1, padx=5)

            DeleteButton = Button(InnerWidget, image=self.DeleteImage, **ButtonsAttr, command= lambda frame=InnerWidget: self.DeleteDetails(frame=frame))
            DeleteButton.grid(row=0, column=2)

            if default is None:
                if contents[-1].startswith('#'):  # Adding new line if there is no new line at end of file
                    contents.append('\n')

                if text not in contents:
                    contents.append(text)
                    self.WriteSite(contents)

            self.DisplayBlockedSites.window_create(END, window=InnerWidget)
            self.DisplayBlockedSites.insert('end', '\n')

            self.EntryVar.set('')
            self.FocusOut()

        else:
            if default is None:
                # Play messageBeep sound when user presses + button without any text in
                # Entry widget but not when there is no website address found in hosts
                # file when program starts for the first time

                winsound.MessageBeep()

    def RenameDetails(self, event=None, widget=None):
        '''When user clicks Rename button'''

        if self.PreviousEntry == widget:
            self.RenameInsideFile()
            self.PreviousEntry = None
            widget.config(state='disabled', cursor='arrow')
            return

        widget.config(state='normal', cursor='xterm')
        widget.focus()
        widget.selection_range(0, 'end')
        self.PreviousText = f'{self.LocalHost}{widget.get()}\n'

        if self.PreviousEntry is not None:
            self.PreviousEntry.config(state='disabled', cursor='arrow')

        self.PreviousEntry = widget

    def DeleteDetails(self, event=None, frame=None):
        '''When user clicks Delete button'''

        contents = self.ReadContents()
        site = f'{self.LocalHost}{frame.winfo_children()[0].get()}\n'

        if site in contents:
            contents.remove(site)
            self.WriteSite(contents)

        index = self.DisplayBlockedSites.index(frame)
        self.DisplayBlockedSites.delete(f'{index} linestart', f'{index} lineend+1c')

        frame.destroy()

    def StartUpInsert(self):
        '''Insert Website Address when program starts'''

        contents = self.ReadContents()

        for content in contents:
            if content and not content.startswith('#'):
                self.AddDetails(default=content.strip('\n'))

    def ReadContents(self):
        '''Read host file and returns the contents of it'''

        with open(self.HostFile, 'r') as f:
            return f.readlines()

    def WriteSite(self, contents):
        '''Save Website Address to the host file'''

        with open(self.HostFile, 'w') as f:
            for content in contents:
                f.write(content)

    def RenameInsideFile(self):
        '''Replace old entry with new entry inside the file'''

        NewText = f'{self.LocalHost}{self.PreviousEntry.get()}\n'
        contents = self.ReadContents()

        if NewText != self.PreviousText:
            try:
                index = contents.index(self.PreviousText)
                contents[index] = NewText

                self.WriteSite(contents)

            except ValueError:
                pass

    def StartAtCenter(self):
        '''Place window at the center of screen when it opens for the first time'''

        self.BlockerWindow.update()
        self.BlockerWindow.resizable(0, 0)

        pos_x = self.BlockerWindow.winfo_screenwidth() // 2 - self.BlockerWindow.winfo_width() // 2
        pos_y = self.BlockerWindow.winfo_screenheight() // 2 - self.BlockerWindow.winfo_height() // 2

        self.BlockerWindow.geometry(f'+{pos_x}+{pos_y}')
        self.BlockerWindow.deiconify()

    def ResourcePath(self, file_name):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    if IsAdmin():
        WebsiteBlocker()

    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, " ".join(sys.argv), None, 0)
