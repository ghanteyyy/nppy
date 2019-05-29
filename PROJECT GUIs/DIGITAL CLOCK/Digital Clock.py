import time

try:  # Python 3
    from tkinter import Tk, Frame, Label
    from winreg import ConnectRegistry, OpenKey, SetValueEx, KEY_WRITE, KEY_SET_VALUE, REG_SZ, HKEY_CURRENT_USER    # Python 3.x

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import Tk, Frame, Label
    from _winreg import ConnectRegistry, OpenKey, SetValueEx, KEY_WRITE, KEY_SET_VALUE, REG_SZ, HKEY_CURRENT_USER    # Python 2.x


def startup():
    '''Add to the startup'''

    areg = ConnectRegistry(None, HKEY_CURRENT_USER)

    try:
        akey = OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run\Digital Clock.exe', 0, KEY_WRITE)
        areg.Close()
        akey.Close()

    except WindowsError:
        key = OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, KEY_SET_VALUE)
        SetValueEx(key, 'Digital Clock', 0, REG_SZ, r'C:\ProgramData\Digital Clock\Digital Clock.exe')
        areg.Close()
        key.Close()


def get_time():
    '''Get Current Date and Time'''

    label.config(text=time.strftime('%B %d %a %Y\n%I:%M:%S %p'))
    root.after(200, get_time)


def Clock():
    '''Display Clock'''

    global root, label

    root = Tk()
    root.config(bg='red')
    root.overrideredirect(True)
    root.wm_attributes("-topmost", 1, "-transparentcolor", 'red')
    root.geometry('240x45+{}+{}'.format(root.winfo_screenwidth() - 260, root.winfo_screenheight() - 90))

    frame = Frame(root)
    label = Label(frame, bg='red', fg="#fc0000", font=('Courier', 16, 'bold'))
    label.pack()
    frame.pack()

    get_time()
    root.mainloop()


if __name__ == '__main__':
    startup()
    Clock()
