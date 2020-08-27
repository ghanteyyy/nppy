import os
import sys
from tkinter import *


class Infinity_Countdown:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('INFINITY COUNTDOWN')
        self.master.geometry('{}x{}+{}+{}'.format(342, 108, self.master.winfo_screenwidth() // 2 - 342 // 2, self.master.winfo_screenheight() // 2 - 108 // 2))
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))
        self.master.config(bg='dark blue')

        self.time = Label(self.master, fg='silver', text='00:00:00', font=("Helvetica", 40), bg='dark blue')
        self.time.pack(side='bottom')

        self.start_button = Button(self.master, text='START', font=("Arial", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, cursor='hand2', command=self.start)
        self.start_button.pack(side='left')

        self.pause_button = Button(self.master, text='PAUSE', font=("Arial", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, state='disabled', cursor='hand2', command=self.pause)
        self.pause_button.pack(side='left')

        self.reset_button = Button(self.master, text='RESET', font=("Arial", 16), bg='dark blue', fg='white', activebackground='dark blue', width=10, state='disabled', cursor='hand2', command=self.reset)
        self.reset_button.pack(side='left', fill='both')

        self.hour = 0
        self.minute = 0
        self.second = 0
        self.pause = False

        self.master.mainloop()

    def start(self):
        '''Command for START button'''

        self.pause = False
        self.start_button['state'] = 'disabled'
        self.pause_button['state'] = 'normal'
        self.reset_button['state'] = 'normal'
        self.master.after(1000, self.Counter)

    def pause(self):
        '''Command for PAUSE button'''

        self.pause = True
        self.pause_button['state'] = 'disabled'

    def reset(self):
        '''Command for RESET button'''

        self.pause = True
        self.pause_button['state'] = 'disabled'
        self.reset_button['state'] = 'disabled'
        self.time['text'] = '00:00:00'

        self.hour, self.minute, self.second = 0, 0, 0

    def Counter(self):
        '''Updating hour, minute and seconds'''

        if self.pause is False:
            self.start_button['state'] = 'disabled'

            if self.second == self.minute == 59:
                self.hour += 1
                self.minute = 0
                self.second = -1

            elif self.second == 59:
                self.minute += 1
                self.second = -1

            self.second += 1

            self.time.config(text='{}:{}:{}'.format(str(self.hour).zfill(2), str(self.minute).zfill(2), str(self.second).zfill(2)))
            self.master.after(1000, self.Counter)

        else:
            self.start_button['state'] = 'normal'

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
    Infinity_Countdown()
