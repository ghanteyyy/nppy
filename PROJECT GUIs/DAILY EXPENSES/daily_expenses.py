import os
import sys
import time
import winsound
from tkinter import *


class Daily_Expenses:
    '''Daily Expenses is built for tracking the expenses you spent in any item.'''

    def __init__(self):
        self.file = 'daily_expenses.txt'

        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.title('DAILY EXPENSES')
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))

        self.width, self.height = 448, 570
        self.screen_width, self.screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width- self.width // 2}+{self.screen_height - self.height // 2}')

        self.items_box_var = StringVar()
        self.items_box = Entry(self.master, width=70, fg='grey', highlightbackground='blue', highlightthickness=2, justify=CENTER, textvariable=self.items_box_var)
        self.items_box_var.set('ITEMS')
        self.items_box.grid(row=0, column=0, ipady=7, padx=10, pady=10)

        self.price_box_var = StringVar()
        self.price_box = Entry(self.master, width=70, fg='grey', highlightbackground='blue', highlightthickness=2, justify=CENTER, textvariable=self.price_box_var)
        self.price_box_var.set('PRICE')
        self.price_box.grid(row=1, column=0, ipady=7, padx=10, pady=5)

        self.display_box = Text(self.master, width=52, fg='black', highlightbackground='blue', highlightthickness=2, state=DISABLED, cursor='arrow')
        self.display_box.grid(row=2, column=0, pady=10)

        self.submit_box = Button(self.master, text='SUBMIT', width=59, bg='green', fg='white', activebackground='green', activeforeground='white', command=self.submit_command)
        self.submit_box.grid(row=3, column=0, ipady=10, padx=10)

        self.preload()

        self.items_box.bind('<Button-1>', lambda e: self.bind_entry(self.items_box_var, 'ITEMS', self.items_box))
        self.items_box.bind('<FocusIn>', lambda e: self.bind_entry(self.items_box_var, 'ITEMS', self.items_box))
        self.items_box.bind('<FocusOut>', lambda e: self.bind_entry(self.items_box_var, 'ITEMS', self.items_box, 'FocusOut'))

        self.price_box.bind('<Button-1>', lambda e: self.bind_entry(self.price_box_var, 'PRICE', self.price_box))
        self.price_box.bind('<FocusIn>', lambda e: self.bind_entry(self.price_box_var, 'PRICE', self.price_box))
        self.price_box.bind('<FocusOut>', lambda e: self.bind_entry(self.price_box_var, 'PRICE', self.price_box, 'FocusOut'))

        self.submit_box.bind('<Return>', lambda e: self.submit_box())
        self.master.bind('<Button-1>', self.enter_leave)
        self.master.bind_class('Entry', '<Return>', lambda e: self.submit_command())

        self.master.mainloop()

    def bind_entry(self, var, cond, widget, bind_type=None):
        '''Bindings entry boxes when user left clicks or use tab to move in/out boxes'''

        get = var.get().strip()

        if get == cond and not bind_type:
            var.set('')
            widget.config(fg='black')

        if bind_type == 'FocusOut' and not get:
            var.set(cond)
            widget.config(fg='grey')

    def enter_leave(self, event):
        '''Changes text and text color in entry boxes when user clicks outside of entry boxes'''

        if event.widget in [self.master, self.display_box]:
            if not self.items_box_var.get().strip():
                self.items_box_var.set('ITEMS')
                self.items_box.config(fg='grey')

            if not self.price_box_var.get().strip():
                self.price_box_var.set('PRICE')
                self.price_box.config(fg='grey')

            self.master.focus()

        elif event.widget == self.items_box and not self.price_box_var.get().strip():
            self.price_box_var.set('PRICE')
            self.price_box.config(fg='grey')

        elif event.widget == self.price_box and not self.items_box_var.get().strip():
            self.items_box_var.set('ITEMS')
            self.items_box.config(fg='grey')

    def preload(self):
        '''Display content of a file at the startup of program'''

        if not os.path.exists(self.file) or os.path.getsize(self.file) == 0:
            self.center_the_text('Your Expenses will be displayed here', 'grey')

        else:
            self.write_to_text_box()

    def write_to_text_box(self):
        '''Display contents that are stored in daily_expenses.txt'''

        self.display_box.config(state=NORMAL)
        self.display_box.delete('1.0', END)
        self.display_box.config(state=DISABLED)

        with open(self.file, 'r') as rf:
            lines = rf.readlines()

            for line in lines:
                self.center_the_text(line, 'black')

    def center_the_text(self, text, color):
        '''Centering each texts in Text widget'''

        self.display_box.config(state=NORMAL)
        self.display_box.config(fg=color)
        self.display_box.tag_configure('center', justify='center')
        self.display_box.insert('end', text, 'center')
        self.display_box.config(state=DISABLED)

    def submit_command(self):
        '''Action for submit button'''

        TIME = time.strftime('%d %b %a')
        get_item = self.items_box.get().strip().title()
        get_price = self.price_box.get().strip()

        if get_item == 'ITEMS' or get_price == 'PRICE':
            winsound.MessageBeep()

        else:
            if not os.path.exists(self.file):
                with open(self.file, 'w'):
                    pass

            with open(self.file, 'r') as f:
                lines = f.readlines()
                in_line = [line for line in lines if get_item in line.title()]    # Checking if get_item is in file

            if in_line:
                price = int(in_line[0].split('|')[-1].strip(' Rs. ')) + int(get_price)
                write = '{} | {} | Rs. {}\n'.format(TIME, get_item, price)

                index = lines.index(in_line[0])
                lines[index] = write      # Replace old value with new value

            else:
                write = f'{TIME} | {get_item} | Rs. {get_price}\n'
                lines.append(write)

            lines.sort(key=len)

            with open(self.file, 'w') as wf:
                for line in lines:
                    wf.write(line)

            for widget, value in {self.items_box: 'ITEMS', self.price_box: 'PRICE'}.items():
                widget.delete(0, END)
                widget.insert(END, value)
                widget.config(fg='grey')

            self.write_to_text_box()
            self.master.focus()

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
    Daily_Expenses()
