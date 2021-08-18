import os
import sys
from tkinter import *


class Infinity_Countdown:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('INFINITY COUNTDOWN')
        self.master.geometry('{}x{}+{}+{}'.format(295, 108, self.master.winfo_screenwidth() // 2 - 342 // 2, self.master.winfo_screenheight() // 2 - 108 // 2))
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))
        self.master.config(bg='dark blue')

        self.buttons_attributes = {'font': ('Arial', 16), 'fg': 'white', 'bg': 'dark blue', 'activebackground': 'dark blue', 'activeforeground': 'white', 'cursor': 'hand2', 'width': 12, 'takefocus': False}
        self.time = Label(self.master, fg='silver', text='00:00:00', font=("Helvetica", 40), bg='dark blue')
        self.time.pack(side='bottom')

        self.start_pause_button = Button(self.master, text='START', **self.buttons_attributes, command=self.start)
        self.start_pause_button.pack(side='left')

        self.reset_button = Button(self.master, text='RESET', **self.buttons_attributes, command=self.reset)
        self.reset_button.pack(side='left', fill='both')

        self.hour = self.minute = self.second = 0
        self.is_paused = False

        self.master.mainloop()

    def start(self):
        '''Command for START button'''

        if not self.is_paused:
            self.is_paused = True
            self.start_pause_button.config(text='PAUSE')
            self.master.after(1000, self.Counter)

        else:
            self.is_paused = False
            self.master.after_cancel(self.timer)
            self.start_pause_button.config(text="START")

    def reset(self):
        '''Command for RESET button'''

        self.is_paused = False
        self.time['text'] = '00:00:00'
        self.hour = self.minute = self.second = 0

        try:
            self.master.after_cancel(self.timer)

        except AttributeError:
            pass

    def Counter(self):
        '''Updating hour, minute and seconds'''

        if self.second == self.minute == 59:
            self.hour += 1
            self.minute = 0
            self.second = -1

        elif self.second == 59:
            self.minute += 1
            self.second = -1

        self.second += 1

        self.time.config(text='{}:{}:{}'.format(str(self.hour).zfill(2), str(self.minute).zfill(2), str(self.second).zfill(2)))
        self.timer = self.master.after(1000, self.Counter)

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            path = sys.argv

            if path:
                base_path = os.path.split(path[0])[0]

            else:
                base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Infinity_Countdown()
