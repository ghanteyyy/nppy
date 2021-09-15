import os
import sys
from tkinter import *
from tkinter import messagebox


class Custom_Countdown:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('CUSTOM COUNTDOWN')
        self.master.geometry(f'295x88+{self.master.winfo_screenwidth() // 2 - 295 // 2}+{self.master.winfo_screenheight() // 2 - 88 // 2}')
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('icon.ico'))

        self.buttons_attributes = {'font': ('Courier', 16), 'bg': 'dark blue', 'fg': 'white', 'activebackground': 'dark blue', 'width': 11, 'cursor': 'hand2'}
        self.entry_attributes = {'width': 5, 'justify': 'center', 'font': ('Courier', 18, 'bold'), 'disabledforeground': 'black'}

        self.start_button = Button(self.master, text='START', **self.buttons_attributes, command=self.start)
        self.start_button.grid(row=1, column=0, sticky='e')

        self.reset_button = Button(self.master, text='RESET', **self.buttons_attributes, command=self.reset)
        self.reset_button.grid(row=1, column=2)

        self.hr_var, self.min_var, self.sec_var = StringVar(), StringVar(), StringVar()

        self.time_frame = Frame(self.master, bg='dark blue')
        self.hour_entry = Entry(self.time_frame, bg='red', textvariable=self.hr_var, disabledbackground='red', **self.entry_attributes)
        self.hour_entry.grid(row=0, column=0, padx=2, pady=5)
        self.minute_entry = Entry(self.time_frame, bg='orange', textvariable=self.min_var, disabledbackground='orange', **self.entry_attributes)
        self.minute_entry.grid(row=0, column=1, padx=2, pady=5)
        self.second_entry = Entry(self.time_frame, bg='brown', textvariable=self.sec_var, disabledbackground='brown', **self.entry_attributes)
        self.second_entry.grid(row=0, column=2, padx=2, pady=5)
        self.time_frame.grid(row=2, column=0, columnspan=3, pady=5)

        self.hour_entry.insert(END, 'HH')
        self.minute_entry.insert(END, 'MM')
        self.second_entry.insert(END, 'SS')

        self.hour_entry.bind('<Enter>', lambda e: self.enter_command(self.hour_entry, 'HH'))
        self.minute_entry.bind('<Enter>', lambda e: self.enter_command(self.minute_entry, 'MM'))
        self.second_entry.bind('<Enter>', lambda e: self.enter_command(self.second_entry, 'SS'))

        self.hour_entry.bind('<Leave>', lambda e: self.leave_command(self.hour_entry, 'HH'))
        self.minute_entry.bind('<Leave>', lambda e: self.leave_command(self.minute_entry, 'MM'))
        self.second_entry.bind('<Leave>', lambda e: self.leave_command(self.second_entry, 'SS'))

        self.hour_entry.bind('<Return>', self.start)
        self.minute_entry.bind('<Return>', self.start)
        self.second_entry.bind('<Return>', self.start)

        self.start_button.bind('<Return>', self.start)
        self.reset_button.bind('<Return>', self.reset)

        self.master['bg'] = 'dark blue'

        self.is_paused = False
        self.hour, self.minute, self.second = 0, 0, 0

        self.master.mainloop()

    def enter_command(self, widget, text):
        '''When cursor enters the widget'''

        widget.focus()
        widget.select_range(0, END)
        widget.select_from(0)

    def leave_command(self, widget, text):
        '''When cursor leaves the widget'''

        if len(widget.get()) == 0:
            widget.insert(END, text)
            widget.focus()

    def reset(self, event=None):
        '''Command for RESET button'''

        self.is_paused = False
        self.change_state('normal')
        self.set_var('HH', 'MM', 'SS')
        self.start_button.config(text='START')
        self.hour, self.minute, self.second = 0, 0, 0

        try:
            self.master.after_cancel(self.timer)

        except AttributeError:
            pass

    def set_var(self, hrs, mins, secs):
        '''Appending hour, minute and second values'''

        self.hr_var.set(str(hrs).zfill(2))
        self.min_var.set(str(mins).zfill(2))
        self.sec_var.set(str(secs).zfill(2))

    def Counter(self):
        '''Updating hour, minute and seconds'''

        if self.hour == self.minute == self.second == 0:
            messagebox.showinfo('Finished', 'Time UP!')
            self.reset()
            return

        elif self.second == self.minute == 0:
            self.hour -= 1
            self.second = 60
            self.minute = 59

        elif self.second == 0:
            self.minute -= 1
            self.second = 60

        self.second -= 1

        self.set_var(self.hour, self.minute, self.second)
        self.timer = self.master.after(1000, self.Counter)

    def start(self, event=None):
        '''Command for START / PAUSE button'''

        if not self.is_paused:  # When user clicks "START" button
            self.is_paused = True
            self.change_state('disabled')
            self.start_button.config(text='PAUSE')
            get_hour, get_minute, get_second = self.hour_entry.get().strip(), self.minute_entry.get().strip(), self.second_entry.get().strip()

            if not get_hour or not get_hour.isdigit():
                self.hour = 24

            elif not get_minute or not get_minute.isdigit():
                self.minute = 59

            elif not get_second or not get_second.isdigit():
                self.second = 60

            else:
                self.hour, self.minute, self.second = int(get_hour), int(get_minute), int(get_second)

            self.set_var(self.hour, self.minute, self.second)

            self.master.focus()
            self.master.after(1000, self.Counter)

        else:  # When user "PASTE" button
            self.is_paused = False
            self.change_state('normal')
            self.master.after_cancel(self.timer)
            self.start_button.config(text='START')

    def change_state(self, state):
        '''Change the state of entries widget as per "state" parameter '''

        for entry in [self.hour_entry, self.minute_entry, self.second_entry]:
            entry.config(state=state)

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

        return os.path.join(base_path, 'included_files', file_name)


if __name__ == '__main__':
    Custom_Countdown()
