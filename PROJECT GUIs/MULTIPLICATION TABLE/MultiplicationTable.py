import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter import Scrollbar
from tkinter import messagebox
import pyperclip


class _Entry:
    def __init__(self, master, default_text, style_name, generate_func):
        self.master = master
        self.isDefault = True
        self.var = StringVar()
        self.style_name = style_name
        self.default_text = default_text
        self.generate_func = generate_func

        self.Style = ttk.Style()
        self.var.set(self.default_text)
        self.Style.configure(self.style_name, foreground='grey')

        self.Entry = ttk.Entry(self.master, textvariable=self.var, justify='center', style=self.style_name)

        self.Entry.bind('<FocusIn>', self.FocusIn)
        self.Entry.bind('<FocusOut>', self.FocusOut)
        self.Entry.bind('<KeyPress>', self.KeyPressed)
        self.Entry.bind('<Return>', self.generate_func)

    def FocusIn(self, event=None):
        '''When user set focus to respective entry widget'''

        if self.isDefault:
            self.var.set('')
            self.isDefault = False
            self.Style.configure(self.style_name, foreground='black')

    def FocusOut(self, event=None):
        '''When user set focus out of respective entry widget'''

        if self.isDefault is False and not self.var.get().strip():
            self.isDefault = True
            self.var.set(self.default_text)
            self.Style.configure(self.style_name, foreground='grey')

    def KeyPressed(self, event=None):
        '''
        When user presses any character from the keyboard and if that
        character is not a digit then forcing tkinter not to insert
        that character
        '''

        char = event.keysym

        if char.isdigit() is False and char not in ['BackSpace', 'Delete', 'Left', 'Right', 'Tab']:
            return 'break'


class MultiplicationTable:
    def __init__(self):
        self.is_table_shown = False

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Multiplication Table')

        self.Style = ttk.Style()
        self.Style.theme_use('clam')
        self.Style.map('TEntry', lightcolor=[('focus', 'blue')])

        self.entry_frame = Frame(self.master)
        self.entry_frame.pack(pady=5)

        self.num_entry = _Entry(self.entry_frame, 'Number', 'N.TEntry', self.generate_table)
        self.num_entry.Entry.pack(side=LEFT, ipady=3, padx=(5, 0))

        self.upto_entry = _Entry(self.entry_frame, 'Upto', 'U.TEntry', self.generate_table)
        self.upto_entry.Entry.pack(side=LEFT, ipady=3, padx=(5, 0))

        self.generate_button = Button(self.entry_frame, width=10, text='GENERATE', bg='#5e72b5', activebackground='#5e72b5', fg='white', activeforeground='white', bd='0', cursor='hand2', command=self.generate_table)
        self.generate_button.pack(ipady=2, padx=(3, 2))

        self.table_frame = Frame(self.master)

        self.table_text = Text(self.table_frame, width=40, height=10, cursor='arrow', state='disabled')
        self.table_text.pack(side=LEFT, pady=(0, 5))

        self.vsb = Scrollbar(self.table_frame, orient='vertical', command=self.table_text.yview)
        self.vsb.pack(side=LEFT, fill='y')
        self.table_text.configure(yscrollcommand=self.vsb.set)

        self.copy_button = Button(self.master, width=47, text='COPY', bg='green', activebackground='green', fg='white', activeforeground='white', bd='0', cursor='hand2', command=self.copy_to_clipboard)

        self.initial_position()

        self.master.bind('<Button-1>', self.focus_everywhere)
        self.master.mainloop()

    def focus_everywhere(self, event=None):
        '''Focus to respective widgets where clicked'''

        event.widget.focus()

    def initial_position(self):
        '''Position window to the center of screen when the program opens'''

        self.master.update()
        self.master.iconbitmap(self.resource_path('icon.ico'))

        width = self.master.winfo_width()
        height = self.master.winfo_height()

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        pos_x = screen_width // 2 - width // 2
        pos_y = screen_height // 2 - height // 2

        self.master.resizable(0, 0)
        self.master.geometry(f'+{pos_x}+{pos_y}')
        self.master.deiconify()

    def generate_table(self, event=None):
        '''Insert multiplication table in text_widget '''

        num = self.num_entry.var.get().strip()
        upto = self.upto_entry.var.get().strip()

        try:
            num = int(num)

            if not upto or upto == 'Upto':
                upto = 10

            upto = int(upto) + 1
            self.table_text.config(state='normal')
            self.table_text.delete('1.0', 'end')

            for n in range(1, upto):
                table = f'{num} x {n} = {num * n}\n'

                if n == upto - 1:
                    table = table.strip('\n')

                self.table_text.insert('end', table)

            self.table_text.config(state='disabled')
            self.table_frame.pack()

            self.copy_button.pack(pady=(0, 5), ipady=5)

        except ValueError:
            messagebox.showinfo('ERR', 'Number must be integer')

    def copy_to_clipboard(self, event=None):
        '''Copy the multiplication table to the clipboard'''

        text = self.table_text.get('1.0', 'end').strip()

        if text:
            pyperclip.copy(text)
            self.copy_button.config(text='Copied!')
            self.master.after(1000, lambda: self.copy_button.config(text='Copy'))

    def resource_path(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    MultiplicationTable()
