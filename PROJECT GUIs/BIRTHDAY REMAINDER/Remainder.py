import os
from datetime import datetime
from winsound import PlaySound, SND_LOOP, SND_ASYNC

try:  # Python 3
    import tkinter.ttk as ttk
    from tkinter import Tk, Label, Button, IntVar
    from winreg import ConnectRegistry, OpenKey, SetValueEx, KEY_WRITE, KEY_SET_VALUE, REG_SZ, HKEY_CURRENT_USER    # Python 3.x

except (ImportError, ModuleNotFoundError):  # Python 2
    import ttk
    from Tkinter import Tk, Label, Button, IntVar
    from _winreg import ConnectRegistry, OpenKey, SetValueEx, KEY_WRITE, KEY_SET_VALUE, REG_SZ, HKEY_CURRENT_USER    # Python 2.x


birthday_list, today_birthdates = {}, {}


def startup():
    '''Add to the startup'''

    areg = ConnectRegistry(None, HKEY_CURRENT_USER)

    try:
        akey = OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Remainder.exe', 0, KEY_WRITE)
        areg.Close()
        akey.Close()

    except WindowsError:
        key = OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, KEY_SET_VALUE)
        SetValueEx(key, 'Birthday Remainder', 0, REG_SZ, r'C:\ProgramData\Birthday Remainder\Remainder.exe')
        areg.Close()
        key.Close()


def is_today():
    '''Check if today's date is in file'''

    with open('mark_read.txt', 'r') as check_seen:
        lines = check_seen.readlines()

        if len(lines) != 0 and datetime.now().strftime('%Y-%m-%d\n') in lines[0]:
            pass

        else:
            with open('mark_read.txt', 'w'):
                pass


def check_file():
    '''Create file if not exists'''

    if not os.path.exists('mark_read.txt'):
        with open('mark_read.txt', 'w'):
            pass


def quit_button(name, date):
    '''When close button is clicked'''

    if var.get() == 1:
        seen_birthday(name, date)

    root.destroy()


def mark_read(name, date):
    '''Check if birthday is already seen by user (when check button is checked)'''

    with open('mark_read.txt', 'r') as notseen:
        lines = notseen.readlines()

    if f'{name.ljust(50)}{date}\n' in lines:
        return False

    else:
        return True


def seen_birthday(name, date):
    '''Save seen birthday to a file'''

    with open('mark_read.txt', 'r+') as seen_write:
        lines = seen_write.readlines()

        if datetime.now().strftime('%Y-%m-%d\n') not in lines:
            seen_write.write(datetime.now().strftime('%Y-%m-%d\n'))
            seen_write.write(f'{name.ljust(50)}{date}\n')

        else:
            seen_write.write(f'{name.ljust(50)}{date}\n')

        seen_write.truncate()


def get_birthdates():
    '''Get birth dates from the file'''

    with open('details.txt', 'r') as birthdates:
        lines = birthdates.readlines()

        for line in lines:
            birthday_list[line.split(' ')[0]] = line.split()[-1].strip('\n')  # Appending name and date to the birthday_list dictionary


def Remainder_Window(name, date):
    '''Display birthday'''

    global root, var

    root = Tk()
    root.resizable(0, 0)
    root.config(bg='red')
    root.overrideredirect(True)
    root.title('BIRTHDAY REMAINDER')
    root.wm_attributes('-topmost', 1)
    root.geometry(f'405x160+{root.winfo_screenwidth() - 406}+0')

    var = IntVar()
    style = ttk.Style()
    style.configure('Red.TCheckbutton', foreground='white', background='red')

    title = Label(root, text='REMAINDER', font=("Courier", 30), bg='red', fg='White')
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

    startup()
    check_file()
    get_birthdates()

    for name, date in birthday_list.items():
        if str(datetime.now())[5:10] == birthday_list[name]:   # Checking if there is anyone's birthday
            today_birthdates.update({name: date})

    if len(today_birthdates) != 0:
        is_today()

        for name, date in today_birthdates.items():
            if mark_read(name, date):
                PlaySound('tone.wav', SND_LOOP + SND_ASYNC)

                Remainder_Window(name, date)


if __name__ == '__main__':
    try:
        if os.path.exists('details.txt'):
            main()

    except FileNotFoundError:
        pass
