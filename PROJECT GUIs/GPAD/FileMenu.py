import os
import hashlib
from tkinter import messagebox
from tkinter import filedialog
import main
import Include


class File_Menu:
    def __init__(self, master, text_widget, var):
        self.Var = var
        self.FileName = ''
        self.master = master
        self.isSaved = False
        self.TextWidget = text_widget
        self.extensions = ([("Plain Text", "*.txt"), ('Python', '*.py')])
        self.PreviousSignature = self.GetSignature(self.GetContents())

    def set_var(self, text, time=4000):
        '''Config text to the status_label'''

        Include.set_var(self.master, self.Var, text, time)

    def GetContents(self):
        '''Get everything that is in text_widget'''

        return self.TextWidget.get('1.0', 'end-1c')

    def GetSignature(self, contents):
        '''Get the hash of the text inside of text_widget'''

        return hashlib.md5(bytes(self.GetContents(), encoding='utf-8')).digest()

    def IsFileChanged(self):
        '''Check if the signature of the the previous content in text_widget is
           not the same of the current content in text_widget.'''

        return self.GetSignature(self.GetContents()) != self.PreviousSignature

    def WriteToFile(self):
        '''Write the content of the text_widget to the given filename'''

        with open(self.FileName, 'w', encoding='utf-8') as f:
            self.isSaved = True
            f.write(self.GetContents())
            self.PreviousSignature = self.GetSignature(self.GetContents())
            self.set_var(f'Saved to {self.FileName}')

    def New(self, event=None):
        '''When user presses ctrl+n or clicks new option from file menu'''

        if self.IsFileChanged():
            choice = messagebox.askyesnocancel('Z-PAD', 'Do you want to quit without saving?')

            if choice is True:
                self.isSaved = True

            elif choice is False:
                self.Save()

            else:
                return

        if self.isSaved:
            self.FileName = ''
            self.isSaved = False
            self.set_var('New File Created')
            self.TextWidget.delete('1.0', 'end')
            self.master.title('Untitled - GPAD')
            self.PreviousSignature = self.GetSignature(self.GetContents)

    def NewWindow(self, event=None):
        '''When user presses ctrl+shift+n or clicks new_window option from file_menu'''

        main.GPAD(NewWindow=True)

    def Open(self, event=None):
        '''When user presses ctrl+o or clicks open option from file menu'''

        if self.IsFileChanged():
            choice = messagebox.askyesnocancel('Z-PAD', 'Do you want to open another file without saving the current one?')

            if choice is False:
                saved = self.Save()

                if not saved:  # If user does not save the contents
                    return 'break'

            elif choice is None:
                return 'break'

        self.master.update()
        file_name = filedialog.askopenfilename(title="Select file", filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

        if file_name:
            self.FileName = file_name
            self.TextWidget.delete('1.0', 'end')

            with open(self.FileName, 'r') as f:
                lines = f.read()
                self.TextWidget.insert('end', lines)

            self.set_var(f'Opened {self.FileName}')
            self.PreviousSignature = self.GetSignature(self.GetContents)
            self.title = os.path.basename(self.FileName) + ' - GPAD'
            self.master.title(self.title)

        return 'break'

    def Save(self, event=None):
        '''When user presses ctrl+s or clicks save option from the file menu'''

        if self.FileName and self.IsFileChanged():  # When user wants to save the file that is already saved once.
            self.WriteToFile()

        elif not self.FileName:  # When user tries to save a file that is not saved previously.
            self.SaveAs()

    def SaveAs(self, event=None):
        '''When user presses ctrl+shift+s or clicks save_as option from the file_menu'''

        self.master.update()
        file_name = filedialog.asksaveasfilename(title="Save", filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

        if file_name:
            self.FileName = file_name
            self.WriteToFile()
            self.master.title(os.path.basename(self.FileName) + ' - GPAD')

        else:
            self.isSaved = False

    def DeleteZoom(self):
        '''Delete the amount of zoomed from the json file'''

        font_details = Include.get_font_details()

        if 'Zoomed' in font_details:
            font_details.pop('Zoomed')

        Include.save_font_details(font_details)
