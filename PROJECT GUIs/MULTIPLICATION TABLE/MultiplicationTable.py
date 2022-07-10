import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter import Scrollbar
from tkinter import messagebox
import pyperclip


class MultiplicationTable:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.title('Multiplication Table')

        self.num_var = StringVar()
        self.num_var.set('Number')
        self.upto_var = StringVar()
        self.upto_var.set('Upto')

        self.num_style = ttk.Style()
        self.num_style.configure('N.TEntry', foreground='grey')
        self.upto_style = ttk.Style()
        self.upto_style.configure('U.TEntry', foreground='grey')

        self.entry_frame = Frame(self.master)
        self.entry_frame.grid(row=0, column=0, sticky='NSEW')

        self.num_entry = ttk.Entry(self.entry_frame, width=40, textvariable=self.num_var, justify='center', style='N.TEntry')
        self.num_entry.grid(row=0, column=0, ipady=3, padx=5, sticky='NSEW')

        self.upto_entry = ttk.Entry(self.entry_frame, width=10, textvariable=self.upto_var, justify='center', style='U.TEntry')
        self.upto_entry.grid(row=0, column=1, ipady=3, padx=5, sticky='NSEW')

        self.table_frame = Frame(self.master)
        self.table_frame.grid(row=1, column=0, sticky='NSEW')

        self.table_text = Text(self.table_frame, width=40, height=10, cursor='arrow', state='disabled')
        self.table_text.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')

        self.vsb = Scrollbar(self.table_frame, orient='vertical', command=self.table_text.yview)
        self.vsb.grid(row=1, column=1, sticky='NS')
        self.table_text.configure(yscrollcommand=self.vsb.set)

        self.show_table = Button(self.master, width=40, text='SHOW TABLE', bg='#5e72b5', activebackground='#5e72b5', fg='white', activeforeground='white', bd='0', cursor='hand2', command=self.generate_table)
        self.show_table.grid(row=2, column=0, ipady=3, padx=5, sticky='NSEW')

        self.copy_button = Button(self.master, width=40, text='COPY', bg='green', activebackground='green', fg='white', activeforeground='white', bd='0', cursor='hand2', command=self.copy_to_clipboard)
        self.copy_button.grid(row=3, column=0, ipady=3, padx=5, pady=5, sticky='NSEW')

        self.master.bind('<Button-1>', self.master_binding)
        self.num_entry.bind('<FocusIn>', self.entry_binding)
        self.upto_entry.bind('<FocusIn>', self.entry_binding)
        self.num_entry.bind('<Return>', self.generate_table)
        self.upto_entry.bind('<Return>', self.generate_table)
        self.show_table.bind('<FocusIn>', self.master_binding)

        self.initial_position()
        self.master.mainloop()

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
        self.master.geometry(f'{width}x{height}+{pos_x}+{pos_y}')
        self.master.deiconify()

    def master_binding(self, event=None, widget=None):
        '''When user clicks anywhere outside of entry boxes and buttons'''

        if widget is None:
            widget = event.widget

        if widget not in [self.num_entry, self.upto_entry]:
            if not self.num_var.get().strip():
                self.num_var.set('Number')
                self.num_style.configure('N.TEntry', foreground='grey')

            if not self.upto_var.get().strip():
                self.upto_var.set('Upto')
                self.upto_style.configure('U.TEntry', foreground='grey')

            self.master.focus()

    def entry_binding(self, event=None):
        '''When focus changes in or out of the entry widget'''

        widget = event.widget

        if widget == self.num_entry:
            if not self.upto_var.get().strip():
                self.upto_var.set('Upto')
                self.upto_style.configure('U.TEntry', foreground='grey')

            if self.num_var.get().strip() == 'Number':
                self.num_var.set('')
                self.num_style.configure('N.TEntry', foreground='black')

        elif widget == self.upto_entry:
            if not self.num_var.get().strip():
                self.num_var.set('Number')
                self.num_style.configure('N.TEntry', foreground='grey')

            if self.upto_var.get().strip() == 'Upto':
                self.upto_var.set('')
                self.upto_style.configure('U.TEntry', foreground='black')

        else:
            self.master_binding(widget=self.master)

    def generate_table(self, event=None):
        '''Insert multiplication table in text_widget '''

        num = self.num_var.get().strip()
        upto = self.upto_var.get().strip()

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
    MultiplicationTable()
