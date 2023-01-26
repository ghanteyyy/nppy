import os
import sys
import json
import random
import string
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Scrollbar


class StickyNotes:
    def __init__(self):
        self.all_tags = {}
        self.json_filename = os.path.abspath(os.path.join('.', 'config.json'))
        self.text_filename = os.path.abspath(os.path.join('.', 'sticky_notes.txt'))

        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.wm_attributes('-topmost', True)
        self.master.iconbitmap(self.resource_path('icon.ico'))

        self.master.title('STICKY NOTES')
        self.width, self.height = 301, 290
        self.screen_width, self.screen_height = self.master.winfo_screenwidth() - 10, 10
        self.master.geometry(f"{self.width}x{self.height}+{self.screen_width - self.width}+{self.screen_height}")

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

        self.format_frame = Frame(self.master, bg='#fffed1')
        self.button_attributes = {'master': self.format_frame, 'bd': 0, 'bg': '#fffed1', 'activebackground': '#fffed1', 'cursor': 'hand2'}

        self.bold_image = PhotoImage(file=self.resource_path('bold.png'))
        self.bold_button = Button(image=self.bold_image, **self.button_attributes, command=lambda: self.change_tags('bold'))
        self.bold_button.pack(side=LEFT)

        self.italic_image = PhotoImage(file=self.resource_path('italic.png'))
        self.italic_button = Button(image=self.italic_image, **self.button_attributes, command=lambda: self.change_tags('italic'))
        self.italic_button.pack(side=LEFT, padx=5)

        self.underline_image = PhotoImage(file=self.resource_path('underline.png'))
        self.underline_button = Button(image=self.underline_image, **self.button_attributes, command=lambda: self.change_tags('underline'))
        self.underline_button.pack(side=LEFT)

        self.overstrike_image = PhotoImage(file=self.resource_path('overstrike.png'))
        self.overstrike_button = Button(image=self.overstrike_image, **self.button_attributes, command=lambda: self.change_tags('overstrike'))
        self.overstrike_button.pack(side=LEFT, padx=5)

        self.format_frame.pack()

        self.text_widget.bind('<Control-a>', self.select_all)
        self.text_widget.bind('<BackSpace>', self.left_click)
        self.text_widget.bind('<Double-Button-1>', self.double_click)
        self.text_widget.bind('<Triple-Button-1>', self.triple_click)
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
        self.master.after(0, self.insert_on_startup)
        self.master.bind('<Alt-Key-F4>', self.on_exit)
        self.master.bind('<Button-1>', self.left_click)
        self.master.protocol('WM_DELETE_WINDOW', self.on_exit)

        self.master.config(bg='#fffed1')
        self.master.mainloop()

    def double_click(self, event=None):
        '''
        Make selection up-to the end of the line when user makes double left clicks
        '''

        self.text_widget.tag_delete('sel', '1.0', 'end')
        cursor_pos = self.text_widget.index('insert')
        line_end = self.text_widget.index(f'{cursor_pos.split(".")[0]}.end')

        if cursor_pos == line_end:
            return 'break'

    def triple_click(self, event=None):
        cursor_index = self.text_widget.index('insert').split('.')[0]
        text = self.text_widget.get(f'{cursor_index}.0', f'{cursor_index}.end').strip()

        if text:
            self.text_widget.tag_add('sel', f'{cursor_index}.0', f'{cursor_index}.end')

        return 'break'

    def left_click(self, event=None):
        '''
        Make cursor visible when user left clicks if hidden previously when
        selecting all text with 'Ctrl + A'
        '''

        if self.text_widget['insertofftime'] > 300:
            self.text_widget.config(insertofftime=300, insertontime=600)

    def select_all(self, event=None):
        '''
        Select all text when user clicks Select-All option or Ctrl+A
        '''

        total_lines = int(self.text_widget.index('end-1c').split('.')[0]) + 1

        for line in range(1, total_lines):
            self.text_widget.tag_add('sel', f'{line}.0', f'{line}.end')

        self.text_widget.config(insertofftime=1000000, insertontime=0)

        return 'break'

    def save_formatting(self, event=None):
        '''
        Saves text styles like bold, italic, underline or overstrike as well as
        starting_index and ending_index of that style in config.json
        '''

        self.text_widget.tag_remove('sel', '1.0', 'end')  # Removing all selected area from the text widget.
        self.text_widget.mark_set('insert', END)  # Moving cursor to the end of the text widget.
        all_formats = self.text_widget.dump('1.0', 'end')[:-1]  # Getting tag_names, text and starting_index_of_that_tag_name except the last character i.e newline.

        tracker = 0
        is_tag_on = True
        style, formatter = [], []

        for tag_name, text, index in all_formats:
            if tag_name == 'text':
                is_tag_on = True

                if style:
                    start_index = index
                    end_index = all_formats[tracker + 1][2]
                    formatter.append({'style': style, 'start_index': start_index, 'end_index': end_index})

                    style = []

            elif tag_name == 'tagon' and is_tag_on:
                is_tag_on = False
                style.extend(self.all_tags[text])

            tracker += 1

        if formatter:
            with open(self.json_filename, 'w') as f:  # Saving formatting and indexes.
                json.dump(formatter, f, indent=4)

    def apply_formatting(self):
        '''
        Apply text styles stored in config.json within starting_index and ending_index
        '''

        try:
            with open(self.json_filename, 'r') as f:
                contents = json.load(f)

                for content in contents:
                    self.change_tags(content['style'], content['start_index'], content['end_index'])

        except json.decoder.JSONDecodeError:
            pass

    def insert_on_startup(self):
        '''
        Inserts text stored in 'sticky_notes.txt' and apply the formatting(if
        available) to the text widget right after the program starts
        '''

        try:
            with open(self.text_filename, 'r') as f:
                contents = f.read().strip('\n')

            if os.path.exists(self.json_filename):
                self.text_widget.insert('1.0', contents)
                self.apply_formatting()

            else:
                messagebox.showerror('Config file not found', 'Any text styles like bold, italic, underline or overstrike won\'t get applied.')
                self.text_widget.insert('1.0', contents)

        except FileNotFoundError:  # When sticky_notes.txt doesn't exists.
            pass

    def on_exit(self, event=None):
        '''
        Saves text in sticky_notes.txt, styling and indexes in config.json
        before destroying the window
        '''

        contents = self.text_widget.get('1.0', END).strip('\n')

        if contents:
            with open(self.text_filename, 'w') as f:
                f.write(contents)

            self.save_formatting()

        self.master.destroy()
        return 'break'

    def tag_exists(self, start_index):
        '''
        Checking if the selected text has already another tag
        '''

        if self.text_widget.tag_names(start_index)[1:]:
            return True

        return False

    def change_tags(self, tag, start_index='sel.first', end_index='sel.last'):
        '''
        Change text styles to bold, italic, underline or overstrike
        '''

        new_tag = ''.join([random.choice(string.ascii_letters) for _ in range(10)])   # Generating new tags.

        try:
            if self.tag_exists(start_index):
                last_tag = self.text_widget.tag_names(start_index)[-1]    # Getting name of last tag used.
                states = self.all_tags[last_tag]

                if tag in states:
                    new_states = [state for state in states if state != tag]

                else:
                    new_states = [state for state in states] + [tag]

            else:
                if isinstance(tag, list):
                    new_states = tag

                else:
                    new_states = [tag]

            self.all_tags[new_tag] = new_states

            use_tags = tuple(new_states)
            fnt = self.font + use_tags

            self.text_widget.tag_add(new_tag, start_index, end_index)
            self.text_widget.tag_configure(new_tag, font=fnt)
            self.text_widget.tag_raise(new_tag)  # Setting new_tag to the higher priority than all previous tags.

        except TclError:
            messagebox.showerror('Invalid Selection', 'You must select text to make any change on it')

        return 'break'

    def resource_path(self, file_name):
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
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    StickyNotes()
