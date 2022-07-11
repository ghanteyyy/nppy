import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox


class MainWindow:
    def __init__(self):
        self.FileName = os.path.abspath(os.path.join('.', 'Remainder.txt'))
        self.master = Tk()

        self.width, self.height = 446, 200
        self.screen_width, self.screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'446x200+{self.screen_width - self.width // 2}+{self.screen_height - self.height // 2}')

        self.title_label = Label(self.master, text='REMIND ME!', fg='#cfb0be', bg='#6200ff', font=('ISOCP', 40, 'bold'))
        self.title_label.pack()

        self.entry_box_var = StringVar()
        self.entry_box_style = ttk.Style()
        self.entry_box_style.configure('E.TEntry', foreground='grey')
        self.entry_box = ttk.Entry(self.master, width=35, justify=CENTER, font=('Helvetica', 12, 'bold'), textvariable=self.entry_box_var, style='E.TEntry')
        self.entry_box_var.set('Remind Me About ...')
        self.entry_box.pack(pady=10, ipady=2)

        self.combo_box_frame = Frame(self.master, bg='#6200ff')

        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.combo_box_month = ttk.Combobox(self.combo_box_frame, value=self.months, width=8)
        self.combo_box_month.set('Month')
        self.combo_box_month.pack(side=LEFT, padx=1, ipady=2)

        self.combo_box_date = ttk.Combobox(self.combo_box_frame, value=self.get_combo_box_values(1, 32), width=5)
        self.combo_box_date.set('Date')
        self.combo_box_date.pack(side=LEFT, padx=1, ipady=2)

        self.combo_box_hour = ttk.Combobox(self.combo_box_frame, value=self.get_combo_box_values(1, 12), width=5)
        self.combo_box_hour.set('Hour')
        self.combo_box_hour.pack(side=LEFT, padx=1, ipady=2)

        self.combo_box_minute = ttk.Combobox(self.combo_box_frame, value=self.get_combo_box_values(0, 59), width=7)
        self.combo_box_minute.set('Minute')
        self.combo_box_minute.pack(side=LEFT, padx=1, ipady=2)

        self.combo_box_am_pm = ttk.Combobox(self.combo_box_frame, value=['AM', 'PM'], width=8)
        self.combo_box_am_pm.set('AM / PM')
        self.combo_box_am_pm.pack(side=LEFT, padx=1, ipady=2)

        self.combo_box_frame.pack(pady=3)

        self.add_button = Button(self.master, text='ADD REMAINDER', width=15, fg='#cfb0be', bg='#6200ff', font=('ISOCP', 15, 'bold'), activebackground='#6200ff', activeforeground='#cfb0be', border=0, command=self.add_command, cursor='hand2')
        self.add_button.pack(pady=10)

        self.master.after(0, self.initial_position)
        self.master.bind('<Button-1>', self.key_bindings)
        self.master.mainloop()

    def initial_position(self):
        '''Start the program in the center of the screen'''

        self.master.withdraw()
        self.master.update()

        width, height = self.master.winfo_width(), self.master.winfo_height() - 5
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

        self.master.resizable(0, 0)
        self.master.title('REMIND ME !')
        self.master.config(bg='#6200ff')
        self.master.iconbitmap(self.resource_path('icon.ico'))

        self.master.deiconify()

    def key_bindings(self, event):
        '''Action when user clicks inside entry widget or outside of the entry widget'''

        get_from_entry = self.entry_box.get().strip()

        if event.widget == self.entry_box:
            if get_from_entry == 'Remind Me About ...':
                self.entry_box_var.set('')
                self.entry_box_style.configure('E.TEntry', foreground='black')

        else:
            if not get_from_entry:
                self.entry_box_var.set('Remind Me About ...')
                self.entry_box_style.configure('E.TEntry', foreground='grey')

            self.master.focus()

    def get_combo_box_values(self, low, high):
        '''Get numbers of month, date, hour and min for month, date, hour and minute combobox'''

        return [str(i).zfill(2) for i in range(low, high + 1)]

    def add_command(self):
        '''Command when user clicks "Add Remainder" button'''

        try:
            message = self.entry_box_var.get().strip()
            month = self.combo_box_month.get().strip()
            date = self.combo_box_date.get().strip()
            hour = self.combo_box_hour.get().strip()
            minute = self.combo_box_minute.get().strip()
            am_pm = self.combo_box_am_pm.get().strip().upper()

            if not message or message == 'Remind Me About ...':
                messagebox.showerror('Invalid Remainder', 'Remainder is not given')

            elif month == 'Month' or month not in self.months:
                messagebox.showerror('Invalid Month', 'Select Valid Month')

            elif not date or date == 'Date' or int(date) not in range(1, 13):
                messagebox.showerror('Invalid Date', 'Date must be in between 1-12')

            elif not hour or hour == 'Hour' or int(hour) not in range(1, 13):
                messagebox.showerror('Invalid Hour', 'Hour must be in between 1-12')

            elif not minute or minute == 'Minute' or int(minute) not in range(0, 60):
                messagebox.showerror('Invalid Minute', 'Minute must be in between 0-59')

            elif am_pm == 'AM/PM' or am_pm not in ['AM', 'PM']:
                messagebox.showerror('Invalid period', 'Period must be AM or PM')

            else:
                if not os.path.exists(self.FileName):
                    with open(self.FileName, 'w'):
                        pass

                with open(self.FileName, 'a') as f:
                    write = f'{message} | {month} {date} {hour} {minute} {am_pm}\n'
                    f.write(write)

                self.entry_box_var.set('Remind Me About ...')
                self.entry_box_style.configure('E.TEntry', foreground='grey')

                self.combo_box_month.set('Month')
                self.combo_box_hour.set('Hour')
                self.combo_box_date.set('Date')
                self.combo_box_minute.set('Minute')
                self.combo_box_am_pm.set('AM / PM')
                self.master.focus()

                messagebox.showinfo('Remainder Added', f'You will reminded in {month} {date} {hour}:{minute} {am_pm}')

        except ValueError:
            messagebox.showerror('Invalid Input', 'Date / Hour / Minute is excepted in numbers')

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
    MainWindow()
