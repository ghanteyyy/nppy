import os
import subprocess
from tkinter import *
import pyperclip
import edit_menu


class Right_Click:
    def __init__(self, master, text_widget, fmc):
        self.master = master
        self.file_name = fmc.file_name
        self.text_widget = text_widget
        self.emc = edit_menu.Edit_Menu(self.master, self.text_widget)

        self.menu_names = ('Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Select All', 'Search with Google', 'Open Containing Folder')
        self.commands = (self.emc.undo, self.emc.cut, self.emc.copy, self.emc.paste, self.emc.delete, self.emc.select_all, self.emc.search_with_google, self.open_file_location)

        self.menu = Menu(self.master, tearoff=False)

        for index, value in enumerate(zip(self.menu_names, self.commands)):
            if index in [1, 6]:
                self.menu.add_separator()

            self.menu.add_command(label=value[0], command=value[1])

    def is_selection_available(self):
        '''Check if any selection is made'''

        try:
            self.text_widget.get('sel.first', 'sel.last')
            return True

        except TclError:
            return False

        return ('found' in self.text_widget.tag_names() or 'triple_click' in self.text_widget.tag_names())

    def open_file_location(self, event=None):
        '''Open the location of file and select it'''

        FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
        path = os.path.normpath(self.file_name)
        self.master.after(0, lambda: subprocess.run([FILEBROWSER_PATH, '/select,', path]))

    def show_popup(self, event=None):
        '''Display popup menu when user right clicks'''

        try:
            if self.text_widget.get('1.0', 'end-1c').strip('\n'):  # Enabling 'Undo', 'Cut', 'Copy' and 'Select All' option if there is any text in text_widget
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

            if self.is_selection_available():  # Enabling 'Delete', Search with Google' option if there is any text is selected in text_widget
                self.menu.entryconfig(5, state=NORMAL)
                self.menu.entryconfig(8, state=NORMAL)

            else:  # Disabling 'Delete', Search with Google' option if there is no any text is selected in text_widget
                self.menu.entryconfig(5, state=DISABLED)
                self.menu.entryconfig(8, state=DISABLED)

            if self.file_name:  # Enabling 'Open File Location' option if the file is saved
                self.menu.entryconfig(9, state=NORMAL)

            else:  # Disabling 'Open File Location' option if the file is not saved
                self.menu.entryconfig(9, state=DISABLED)

            self.menu.tk_popup(event.x_root, event.y_root)

        finally:
            self.menu.grab_release()
