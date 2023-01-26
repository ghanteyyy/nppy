import os
import sys
from tkinter import *


class InfinityCountdown:
    def __init__(self):
        self.hour = self.minute = self.second = 0
        self.is_running = False  # Track if program has started running
        self.is_paused = False  # Track if timer is paused. True for paused and False for not paused

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('INFINITY COUNTDOWN')
        self.master.geometry('{}x{}+{}+{}'.format(295, 108, self.master.winfo_screenwidth() // 2 - 342 // 2, self.master.winfo_screenheight() // 2 - 108 // 2))
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.config(bg='dark blue')

        self.buttons_attributes = {'font': ('Arial', 16), 'fg': 'white', 'bg': 'dark blue', 'activebackground': 'dark blue', 'activeforeground': 'white', 'cursor': 'hand2', 'width': 12, 'takefocus': False}
        self.time = Label(self.master, fg='silver', text='00:00:00', font=("Helvetica", 40), bg='dark blue')
        self.time.pack(side='bottom')

        self.start_pause_button = Button(self.master, text='START', **self.buttons_attributes, command=self.start)
        self.start_pause_button.pack(side='left')

        self.reset_button = Button(self.master, text='RESET', **self.buttons_attributes, command=self.reset)
        self.reset_button.pack(side='left', fill='both')

        self.master.mainloop()

    def start(self):
        '''
        Command for START button
        '''

        if self.is_paused:  # Pause program if program is running.
            self.is_paused = False
            self.start_pause_button.config(text="START")

        else:  # Resume program if program is paused.
            self.is_paused = True

            if self.is_running is False:  # Call counter method only is self.is_running is False
                self.is_running = True
                self.master.after(1000, self.counter)

            self.start_pause_button.config(text='PAUSE')

    def reset(self):
        '''
        Command for RESET button
        '''

        self.is_paused = False
        self.time['text'] = '00:00:00'
        self.hour = self.minute = self.second = 0
        self.start_pause_button.config(text='START')

    def counter(self):
        '''
        Updating hour, minute and seconds
        '''

        if self.is_paused:
            if self.second == self.minute == 59:
                self.hour += 1
                self.minute = 0
                self.second = -1

            elif self.second == 59:
                self.minute += 1
                self.second = -1

            self.second += 1
            self.time.config(text='{}:{}:{}'.format(str(self.hour).zfill(2), str(self.minute).zfill(2), str(self.second).zfill(2)))

        self.timer = self.master.after(1000, self.counter)

    def resource_path(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    InfinityCountdown()
