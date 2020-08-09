import os
import sys
from tkinter import *


class Custom_Countdown:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('CUSTOM COUNTDOWN')
        self.master.geometry(f'342x81+{self.master.winfo_screenwidth() // 2 - 342 // 2}+{self.master.winfo_screenheight() // 2 - 81 // 2}')
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))

        self.start_button = Button(self.master, text='START', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, cursor='hand2', command=self.start)
        self.start_button.grid(row=1, column=0, sticky='e')

        self.pause_button = Button(self.master, text='PAUSE', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, cursor='hand2', state='disabled', command=self.pause)
        self.pause_button.grid(row=1, column=1)

        self.reset_button = Button(self.master, text='RESET', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, cursor='hand2', state='disabled', command=self.reset)
        self.reset_button.grid(row=1, column=2)

        self.hr_var, self.min_var, self.sec_var = StringVar(), StringVar(), StringVar()

        self.time_frame = Frame(self.master, bg='dark blue')
        self.hour_entry = Entry(self.time_frame, bg='red', width=5, textvariable=self.hr_var, justify='center', font=("Courier", 18, 'bold'), disabledbackground='red', disabledforeground='black')
        self.hour_entry.grid(row=0, column=0, padx=2, pady=5)
        self.minute_entry = Entry(self.time_frame, bg='orange', width=5, textvariable=self.min_var, justify='center', font=("Courier", 18, 'bold'), disabledbackground='orange', disabledforeground='black')
        self.minute_entry.grid(row=0, column=1, padx=2, pady=5)
        self.second_entry = Entry(self.time_frame, bg='brown', width=5, textvariable=self.sec_var, justify='center', font=("Courier", 18, 'bold'), disabledbackground='brown', disabledforeground='black')
        self.second_entry.grid(row=0, column=2, padx=2, pady=5)
        self.time_frame.grid(row=2, column=0, columnspan=3)

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
        self.pause_button.bind('<Return>', self.pause)
        self.reset_button.bind('<Return>', self.reset)

        self.master['bg'] = 'dark blue'

        self.hour = 0
        self.minute = 0
        self.second = 0
        self.pause = False

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

    def activate_deactivate_buttons(self, widgets=None, entries=None):
        '''Enable or disable buttons or entry_boxes'''

        if widgets:   # Enabling or disabling buttons
            for widget, state in widgets.items():
                widget.config(state=state)

        if entries:   # Enabling or disabling entry_boxes
            for widget in entries[0]:
                widget.config(state=entries[1][0], cursor=entries[1][1])

    def pause(self, event=None):
        '''Command for self.pause button'''

        self.pause = True
        self.activate_deactivate_buttons(widgets={self.pause_button: 'disabled'}, entries=[(self.hour_entry, self.minute_entry, self.second_entry), ('normal', 'xterm')])

    def reset(self, event=None):
        '''Command for RESET button'''

        self.pause = True
        self.activate_deactivate_buttons(widgets={self.start_button: 'normal', self.pause_button: 'disabled', self.reset_button: 'disabled'}, entries=[(self.hour_entry, self.minute_entry, self.second_entry), ('normal', 'xterm')])
        self.set_var('HH', 'MM', 'SS')
        self.hour, self.minute, self.second = 0, 0, 0

    def set_var(self, hrs, mins, secs):
        '''Appending hour, minute and second values'''

        self.hr_var.set(str(hrs).zfill(2))
        self.min_var.set(str(mins).zfill(2))
        self.sec_var.set(str(secs).zfill(2))

    def Counter(self):
        '''Updating hour, minute and seconds'''

        if self.pause is False:
            self.activate_deactivate_buttons(widgets={self.start_button: 'disabled'})

            if self.hour == self.minute == self.second == 0:
                self.reset()
                self.activate_deactivate_buttons(entries=[(self.hour_entry, self.minute_entry, self.second_entry), ('normal', 'xterm')])
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
            self.master.after(1000, self.Counter)

        else:
            self.activate_deactivate_buttons(widgets={self.start_button: 'normal'})

    def start(self, event=None):
        '''Command for START button'''

        self.pause = False

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

        self.activate_deactivate_buttons(widgets={self.start_button: 'disabled', self.pause_button: 'normal', self.reset_button: 'normal'}, entries=[(self.hour_entry, self.minute_entry, self.second_entry), ('disabled', 'arrow')])
        self.master.focus()
        self.master.after(1000, self.Counter)

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
    Custom_Countdown()
