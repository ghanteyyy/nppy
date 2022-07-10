import os
import sys
import time
from tkinter import *
from tkinter import messagebox


class DailyExpenses:
    '''Daily Expenses is built for tracking the expenses you spent in any item.'''

    def __init__(self):
        self.file = os.path.abspath(os.path.join('.', 'daily_expenses.txt'))
        self.entry_attributes = {'width': 70, 'fg': 'grey', 'highlightbackground': 'blue', 'highlightcolor': 'blue', 'highlightthickness': 2, 'justify': CENTER}

        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.title('DAILY EXPENSES')
        self.master.after(0, self.master.deiconify)
        self.master.iconbitmap(self.resource_path('icon.ico'))

        self.width, self.height = 448, 570
        self.screen_width, self.screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width- self.width // 2}+{self.screen_height - self.height // 2}')

        self.items_box_var = StringVar()
        self.items_box = Entry(self.master, **self.entry_attributes, textvariable=self.items_box_var)
        self.items_box_var.set('ITEMS')
        self.items_box.grid(row=0, column=0, ipady=7, padx=10, pady=10)

        self.price_box_var = StringVar()
        self.price_box = Entry(self.master, **self.entry_attributes, textvariable=self.price_box_var)
        self.price_box_var.set('PRICE')
        self.price_box.grid(row=1, column=0, ipady=7, padx=10, pady=5)

        self.display_box = Text(self.master, width=52, fg='black', highlightbackground='blue', highlightcolor='blue', highlightthickness=2, state=DISABLED, cursor='arrow')
        self.display_box.grid(row=2, column=0, pady=10)

        self.submit_box = Button(self.master, text='SUBMIT', width=59, bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=self.submit_command)
        self.submit_box.grid(row=3, column=0, ipady=10, padx=10)

        self.master.bind('<Button-1>', self.bind_keys)
        self.price_box.bind('<FocusIn>', self.bind_keys)
        self.items_box.bind('<FocusIn>', self.bind_keys)
        self.price_box.bind('<Return>', self.submit_command)
        self.items_box.bind('<Return>', self.submit_command)
        self.submit_box.bind('<Return>', self.submit_command)
        self.price_box.bind('<FocusOut>', lambda event, focus_out=True: self.bind_keys(event, focus_out))

        self.master.after(100, self.preload)
        self.master.mainloop()

    def bind_keys(self, event, focus_out=False):
        '''Commands when user clicks in and out of the entries widgets'''

        get_from_item_box = self.items_box_var.get().strip()
        get_from_price_box = self.price_box_var.get().strip()

        if event.widget == self.items_box or focus_out:
            if get_from_item_box == 'ITEMS' and not focus_out:
                self.items_box_var.set('')
                self.items_box.config(fg='black')

            if not get_from_price_box:
                self.price_box_var.set('PRICE')
                self.price_box.config(fg='grey')

        elif event.widget == self.price_box:
            if get_from_price_box == 'PRICE':
                self.price_box_var.set('')
                self.price_box.config(fg='black')

            if not get_from_item_box:
                self.items_box_var.set('ITEMS')
                self.items_box.config(fg='grey')

        if event.widget in [self.master, self.display_box]:
            if not get_from_item_box:
                self.items_box_var.set('ITEMS')
                self.items_box.config(fg='grey')

            if not get_from_price_box:
                self.price_box_var.set('PRICE')
                self.price_box.config(fg='grey')

            self.master.focus()

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

    def submit_command(self, event=None):
        '''Commands when user cilcks submit button'''

        current_time = time.strftime('%d %b %a')
        get_item = self.items_box.get().strip().title()
        get_price = self.price_box.get().strip()

        if get_item == 'ITEMS' or get_price == 'PRICE':
            messagebox.showerror('Invalid Fields', 'Some fields left empty')

        else:
            if not os.path.exists(self.file):
                with open(self.file, 'w'):
                    pass

            with open(self.file, 'r') as f:
                lines = f.readlines()
                in_line = [line for line in lines if get_item in line.title()]    # Checking if get_item is in file

            if in_line:
                price = int(in_line[0].split('|')[-1].strip(' Rs. ')) + int(get_price)
                write = '{} | {} | Rs. {}\n'.format(current_time, get_item, price)

                index = lines.index(in_line[0])
                lines[index] = write      # Replace old value with new value

            else:
                write = f'{current_time} | {get_item} | Rs. {get_price}\n'
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
    DailyExpenses()
