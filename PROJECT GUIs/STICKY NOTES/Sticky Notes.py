import os
import sys
import random
import string

try:  # Python 3
    from tkinter import *
    from tkinter import messagebox
    from tkinter.ttk import Scrollbar

except (ModuleNotFoundError, ImportError):  # Python 2
    from Tkinter import *
    from ttk import Scrollbar
    import tkMessageBox as messagebox


class Sticky_Notes:
    def __init__(self):
        self.all_tags = {}

        self.master = Tk()
        self.master.withdraw()
        self.master.wm_attributes('-topmost', True)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))

        self.master.title('STICKY NOTES')
        self.width, self.height = 301, 290
        self.screen_width, self.screen_height = self.master.winfo_screenwidth() - 10, 10
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width - self.width}+{self.screen_height}')

        self.font = ('Courier', 13)

        self.container = Frame(self.master)
        self.text_widget_frame = Frame(self.container)
        self.text_widget = Text(self.text_widget_frame, fg='black', bg='#fffed1', width=27, height=11, bd=0, font=self.font, wrap=WORD, insertbackground='black')
        self.text_widget.pack(side=LEFT, ipadx=6, ipady=14)
        self.text_widget_frame.pack(side=LEFT)
        self.container.pack()

        self.scrollbar = Scrollbar(self.text_widget_frame, orient='vertical', command=self.text_widget.yview)
        self.scrollbar.pack(side=LEFT, fill='y')
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.formatter_frame = Frame(self.master, bg='#fffed1')

        self.bold_obj = PhotoImage(file=self.resource_path('included_files/bold.png'))
        self.bold_button = Button(self.formatter_frame, image=self.bold_obj, bd=0, bg='#fffed1', activebackground='#fffed1', cursor='hand2', command=lambda: self.change_tags('bold'))
        self.bold_button.pack(side=LEFT)

        self.italic_obj = PhotoImage(file=self.resource_path('included_files/italic.png'))
        self.italic_button = Button(self.formatter_frame, image=self.italic_obj, bd=0, bg='#fffed1', activebackground='#fffed1', cursor='hand2', command=lambda: self.change_tags('italic'))
        self.italic_button.pack(side=LEFT, padx=5)

        self.underline_obj = PhotoImage(file=self.resource_path('included_files/underline.png'))
        self.underline_button = Button(self.formatter_frame, image=self.underline_obj, bd=0, bg='#fffed1', activebackground='#fffed1', cursor='hand2', command=lambda: self.change_tags('underline'))
        self.underline_button.pack(side=LEFT)

        self.overstrike_obj = PhotoImage(file=self.resource_path('included_files/overstrike.png'))
        self.overstrike_button = Button(self.formatter_frame, image=self.overstrike_obj, bd=0, bg='#fffed1', activebackground='#fffed1', cursor='hand2', command=lambda: self.change_tags('overstrike'))
        self.overstrike_button.pack(side=LEFT, padx=5)

        self.formatter_frame.pack()

        self.text_widget.bind('<Control-b>', lambda e: self.change_tags('bold'))
        self.text_widget.bind('<Control-B>', lambda e: self.change_tags('bold'))
        self.text_widget.bind('<Control-i>', lambda e: self.change_tags('italic'))
        self.text_widget.bind('<Control-I>', lambda e: self.change_tags('italic'))
        self.text_widget.bind('<Control-u>', lambda e: self.change_tags('underline'))
        self.text_widget.bind('<Control-U>', lambda e: self.change_tags('underline'))
        self.text_widget.bind('<Control-o>', lambda e: self.change_tags('overstrike'))
        self.text_widget.bind('<Control-O>', lambda e: self.change_tags('overstrike'))

        self.text_widget.focus()

        self.master.after(0, self.master.deiconify)
        self.master.config(bg='#fffed1')
        self.master.mainloop()

    def tag_exists(self):
        '''Checking if the selected text has got already tag'''

        if self.text_widget.tag_names('sel.first')[1:]:
            return True

        return False

    def change_tags(self, tag):
        '''Change text to bold, italic, underline or overstrike'''

        new_tag = ''.join([random.choice(string.ascii_letters) for _ in range(10)])   # Generating new tags

        try:
            if self.tag_exists():
                tag_name = self.text_widget.tag_names('sel.first')[-1]    # Getting the last tag name
                states = self.all_tags[tag_name]

                if tag in states:
                    new_states = [state for state in states if state != tag]

                else:
                    new_states = [state for state in states] + [tag]

                if not new_states:
                    new_states = ['normal']

            else:
                new_states = [tag]

            self.all_tags[new_tag] = new_states

            use_tags = tuple(new_states)
            fnt = self.font + use_tags

            self.text_widget.tag_add(new_tag, 'sel.first', 'sel.last')
            self.text_widget.tag_configure(new_tag, font=fnt)
            self.text_widget.tag_raise(new_tag)    # Setting new_tag to the higher priority than previous all tags

        except:
            messagebox.showerror('Invalid Selection', 'You need to select text to make any change on it')

        return 'break'

    def resource_path(self, relative_path):
        """ Get absolute path to resource from temporary directory

        In development:
            Gets path of photos that are used in this script like in icons and title_image from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of photos that are used in this script like in icons and title image from temporary directory"""

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path in _MEIPASS

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Sticky_Notes()
