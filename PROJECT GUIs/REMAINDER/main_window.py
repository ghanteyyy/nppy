import os
import sys

try:  # Python 3
    from tkinter import *
    from tkinter import messagebox
    from tkinter.ttk import Combobox

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *
    from ttk import Combobox
    import tkMessageBox as messagebox


class GUI:
    def __init__(self):
        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.title('REMIND ME !')
        self.master.config(bg='#6200ff')
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))

        self.width, self.height = 446, 200
        self.screen_width, self.screen_heigth = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'446x200+{self.screen_width - self.width // 2}+{self.screen_heigth - self.height // 2}')

        self.title_label = Label(self.master, text='REMIND ME!', fg='#cfb0be', bg='#6200ff', font=('ISOCP', 40, 'bold'))
        self.title_label.pack()

        self.entry_box_var = StringVar()
        self.entry_box = Entry(self.master, fg='#8a86ad', width=33, font=('ISOCP', 12, 'bold'), textvariable=self.entry_box_var, justify=CENTER)
        self.entry_box_var.set('Remind Me About ...')
        self.entry_box.pack(pady=10)

        self.combo_box_frame = Frame(self.master)

        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.combo_box_month = Combobox(self.combo_box_frame, value=self.months, width=8)
        self.combo_box_month.set('Month')
        self.combo_box_month.pack(side=LEFT)

        self.combo_box_date = Combobox(self.combo_box_frame, value=self.get_combo_box_values(1, 32), width=5)
        self.combo_box_date.set('Date')
        self.combo_box_date.pack(side=LEFT)

        self.combo_box_hour = Combobox(self.combo_box_frame, value=self.get_combo_box_values(1, 12), width=5)
        self.combo_box_hour.set('Hour')
        self.combo_box_hour.pack(side=LEFT)

        self.combo_box_minute = Combobox(self.combo_box_frame, value=self.get_combo_box_values(0, 59), width=7)
        self.combo_box_minute.set('Minute')
        self.combo_box_minute.pack(side=LEFT)

        self.combo_box_am_pm = Combobox(self.combo_box_frame, value=['AM', 'PM'], width=8)
        self.combo_box_am_pm.set('AM / PM')
        self.combo_box_am_pm.pack(side=LEFT)

        self.combo_box_frame.pack(pady=10)

        self.add_button = Button(self.master, text='ADD REMAINDER', width=15, fg='#cfb0be', bg='#6200ff', font=('ISOCP', 15, 'bold'), activebackground='#6200ff', activeforeground='#cfb0be', border=0, command=self.add_command, cursor='hand2')
        self.add_button.pack(pady=10)

        self.master.bind('<Button-1>', self.key_bindings)
        self.master.mainloop()

    def key_bindings(self, event):
        '''Different action when user clicks to different widgets'''

        if event.widget == self.entry_box:
            self.entry_box_var.set('')
            self.entry_box.config(fg='black')

        elif event.widget in [self.master, self.title_label]:
            if not self.entry_box_var.get().strip():
                self.entry_box_var.set('Remind Me About ...')
                self.entry_box.config(fg='grey')

            self.master.focus()

    def get_combo_box_values(self, low, high):
        '''Get values of date, hour and min for combobox'''

        return [str(i).zfill(2) for i in range(low, high + 1)]

    def add_command(self):
        '''When user click "Add Remainder" button'''

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

            elif not date or date == 'Date' or not int(date) in range(1, 13):
                messagebox.showerror('Invalid Date', 'Date must be in between 1-12')

            elif not hour or hour == 'Hour' or int(hour) not in range(1, 13):
                messagebox.showerror('Invalid Hour', 'Hour must be in between 1-12')

            elif not minute or minute == 'Minute' or int(minute) not in range(0, 60):
                messagebox.showerror('Invalid Minute', 'Minute must be in between 0-59')

            elif am_pm == 'AM/PM' or am_pm not in ['AM', 'PM']:
                messagebox.showerror('Invalid period', 'Period must be AM or PM')

            else:
                if not os.path.exists('Remainder.txt'):
                    with open('Remainder.txt', 'w'):
                        pass

                with open('Remainder.txt', 'a') as f:
                    write = f'{message} | {month} {date} {hour} {minute} {am_pm}\n'
                    f.write(write)

                self.entry_box_var.set('Remind Me About ...')
                self.entry_box.config(fg='grey')

                self.combo_box_month.set('Month')
                self.combo_box_hour.set('Hour')
                self.combo_box_minute.set('Minute')
                self.combo_box_am_pm.set('AM/PM')
                self.master.focus()

                messagebox.showinfo('Remainder Added', f'You will reminded in {month} {date} {hour}:{minute} {am_pm}')

        except ValueError:
            messagebox.showerror('Invalid Input', 'Date / Hour / Minute is excepted in numbers')

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
    GUI()
