import os
import sys
import time
from tkinter import *
from tkinter import font


class StopWatch:
    def __init__(self):
        self.start_time = self.elapsed_time = 0.0
        self.has_started = False

        self.master = Tk()
        self.master.withdraw()
        self.master.title('StopWatch')
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.resizable(0, 0)
        self.master.config(bg='dark blue')
        self.time_var = StringVar()
        self.time_var.set('00:00:00')

        self.time_label = Label(self.master, textvariable=self.time_var, bg='dark blue', fg='white', font=font.Font(size=20))
        self.time_label.pack(padx=5)

        self.buttons_frame = Frame(self.master, bg='dark blue')
        self.buttons_frame.pack(padx=5, pady=5)

        self.start_pause_button = Button(self.buttons_frame, text='Start', width=7, font=font.Font(size=15), cursor='hand2', bg='dark blue', fg='white', activebackground='dark blue', activeforeground='white', command=self.start_pause)
        self.start_pause_button.grid(row=0, column=0)

        self.reset_button = Button(self.buttons_frame, text='Reset', width=7, font=font.Font(size=15), cursor='hand2', bg='dark blue', fg='white', activebackground='dark blue', activeforeground='white', command=self.reset)
        self.reset_button.grid(row=0, column=1, padx=10)

        self.master.after(0, self.initial_position)
        self.master.mainloop()

    def initial_position(self):
        '''Position of window when program starts'''

        self.master.update()

        width, height = self.master.winfo_width(), self.master.winfo_height()
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2

        self.master.geometry(f'250x90+{screen_width - width}+{screen_height - height}')
        self.master.deiconify()

    def start_pause(self, event=None):
        '''When user Start or Pause button is clicked'''

        if self.has_started:
            self.master.after_cancel(self.timer)
            self.elapsed_time = time.time() - self.start_time
            self.has_started = False
            self.start_pause_button.config(text='Start')

        else:
            self.start_time = time.time() - self.elapsed_time
            self.update()

            self.has_started = True
            self.start_pause_button.config(text='Pause')

    def reset(self, event=None):
        '''When reset button is clicked'''

        self.elapsed_time = 0.0
        self.has_started = False
        self.start_time = time.time()
        self.time_var.set('00:00:00')
        self.start_pause_button.config(text='Start')

        try:
            self.master.after_cancel(self.timer)

        except AttributeError:
            pass

    def update(self):
        '''Update hour, minute, second and millisecond'''

        self.elapsed_time = time.time() - self.start_time

        minutes = int(self.elapsed_time / 60)
        seconds = int(self.elapsed_time - minutes * 60.0)
        hseconds = int((self.elapsed_time - minutes * 60.0 - seconds) * 100)

        self.time_var.set(f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}:{str(hseconds).zfill(2)}')
        self.timer = self.master.after(50, self.update)

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
    StopWatch()
