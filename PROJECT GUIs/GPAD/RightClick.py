import os
import random
import string
import subprocess
from tkinter import *
import tkcap
import pyperclip
import EditMenu


class RightClick:
    def __init__(self, master, text_widget, fmc, var):
        self.master = master
        self.FileName = fmc.FileName
        self.TextWidget = text_widget
        self.emc = EditMenu.Edit_Menu(self.master, self.TextWidget, var)

        self.MenuNames = ('Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Select All', 'Take Screenshot', 'Search with Google', 'Open Containing Folder')
        self.commands = (self.emc.undo, self.emc.cut, self.emc.copy, self.emc.paste, self.emc.delete, self.emc.SelectAll, self.TakeScreenshot, self.emc.SearchWithGoogle, self.OpenFileLocation)

        self.menu = Menu(self.master, tearoff=False)

        for index, value in enumerate(zip(self.MenuNames, self.commands)):
            if index in [1, 6]:
                self.menu.add_separator()

            self.menu.add_command(label=value[0], command=value[1])

    def IsSelectionAvailable(self):
        '''
        Check if any selection is made
        '''

        try:
            self.TextWidget.get('sel.first', 'sel.last')
            return True

        except TclError:
            return False

        return ('found' in self.TextWidget.tag_names() or 'triple_click' in self.TextWidget.tag_names())

    def OpenFileLocation(self, event=None):
        '''
        Open the location of file and select it
        '''

        FILE_BROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        path = os.path.normpath(self.FileName)
        self.master.after(0, lambda: subprocess.run([FILE_BROWSER_PATH, '/select,', path]))

    def TakeScreenshot(self, event=None):
        '''
        Take screenshot of the entire window
        '''

        random_name = ''.join(random.choice(string.ascii_letters) for _ in range(8)) + '.png'
        cap = tkcap.CAP(self.master)
        self.master.after(250, lambda: cap.capture(random_name))

    def ShowPopUp(self, event=None):
        '''
        Display popup menu when user right clicks
        '''

        try:
            if self.TextWidget.get('1.0', 'end-1c').strip('\n'):  # Enabling 'Undo', 'Cut', 'Copy' and 'Select All' option if there is any text in text_widget
                self.menu.entryconfig(0, state=NORMAL)
                self.menu.entryconfig(2, state=NORMAL)
                self.menu.entryconfig(3, state=NORMAL)
                self.menu.entryconfig(6, state=NORMAL)

            else:  # Disabling 'Undo', Cut' and 'Copy' option if there is no any text in text_widget
                self.menu.entryconfig(0, state=DISABLED)
                self.menu.entryconfig(2, state=DISABLED)
                self.menu.entryconfig(3, state=DISABLED)
                self.menu.entryconfig(6, state=DISABLED)

            if pyperclip.paste():  # Enabling 'Paste' option if there is any text in clipboard
                self.menu.entryconfig(4, state=NORMAL)

            else:  # Disabling 'Paste' option if there is no any text in clipboard
                self.menu.entryconfig(4, state=DISABLED)

            if self.IsSelectionAvailable():  # Enabling 'Delete', Search with Google' option if there is any text is selected in text_widget
                self.menu.entryconfig(5, state=NORMAL)
                self.menu.entryconfig(9, state=NORMAL)

            else:  # Disabling 'Delete', Search with Google' option if there is no any text is selected in text_widget
                self.menu.entryconfig(5, state=DISABLED)
                self.menu.entryconfig(9, state=DISABLED)

            if self.FileName:  # Enabling 'Open File Location' option if the file is saved
                self.menu.entryconfig(10, state=NORMAL)

            else:  # Disabling 'Open File Location' option if the file is not saved
                self.menu.entryconfig(10, state=DISABLED)

            self.menu.tk_popup(event.x_root, event.y_root)

        finally:
            self.menu.grab_release()
