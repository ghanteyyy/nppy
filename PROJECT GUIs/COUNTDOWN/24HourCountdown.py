import os
import sys
from tkinter import *


class TwentyFourHourCountdown:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('24 Hour COUNTDOWN')
        self.master.geometry(f'326x82+{self.master.winfo_screenwidth() // 2 - 326 // 2}+{self.master.winfo_screenheight() // 2 - 82 // 2}')
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.config(bg='dark blue')

        self.time_label = Label(self.master, text='24:00:00', font=('Courier', 50, 'bold'), bg='dark blue', fg='silver')
        self.time_label.pack(fill='both')

        self.sec = 0
        self.min = 0
        self.hrs = 24
        self.pause = False

        self.master.after(1000, self.Counter)
        self.master.mainloop()

    def Counter(self):
        '''
        Updating hour, minute and seconds
        '''

        if self.pause is False:
            if self.sec == self.min == self.hrs == 0:
                self.pause = True
                self.time_label.config(text='Time Up!', font=('Courier', 40, 'bold'))
                return

            elif self.sec == self.min == 0:
                self.hrs -= 1
                self.min = 59
                self.sec = 60

            elif self.sec == 0:
                self.min -= 1
                self.sec = 60

            self.sec -= 1

            self.time_label.config(text=f'{str(self.hrs).zfill(2)}:{str(self.min).zfill(2)}:{str(self.sec).zfill(2)}')
            self.master.after(1000, self.Counter)

    def resource_path(self, file_name):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    TwentyFourHourCountdown()
