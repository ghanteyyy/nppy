import os
import sys
import time
import winsound
import tkinter.ttk as ttk
from tkinter import Tk, Label, Button, IntVar


class Remainder_Window:
    def __init__(self):
        self.birthdates = {}
        self.todays_date = time.strftime('%m-%d')
        self.files = ['birthday_remainder.txt', 'seen_birthday.txt']
        self.month_number = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    def Window(self, name, date):
        '''GUI window for showing those whose have birthday today'''

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.resizable(0, 0)
        self.master.config(bg='red')
        self.master.overrideredirect(True)
        self.master.title('BIRTHDAY REMAINDER')
        self.master.wm_attributes('-topmost', 1)
        self.master.geometry(f'405x170+{self.master.winfo_screenwidth() - 406}+0')

        self.var = IntVar()
        self.style = ttk.Style()
        self.style.configure('Red.TCheckbutton', foreground='white', background='red')

        title = Label(self.master, text='REMAINDER', font=("Courier", 30), bg='red', fg='White')
        wishes = Label(self.master, text=f'Today is {name}\'s Birthday\n({date})', font=("Courier", 15), bg='red', fg='White', wraplength=450)
        check_button = ttk.Checkbutton(self.master, style='Red.TCheckbutton', text='Don\'t show again', variable=self.var)
        close_button = Button(self.master, text='CLOSE', font=("Courier", 12), bg='red', activeforeground='white', activebackground='red', fg='White', width=10, relief='ridge', command=lambda: self.quit_button(name))

        title.pack()
        wishes.pack()
        check_button.pack(side='bottom')
        close_button.pack(side='bottom')

        self.master.mainloop()

    def read_file(self, filename):
        '''Storing name and birthdates from the given name of file in a dictionary'''

        dic = {}

        with open(filename, 'r') as f:
            lines = [line.strip('\n') for line in f.readlines()]

            for line in lines:
                split = line.split(':')
                dic.update({split[0].strip(): split[1].strip()})

        return dic

    def get_today_birthdays(self):
        '''Getting name and date of those whose birthday is today'''

        try:
            all_birthdates = self.read_file(self.files[0])

            if os.path.exists(self.files[1]):
                today_birthdates = self.read_file(self.files[1])

                for name, date in all_birthdates.items():
                    if name not in today_birthdates and date == self.todays_date:  # If birthdates from 'birthday_remainder.txt' is same as todays_date and name is not in 'seen_birthday.txt'
                        self.birthdates.update({name: date})

            else:
                for name, date in all_birthdates.items():
                    if date == self.todays_date:
                        self.birthdates.update({name: date})

        except FileNotFoundError:
            return

    def quit_button(self, name):
        '''Command when close button is closed.

           When close button is clicked with selecting the check_button that means
           don't show remainder of that name again. So this function saves those
           names to seen_birthday.txt and excludes the stored birthdates next time
           when this script runs'''

        if self.var.get() == 1:
            if not os.path.exists(self.files[1]):
                with open(self.files[1], 'w'):
                    pass

            with open(self.files[1], 'a') as tf:
                tf.write(f'{name.ljust(30)}:{self.birthdates[name].rjust(10)}\n')

        self.master.destroy()

    def remove_file(self):
        '''Removing seen_birthday.txt if date in that file does not match from
           today's date'''

        if os.path.exists(self.files[1]):
            contents = self.read_file(self.files[1])

            for key, value in contents.items():
                if value != self.todays_date:
                    os.remove(self.files[1])
                    return

    def main(self):
        '''Getting, showing and removing birthdays'''

        self.remove_file()
        self.get_today_birthdays()

        if self.birthdates:
            for name, date in self.birthdates.items():
                winsound.PlaySound(self.resource_path('included_files/tone.wav'), winsound.SND_LOOP + winsound.SND_ASYNC)
                self.Window(name, date)

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

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    remainder = Remainder_Window()
    remainder.main()
