import os
import hashlib
from tkinter import messagebox
from tkinter import filedialog
import main
import include


class File_Menu:
    def __init__(self, master, text_widget):
        self.file_name = ''
        self.master = master
        self.is_saved = False
        self.text_widget = text_widget
        self.previous_signature = self.get_signature(self.get_contents)

    def get_contents(self):
        '''Get everything that is in text_widget'''

        return self.text_widget.get('1.0', 'end-1c')

    def get_signature(self, contents):
        '''Get the hash of the text inside of text_widget'''

        return hashlib.md5(bytes(self.get_contents(), encoding='utf-8')).digest()

    def is_file_changed(self):
        '''Check if the signature of the the previous content in text_widet is
           not the same of the current content in text_widget.'''

        current_signature = self.get_signature(self.get_contents)
        return current_signature != self.previous_signature

    def write_to_file(self):
        '''Write the content of the text_widget to the given filename'''

        with open(self.file_name, 'w') as f:
            self.is_saved = True
            f.write(self.get_contents())
            self.previous_signature = self.get_signature(self.get_contents())
            return True

        title = self.master.title()

        if title.startswith('*') and not self.is_file_changed():
            self.master.title(title[1:])

    def new(self, event=None):
        '''When user presses ctrl+n or clicks new option from file menu'''

        if self.is_file_changed():
            choice = messagebox.askyesnocancel('Z-PAD', 'Do you want to quit without saving?')

            if choice is True:
                self.is_saved = True

            elif choice is False:
                self.save()

            else:
                return

        if self.is_saved:
            self.file_name = ''
            self.is_saved = False
            self.text_widget.delete('1.0', 'end')
            self.master.title('Untitled - ZPAD')
            self.previous_signature = self.get_signature(self.get_contents)

    def new_window(self, event=None):
        '''When user presses ctrl+shift+n or clicks new_window option from file_menu'''

        main.ZPAD()

    def open(self, event=None):
        '''When user presses ctrl+o or clicks open option from file menu'''

        if self.is_file_changed():
            choice = messagebox.askyesnocancel('Z-PAD', 'Do you want to open another file without saving the current one?')

            if choice is False:
                saved = self.save()

                if not saved:  # If user does not save the contents
                    return 'break'

            elif choice is None:
                return 'break'

        self.master.update()
        self.file_name = filedialog.askopenfilename(title="Select file", filetypes=(("text files", "*.txt"), ("text files")))

        if self.file_name:
            self.text_widget.delete('1.0', 'end')

            with open(self.file_name, 'r') as f:
                lines = f.read()
                self.text_widget.insert('end', lines)

            self.previous_signature = self.get_signature(self.get_contents)
            self.title = os.path.basename(self.file_name).rstrip('.txt') + ' - ZPAD'
            self.master.title(self.title)

        return 'break'

    def save(self, event=None):
        '''When user presses ctrl+s or clicks save option from the file menu'''

        if self.file_name and self.is_file_changed():  # When user wants to save the file that is already saved once.
            self.write_to_file()

        elif not self.file_name:  # When user tries to save a file that is not saved previously.
            self.save_as()

    def save_as(self, event=None):
        '''When user presses ctrl+shift+s or clicks save_as option from the file_menu'''

        self.master.update()
        self.file_name = filedialog.asksaveasfilename(initialdir="/", title="Save", filetypes=(("Text Documents (*.txt)", "*.txt"), ("All Files", "*.txt")))

        if self.file_name:
            if not self.file_name.endswith('.txt'):
                self.file_name += '.txt'

            self.write_to_file()
            self.master.title(os.path.basename(self.file_name).rstrip('.txt') + ' - ZPAD')

        else:
            self.is_saved = False

    def delete_zoom(self):
        '''Delete the amount of zoomed from the json file'''

        font_details = include.get_font_details()

        if 'Zoomed' in font_details:
            font_details.pop('Zoomed')

        include.save_font_details(font_details)

    def exit(self, event=None):
        '''When user wants to exit the program'''

        if self.is_file_changed():
            choice = messagebox.askyesnocancel('ZPAD', 'Do you really want to quit without saving?')

            if choice is True:
                self.delete_zoom()
                self.master.destroy()

            elif choice is False:
                self.save()

                if not self.is_file_changed():
                    self.delete_zoom()
                    self.master.destroy()

            else:
                return

        else:
            self.delete_zoom()
            self.master.destroy()
