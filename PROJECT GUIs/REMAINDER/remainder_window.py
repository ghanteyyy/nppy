import os
import time
from winsound import PlaySound, SND_LOOP, SND_ASYNC

try:  # Python 3
    from tkinter import Tk, Label, Button, IntVar

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import Tk, Label, Button, IntVar


def Remainder_Window(text):
    '''Remainder window to show remainders'''

    PlaySound('included files/tone.wav', SND_LOOP + SND_ASYNC)

    root = Tk()
    root.withdraw()
    root.after(0, root.deiconify)
    root.resizable(0, 0)
    root.config(bg='red')
    root.overrideredirect(True)
    root.title('BIRTHDAY REMAINDER')
    root.wm_attributes('-topmost', 1)
    root.geometry(f'405x160+{root.winfo_screenwidth() - 406}+0')

    title = Label(root, text='REMAINDER', font=("Courier", 30), bg='red', fg='White')
    wishes = Label(root, text=text, font=("Courier", 15), bg='red', fg='White')
    close_button = Button(root, text='CLOSE', font=("Courier", 12), bg='red', activeforeground='white', activebackground='red', fg='White', width=10, relief='ridge', command=root.destroy)

    title.pack()
    wishes.pack()
    close_button.pack(side='bottom', pady=5)

    root.mainloop()


def get_remainders():
    '''Getting all todays remainders'''

    remainder = {}

    if os.path.exists('remind_me.txt'):
        with open('remind_me.txt', 'r') as r_r:
            lines = r_r.readlines()

            for line in lines:
                split = line.strip('\n').split(' || ')

                if split[-1][:6] == time.strftime('%b %d'):    # If current month and date of txt file matches to the current month and date
                    remainder.update({split[0]: split[-1]})    # then updating to remainder dictionary

            return remainder


def remove_remainders(text, timee):
    '''Removing showed remainders from txt file'''

    with open('remind_me.txt', 'r') as r_r, open('remind_me.txt', 'w') as r_w:
        lines = r_r.readlines()

        for line in lines:
            check = '{} || {}\n'.format(text, timee)

            if check != line:
                r_w.write(line)


track = 0

if get_remainders():
    while True:
        todays_remainders = get_remainders()
        curr_time = time.strftime('%b %d %H %M %p')
        split_curr_time = [int(ct) if ct.isdigit() else ct for ct in curr_time.split()[2:4]]

        for text, timee in todays_remainders.items():
            if timee == curr_time:
                track += 1
                Remainder_Window(text)
                remove_remainders(text, timee)

        for text, timee in todays_remainders.items():
            split_timee = [int(tim) if tim.isdigit() else tim for tim in timee.split()[2:4]]

            if split_curr_time[0] > split_timee[0] or (split_curr_time[0] == split_timee[0] and split_curr_time[1] > split_timee[1]):
                track += 1
                Remainder_Window(text)
                remove_remainders(text, timee)

        if len(todays_remainders) == track:
                break
