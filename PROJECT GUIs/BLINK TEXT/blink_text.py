try:  # Python 3
    from tkinter import *

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *


def blink():
    if text['fg'] == 'white':
        text['fg'] = 'red'

    else:
        text['fg'] = 'white'

    root.after(100, blink)


root = Tk()
root.withdraw()
root.after(0, root.deiconify)
root.iconbitmap('icon.ico')
root.title('Blinking Text')
root.resizable(0, 0)
root.geometry('298x36+{}+{}'.format(root.winfo_screenwidth() // 2 - 298 // 2, root.winfo_screenheight() // 2 - 36 // 2))
text = Label(root, text='BLINK', fg='white', bg='white', font=('Courier', 20))
text.pack()

blink()

root.config(bg='white')
root.mainloop()
