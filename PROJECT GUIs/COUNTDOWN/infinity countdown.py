from tkinter import *

HOUR, MINUTE, SECOND = 0, 0, 0


def start():
    '''Command for START button'''

    global PAUSE

    PAUSE = False
    start_button['state'] = 'disabled'
    pause_button['state'] = 'normal'
    reset_button['state'] = 'normal'
    Counter()


def pause():
    '''Command for PAUSE button'''

    global PAUSE

    PAUSE = True
    pause_button['state'] = 'disabled'


def reset():
    '''Command for RESET button'''

    global HOUR, MINUTE, SECOND, PAUSE

    PAUSE = True
    pause_button['state'] = 'disabled'
    reset_button['state'] = 'disabled'
    time['text'] = '00:00:00'

    HOUR, MINUTE, SECOND = 0, 0, 0


def Counter():
    '''Updating hour, minute and seconds'''

    global HOUR, MINUTE, SECOND

    if PAUSE is False:
        start_button['state'] = 'disabled'

        if SECOND == 59:
            if MINUTE == SECOND == 59:
                HOUR += 1
                MINUTE = 0

            else:
                MINUTE += 1

            SECOND = -1

        SECOND += 1

        time.config(text='{}:{}:{}'.format(str(HOUR).zfill(2), str(MINUTE).zfill(2), str(SECOND).zfill(2)))
        root.after(1000, Counter)

    else:
        start_button['state'] = 'normal'


root = Tk()
root.withdraw()
root.after(1, root.deiconify)
root.title('INFINITY COUNTDOWN')
root.geometry('{}x{}+{}+{}'.format(342, 108, root.winfo_screenwidth() // 2 - 342 // 2, root.winfo_screenheight() // 2 - 108 // 2))
root.resizable(0, 0)
root.iconbitmap('icon.ico')
root.config(bg='dark blue')

time = Label(root, fg='silver', text='00:00:00', font=("Helvetica", 40), bg='dark blue')
time.pack(side='bottom')

start_button = Button(root, text='START', font=("Arial", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, command=start)
start_button.pack(side='left')

pause_button = Button(root, text='PAUSE', font=("Arial", 16), bg='dark blue', fg='white', activebackground='dark blue', width=8, state='disabled', command=pause)
pause_button.pack(side='left')

reset_button = Button(root, text='RESET', font=("Arial", 16), bg='dark blue', fg='white', activebackground='dark blue', width=10, state='disabled', command=reset)
reset_button.pack(side='left', fill='both')

root.mainloop()
