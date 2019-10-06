import time

try:  # Python 3
    from tkinter import Tk, Frame, Label

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import Tk, Frame, Label


def get_time():
    '''Get Current Date and Time'''

    label.config(text=time.strftime('%b %d %a %Y\n%I:%M:%S %p'))
    root.after(200, get_time)


root = Tk()
root.withdraw()
root.after(0, root.deiconify)
root.config(bg='red')
root.overrideredirect(True)
root.wm_attributes("-topmost", 1, "-transparentcolor", 'red')
root.geometry('240x45+{}+{}'.format(root.winfo_screenwidth() - 260, root.winfo_screenheight() - 90))

label = Label(root, bg='red', fg="#fc0000", font=('Courier', 16, 'bold'))
label.pack()

get_time()
root.mainloop()
