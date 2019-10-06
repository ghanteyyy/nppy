import os
import time
from winsound import PlaySound, SND_LOOP, SND_ASYNC

try:  # Python 3
    import tkinter.ttk as ttk
    from tkinter import Tk, Label, Button, IntVar

except (ImportError, ModuleNotFoundError):  # Python 2
    import ttk
    from Tkinter import Tk, Label, Button, IntVar


today_birthdates = {}
current_date = time.strftime('%Y-%m-%d\n')


def quit_button(name, date):
    '''When close button is clicked'''

    if var.get() == 1:
        with open('details.txt', 'w') as r_d:     # Removing showed name and date from the file
            for line in lines:
                if line != '{}{}\n'.format(name.ljust(50), date):
                    r_d.write(line)

    root.destroy()


def get_birthdates():
    '''Get today birthdates from the file'''

    global lines

    with open('details.txt', 'r') as birthdates:
        lines = birthdates.readlines()

        for line in lines:
            split = line.split()

            if split[-1] == current_date.strip()[5:]:
                today_birthdates.update({split[0]: split[-1]})


def Remainder_Window(name, date):
    '''Display birthday'''

    global root, var

    root = Tk()
    root.withdraw()
    root.after(0, root.deiconify)
    root.resizable(0, 0)
    root.config(bg='red')
    root.overrideredirect(True)
    root.title('BIRTHDAY REMAINDER')
    root.wm_attributes('-topmost', 1)
    root.geometry(f'405x160+{root.winfo_screenwidth() - 406}+0')

    var = IntVar()
    style = ttk.Style()
    style.configure('Red.TCheckbutton', foreground='white', background='red')

    title = Label(root, text='BIRTHDAY REMAINDER', font=("Courier", 25, "bold"), bg='red', fg='white')
    wishes = Label(root, text=f'Today is {name}\'s Birthday\n({date})', font=("Courier", 15), bg='red', fg='White')
    check_button = ttk.Checkbutton(root, style='Red.TCheckbutton', text='Don\'t show again', variable=var)
    close_button = Button(root, text='CLOSE', font=("Courier", 12), bg='red', activeforeground='white', activebackground='red', fg='White', width=10, relief='ridge', command=lambda: quit_button(name, date))

    title.pack()
    wishes.pack()
    check_button.pack(side='bottom')
    close_button.pack(side='bottom')

    root.mainloop()


def main():
    '''Main function of the entire script'''

    get_birthdates()

    if len(today_birthdates) != 0:
        for name, date in today_birthdates.items():
            PlaySound('tone.wav', SND_LOOP + SND_ASYNC)
            Remainder_Window(name, date)


if __name__ == '__main__':
    if os.path.exists('details.txt'):
        main()
