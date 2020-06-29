import os
import sys
import PIL.Image
import PIL.ImageTk
import winsound

try:  # Python 3
    from tkinter import *
    from tkinter.ttk import Combobox

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *
    from ttk import Combobox


class Birthday_Remainder:
    def __init__(self):
        self.file = 'birthday_remainder.txt'
        self.month_number = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    def Window(self):
        '''GUI window'''

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))
        self.master.title('Birthday Remainder')
        self.master.geometry(f'426x500+{self.master.winfo_screenwidth() // 2 - 426 // 2}+{self.master.winfo_screenheight() // 2 - 500 // 2}')

        # Inserting image
        self.birthday_quote_frame = Frame(self.master)
        self.birthday_quote_image = PIL.ImageTk.PhotoImage(PIL.Image.open(self.resource_path('included_files/image.jpg'), 'r'))
        self.label_birthday_quote = Label(self.birthday_quote_frame, image=self.birthday_quote_image)
        self.label_birthday_quote.grid(row=0, column=0)
        self.birthday_quote_frame.place(x=0, y=0)

        # Insert Name label and entry field
        self.label_entry_frame = Frame(self.master, bg='dark green')
        self.name_label = Label(self.label_entry_frame, text='Name', fg='white', font=('Courier', 12), bg='dark green')
        self.name_box = Entry(self.label_entry_frame, width=30)
        self.name_label.grid(row=0, column=0)
        self.name_box.grid(row=0, column=1, padx=30, pady=20)

        # Insert date of birth label
        self.birthday_label = Label(self.label_entry_frame, text='Date of Birth', fg='white', font=('Courier', 12), bg='dark green')
        self.birthday_label.grid(row=1, column=0)
        self.label_entry_frame.place(x=70, y=240)

        # Options to select month and dates
        self.combo_box_frame = Frame(self.master, bg='dark green')
        self.month_box = Combobox(self.combo_box_frame, values=[month for month in self.month_number], width=13)
        self.month_box.set('Select Month')
        self.month_box.grid(row=0, column=0)

        self.date_box = Combobox(self.combo_box_frame, values=[i for i in range(1, 32)], width=10)
        self.date_box.set('Select Date')
        self.date_box.grid(row=0, column=1, padx=5)

        self.combo_box_frame.place(x=235, y=300)

        # Insert radiobuttons add or delete
        self.var = IntVar()
        self.radio_frame = Frame(self.master, bg='dark green')
        self.add_radio_button = Radiobutton(self.radio_frame, text='Add', fg='#000000', activebackground='dark green', font=('Courier', 12), bg='dark green', value=1, variable=self.var, disabledforeground='black')
        self.delete_radio_button = Radiobutton(self.radio_frame, text='Delete', fg='#000000', activebackground='dark green', font=('Courier', 12), bg='dark green', value=2, variable=self.var, disabledforeground='black')
        self.add_radio_button.grid(row=0, column=0)
        self.delete_radio_button.grid(row=0, column=1)
        self.radio_frame.place(x=255, y=360)

        # Insert submit button
        self.button_frame = Frame(self.master)
        self.submit_button = Button(self.button_frame, text='SUBMIT', fg='white', bg='#039e05', activebackground='#039e05', font=('Courier', 12), width=16, height=3, relief=RAISED, command=self.add_info)
        self.submit_button.grid(row=2, column=0)
        self.button_frame.place(x=250, y=400)

        # Bind keys
        self.name_box.bind('<Return>', self.add_info)
        self.date_box.bind('<Return>', self.add_info)
        self.name_box.bind('<Enter>', lambda e: self.name_box.focus_set())

        self.master.config(bg='dark green')
        self.master.mainloop()

    def exists_details(self, name, date):
        '''Check if name and date provided is already in file or not'''

        with open(self.file, 'r') as details:
            lines = details.readlines()

            for line in lines:
                split = line.strip('\n').split(':')

                if split[0].strip() == name and split[1].strip():
                    return True

            return False

    def sort_details(self):
        '''Sort details alphabetically'''

        with open(self.file, 'r+') as read_write:
            lines = read_write.readlines()
            lines.sort()
            read_write.seek(0)

            for line in lines:
                read_write.write(line)

    def show_info(self, message, pos_x, pos_y):
        '''Display result to user'''

        self.error_frame = Frame(self.master, bg='dark green')
        self.label_error_message = Label(self.error_frame, text=message, font=('Courier', 20), fg='white', bg='dark green')
        self.label_error_message.grid(row=0, column=0)
        self.error_frame.place(x=pos_x, y=pos_y)

        self.master.update()
        self.master.after(1000, self.label_error_message.grid_forget)

    def add_info(self, event=None):
        '''Get value from user and add/delete them'''

        name = self.name_box.get().strip().upper()
        month = self.month_box.get()
        day = self.date_box.get()

        if len(name) == 0 or len(month) == 0:
            winsound.MessageBeep()
            self.show_info(message='Empty Field(s)', pos_x=15, pos_y=415)
            self.name_box.delete(0, END)

        elif month not in self.month_number or not day.isdigit() or day == 'Select Date' or month == 'Select Month':
            winsound.MessageBeep()
            self.show_info(message='Invalid Date', pos_x=25, pos_y=415)

        elif int(day) > 32 or int(day) == 0:
            winsound.MessageBeep()
            self.show_info(message='Invalid Date', pos_x=25, pos_y=415)

        elif self.var.get() != 1 and self.var.get() != 2:
            winsound.MessageBeep()
            self.show_info(message='No button\nselected', pos_x=50, pos_y=400)

        else:
            if not os.path.exists(self.file):   # Creating file if not exists
                with open(self.file, 'w'):
                    pass

            date = f'{self.month_number[month].zfill(2)}-{day.zfill(2)}'

            if self.var.get() == 1:
                if self.exists_details(name, date):
                    winsound.MessageBeep()
                    self.show_info(message='Details Exists', pos_x=12, pos_y=415)

                else:
                    with open(self.file, 'a') as append:
                        append.write(f'{name.ljust(30)}:{date.rjust(10)}\n')

                    self.show_info(message='Details Added', pos_x=17, pos_y=415)

                    # Setting all entry box and combo-box to defaults
                    self.name_box.delete(0, END)
                    self.month_box.delete(0, END)
                    self.month_box.set('Select Month')
                    self.date_box.delete(0, END)
                    self.date_box.set('Select Date')

            elif self.var.get() == 2:
                if not self.exists_details(name, date):
                    winsound.MessageBeep()
                    self.show_info(message='Invalid Details', pos_x=2, pos_y=415)

                else:
                    with open(self.file, 'r+') as read_write_details:
                        lines = read_write_details.readlines()
                        lines.remove(f'{name.ljust(30)}:{date.rjust(10)}\n')
                        read_write_details.seek(0)

                        for line in lines:
                            read_write_details.write(line)

                        read_write_details.truncate()

                    self.show_info(message='Details Deleted', pos_x=2, pos_y=415)

            self.sort_details()

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
    remainder = Birthday_Remainder()
    remainder.Window()
