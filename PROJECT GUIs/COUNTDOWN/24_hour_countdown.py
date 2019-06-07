from tkinter import *

HOUR, MINUTE, SECOND, PAUSE = 24, 0, 6, False


def Counter():
    '''Updating hour, minute and seconds'''

    global HOUR, MINUTE, SECOND, PAUSE

    if PAUSE is False:
        if SECOND == 0:
            if MINUTE == SECOND == 0:
                HOUR -= 1
                MINUTE = 59

            else:
                MINUTE -= 1

            SECOND = 60

        SECOND -= 1

        if HOUR == MINUTE == SECOND == 0:
            PAUSE = True
            tim_e.config(text='Time up', font=('Courier', 40, 'bold'))

        else:
            tim_e.config(text='{}:{}:{}'.format(str(HOUR).zfill(2), str(MINUTE).zfill(2), str(SECOND).zfill(2)))

        root.after(1000, Counter)


root = Tk()
root.withdraw()
root.after(0, root.deiconify)
root.title('24 HOUR COUNTDOWN')
root.geometry(f'326x82+{root.winfo_screenwidth() // 2 - 326 // 2}+{root.winfo_screenheight() // 2 - 82 // 2}')
root.resizable(0, 0)
root.iconbitmap('icon.ico')
root.config(bg='dark blue')

tim_e = Label(root, font=('Courier', 50, 'bold'), bg='dark blue', fg='silver')
tim_e.pack(fill='both')

Counter()

root.mainloop()
