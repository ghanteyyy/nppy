from tkinter import *


class custom_countdown:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('CUSTOM COUNTDOWN')
        self.master.geometry(f'342x81+{self.master.winfo_screenwidth() // 2 - 342 // 2}+{self.master.winfo_screenheight() // 2 - 81 // 2}')
        self.master.resizable(0, 0)
        self.master.iconbitmap('included files/icon.ico')

        self.start_button = Button(self.master, text='START', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, command=self.start)
        self.start_button.grid(row=1, column=0, sticky='e')

        self.pause_button = Button(self.master, text='PAUSE', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, state='disabled', command=self.pause)
        self.pause_button.grid(row=1, column=1)

        self.reset_button = Button(self.master, text='RESET', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, state='disabled', command=self.reset)
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

        self.master.focus()

    def activate_edit(self):
        '''Activate editing mode in hour, minute and second entry box'''

        self.hour_entry.config(state='normal', cursor='xterm')
        self.minute_entry.config(state='normal', cursor='xterm')
        self.second_entry.config(state='normal', cursor='xterm')

    def pause(self, event=None):
        '''Command for self.pause button'''

        self.pause = True
        self.pause_button['state'] = 'disabled'
        self.activate_edit()

    def reset(self, event=None):
        '''Command for RESET button'''

        self.pause = True
        self.pause_button['state'] = 'disabled'
        self.reset_button['state'] = 'disabled'

        self.hr_var.set('HH')
        self.min_var.set('MM')
        self.sec_var.set('SS')

        self.activate_edit()

    def Counter(self):
        '''Updating hour, minute and seconds'''

        if self.pause is False:
            self.start_button['state'] = 'disabled'

            if self.hour == self.minute == self.second == 0:
                self.hour, self.minute, self.second = 'HH', 'MM', 'SS'
                self.pause_button['state'] = 'disabled'
                self.reset_button['state'] = 'disabled'
                self.activate_edit()
                self.pause = True

            elif self.second == 0:
                if self.minute == self.second == 0:
                    self.hour -= 1

                if self.minute == 0:
                    self.minute = 59

                else:
                    self.minute -= 1

                self.second = 59

            else:
                self.second -= 1

            self.hr_var.set(str(self.hour).zfill(2))
            self.min_var.set(str(self.minute).zfill(2))
            self.sec_var.set(str(self.second).zfill(2))

            self.master.after(1000, self.Counter)

        else:
            self.start_button['state'] = 'normal'

    def start(self, event=None):
        '''Command for START button'''

        self.pause = False

        get_hour, get_minute, get_second = self.hour_entry.get(), self.minute_entry.get(), self.second_entry.get()

        if len(get_hour) == 0 or not get_hour.isdigit():
            self.hour = 24

        if len(get_minute) == 0 or not get_minute.isdigit():
            self.minute = 0

        if len(get_second) == 0 or not get_second.isdigit():
            self.second = 2

        if get_minute.isdigit() and get_minute.isdigit():
            if int(get_minute) > 60:
                self.minute = 59

            if int(get_second) > 60:
                self.second = 60

            else:
                self.minute = int(get_minute)
                self.second = int(get_second)

        if get_hour.isdigit():
            self.hour = int(get_hour)

        self.start_button['state'] = 'disabled'
        self.pause_button['state'] = 'normal'
        self.reset_button['state'] = 'normal'

        self.hour_entry.config(state='disabled', cursor='arrow')
        self.minute_entry.config(state='disabled', cursor='arrow')
        self.second_entry.config(state='disabled', cursor='arrow')

        self.master.focus()
        self.master.after(1000, self.Counter)


if __name__ == '__main__':
    root = Tk()
    custom_countdown(root)
    root.mainloop()
