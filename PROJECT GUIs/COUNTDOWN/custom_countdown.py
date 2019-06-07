from tkinter import *

HOUR, MINUTE, SECOND = 0, 0, 0


def enter_command(widget, text):
    '''When cursor enters the widget'''

    widget.focus()
    widget.select_range(0, END)
    widget.select_from(0)


def leave_command(widget, text):
    '''When cursor leaves the widget'''

    if len(widget.get()) == 0:
        widget.insert(END, text)
        widget.focus()

    root.focus()


def activate_edit():
    '''Activate editing mode in hour, minute and second entry box'''

    hour_entry.config(state='normal', cursor='xterm')
    minute_entry.config(state='normal', cursor='xterm')
    second_entry.config(state='normal', cursor='xterm')


def start(event=None):
    '''Command for START button'''

    global HOUR, MINUTE, SECOND, PAUSE

    PAUSE = False

    get_hour, get_minute, get_second = hour_entry.get(), minute_entry.get(), second_entry.get()

    if len(get_hour) == 0 or not get_hour.isdigit():
        HOUR = 24

    if len(get_minute) == 0 or not get_minute.isdigit():
        MINUTE = 0

    if len(get_second) == 0 or not get_second.isdigit():
        SECOND = 2

    if get_minute.isdigit() and get_minute.isdigit():
        if int(get_minute) > 60:
            MINUTE = 59

        if int(get_second) > 60:
            SECOND = 60

        else:
            MINUTE = int(get_minute)
            SECOND = int(get_second)

    if get_hour.isdigit():
        HOUR = int(get_hour)

    start_button['state'] = 'disabled'
    pause_button['state'] = 'normal'
    reset_button['state'] = 'normal'

    hour_entry.config(state='disabled', cursor='arrow')
    minute_entry.config(state='disabled', cursor='arrow')
    second_entry.config(state='disabled', cursor='arrow')

    root.focus()
    Counter()


def pause(event=None):
    '''Command for PAUSE button'''

    global PAUSE

    PAUSE = True
    pause_button['state'] = 'disabled'
    activate_edit()


def reset(event=None):
    '''Command for RESET button'''

    global HOUR, MINUTE, SECOND, PAUSE

    PAUSE = True
    pause_button['state'] = 'disabled'
    reset_button['state'] = 'disabled'

    hr_var.set('HH')
    min_var.set('MM')
    sec_var.set('SS')

    activate_edit()


def Counter():
    '''Updating hour, minute and seconds'''

    global HOUR, MINUTE, SECOND, PAUSE

    if PAUSE is False:
        start_button['state'] = 'disabled'

        if HOUR == MINUTE == SECOND == 0:
            HOUR, MINUTE, SECOND = 'HH', 'MM', 'SS'
            pause_button['state'] = 'disabled'
            reset_button['state'] = 'disabled'
            activate_edit()
            PAUSE = True

        elif SECOND == 0:
            if MINUTE == SECOND == 0:
                HOUR -= 1

            if MINUTE == 0:
                MINUTE = 59

            else:
                MINUTE -= 1

            SECOND = 59

        else:
            SECOND -= 1

        hr_var.set(str(HOUR).zfill(2))
        min_var.set(str(MINUTE).zfill(2))
        sec_var.set(str(SECOND).zfill(2))

        root.after(1000, Counter)

    else:
        start_button['state'] = 'normal'


root = Tk()
root.withdraw()
root.after(1, root.deiconify)
root.title('CUSTOM COUNTDOWN')
root.geometry(f'342x81+{root.winfo_screenwidth() // 2 - 342 // 2}+{root.winfo_screenheight() // 2 - 81 // 2}')
root.resizable(0, 0)
root.iconbitmap('icon.ico')

start_button = Button(root, text='START', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, command=start)
start_button.grid(row=1, column=0, sticky='e')

pause_button = Button(root, text='PAUSE', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, state='disabled', command=pause)
pause_button.grid(row=1, column=1)

reset_button = Button(root, text='RESET', font=("Courier", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, state='disabled', command=reset)
reset_button.grid(row=1, column=2)

hr_var, min_var, sec_var = StringVar(), StringVar(), StringVar()

time_frame = Frame(root, bg='dark blue')
hour_entry = Entry(time_frame, bg='red', width=5, textvariable=hr_var, justify='center', font=("Courier", 18, 'bold'), disabledbackground='red', disabledforeground='black')
hour_entry.grid(row=0, column=0, padx=2, pady=5)
minute_entry = Entry(time_frame, bg='orange', width=5, textvariable=min_var, justify='center', font=("Courier", 18, 'bold'), disabledbackground='orange', disabledforeground='black')
minute_entry.grid(row=0, column=1, padx=2, pady=5)
second_entry = Entry(time_frame, bg='brown', width=5, textvariable=sec_var, justify='center', font=("Courier", 18, 'bold'), disabledbackground='brown', disabledforeground='black')
second_entry.grid(row=0, column=2, padx=2, pady=5)
time_frame.grid(row=2, column=0, columnspan=3)

hour_entry.insert(END, 'HH')
minute_entry.insert(END, 'MM')
second_entry.insert(END, 'SS')

hour_entry.bind('<Enter>', lambda e: enter_command(hour_entry, 'HH'))
minute_entry.bind('<Enter>', lambda e: enter_command(minute_entry, 'MM'))
second_entry.bind('<Enter>', lambda e: enter_command(second_entry, 'SS'))

hour_entry.bind('<Leave>', lambda e: leave_command(hour_entry, 'HH'))
minute_entry.bind('<Leave>', lambda e: leave_command(minute_entry, 'MM'))
second_entry.bind('<Leave>', lambda e: leave_command(second_entry, 'SS'))

hour_entry.bind('<Return>', start)
minute_entry.bind('<Return>', start)
second_entry.bind('<Return>', start)

start_button.bind('<Return>', start)
pause_button.bind('<Return>', pause)
reset_button.bind('<Return>', reset)

root['bg'] = 'dark blue'
root.mainloop()
