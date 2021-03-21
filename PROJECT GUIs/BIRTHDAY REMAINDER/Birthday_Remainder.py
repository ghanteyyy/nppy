import os
import sys
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox


class Birthday_Remainder:
    def __init__(self):
        self.file = 'birthday_remainder.txt'
        self.month_number = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
        self.label_attributes = {'fg': 'white', 'font': ('Courier', 12), 'bg': 'dark green'}

        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.title('Birthday Remainder')

        self.width, self.height = 426, 470
        self.screen_width, self.screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width // 2 - self.width // 2}+{self.screen_height // 2 - self.height // 2}')

        self.birthday_quote_frame = Frame(self.master)
        self.birthday_quote_image = PhotoImage(file=self.resource_path('image.png'))
        self.label_birthday_quote = Label(self.birthday_quote_frame, image=self.birthday_quote_image)
        self.label_birthday_quote.grid(row=0, column=0)
        self.birthday_quote_frame.place(x=0, y=0)

        self.label_entry_frame = Frame(self.master, bg='dark green')
        self.name_label = Label(self.label_entry_frame, text='Name', **self.label_attributes)
        self.name_box = Entry(self.label_entry_frame, width=30)
        self.name_label.grid(row=0, column=0)
        self.name_box.grid(row=0, column=1, padx=30, pady=20, ipady=2)

        self.birthday_label = Label(self.label_entry_frame, text='Date of Birth', **self.label_attributes)
        self.birthday_label.grid(row=1, column=0)
        self.label_entry_frame.place(x=70, y=240)

        self.combo_box_frame = Frame(self.master, bg='dark green')
        self.month_box = ttk.Combobox(self.combo_box_frame, values=[month for month in self.month_number], width=12, height=9)
        self.month_box.set('Select Month')
        self.month_box.grid(row=0, column=0)

        self.date_box = ttk.Combobox(self.combo_box_frame, values=[i for i in range(1, 32)], width=10, height=9)
        self.date_box.set('Select Date')
        self.date_box.grid(row=0, column=1, padx=5)

        self.combo_box_frame.place(x=235, y=305)

        self.var = IntVar()
        self.style = ttk.Style()
        self.style.configure('R.TRadiobutton', background='dark green', foreground='white')

        self.radio_frame = Frame(self.master, bg='dark green')
        self.add_radio_button = ttk.Radiobutton(self.radio_frame, text='Add', value=1, variable=self.var, style='R.TRadiobutton', cursor='hand2')
        self.delete_radio_button = ttk.Radiobutton(self.radio_frame, text='Delete', value=2, variable=self.var, style='R.TRadiobutton', cursor='hand2')
        self.add_radio_button.grid(row=0, column=0, padx=10)
        self.delete_radio_button.grid(row=0, column=1)
        self.radio_frame.place(x=255, y=350)

        self.button_frame = Frame(self.master)
        self.submit_button = Button(self.button_frame, text='SUBMIT', fg='white', bg='#039e05', activebackground='#039e05', activeforeground='white', cursor='hand2', font=('Courier', 12), width=16, height=3, bd=0, relief=GROOVE, command=self.submit_command)
        self.submit_button.grid(row=2, column=0)
        self.button_frame.place(x=250, y=390)

        self.name_box.bind('<Return>', self.submit_command)
        self.date_box.bind('<Return>', self.submit_command)
        self.master.bind('<Button-1>', self.master_bindings)

        self.master.after(0, self.master.deiconify)
        self.master.config(bg='dark green')
        self.master.mainloop()

    def master_bindings(self, event=None):
        '''When user clicks outside of the Entry box'''

        if event.widget not in [self.name_box, self.month_box, self.date_box]:
            if not self.month_box.get().strip():
                self.month_box.set('Select Month')

            if not self.date_box.get().strip():
                self.date_box.set('Select Date')

            self.master.focus()

    def submit_command(self, event=None):
        '''Command for submit button'''

        success = False
        var = self.var.get()
        day = self.date_box.get().strip()
        month = self.month_box.get().strip()
        name = self.name_box.get().strip().upper()

        if not name or not month:
            messagebox.showerror('No Input', 'Name and date of birthday was expected')
            self.name_box.delete(0, END)

        elif month not in self.month_number:
            messagebox.showerror('Invalid Month', 'Month was expected between Jan-Dec')

        elif not day.isdigit() or not 0 < int(day) <= 32:
            messagebox.showerror('Invalid Date', 'Date was expected between 1-32')

        elif var not in [1, 2]:
            messagebox.showerror('Invalid Option', 'Either Add or Remove button was expected')

        else:
            if not os.path.exists(self.file):   # Creating file if not exists
                with open(self.file, 'w'):
                    pass

            date = f'{self.month_number[month].zfill(2)}-{day.zfill(2)}'
            details = f'{name.ljust(30)}:{date.rjust(10)}\n'

            with open(self.file, 'r+') as f:
                contents = f.readlines()

                if var == 1:
                    if details in contents:
                        messagebox.showerror('EXISTS', 'Name and Date of Birth already exists in file')

                    else:
                        success = True
                        contents.append(details)
                        messagebox.showinfo('ADDED', 'Name and Date of Birth is added to the file')

                elif var == 2:
                    if details not in contents:
                        messagebox.showerror('Invalid', 'Name and Date of Birth is not in file')

                    else:
                        success = True
                        contents.remove(details)
                        messagebox.showinfo('REMOVED', 'Name and Date of Birth removed from the file')

                contents.sort()
                f.seek(0)

                for content in contents:
                    f.write(content)

                f.truncate()

            if success:
                for widget in [self.date_box, self.name_box, self.month_box]:
                    widget.delete(0, END)

                self.var.set(0)
                self.date_box.set('Select Date')
                self.month_box.set('Select Month')

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS.

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, 'included_files', relative_path)


if __name__ == '__main__':
    Birthday_Remainder()
