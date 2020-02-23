from tkinter import *


def blink():
    text.pack()

    if text['fg'] == 'white':
        text['fg'] = 'red'

    else:
        text['fg'] = 'white'

    root.after(100, blink)


root = Tk()
root.resizable(0, 0)
root.iconbitmap('included files/icon.ico')
root.title('Blinking Text')
root.geometry('298x36+{}+{}'.format(root.winfo_screenwidth() // 2 - 298 // 2, root.winfo_screenheight() // 2 - 36 // 2))
text = Label(root, text='BLINK', fg='white', bg='white', font=('Courier', 20, 'bold'))

blink()

root.config(bg='white')
root.mainloop()
