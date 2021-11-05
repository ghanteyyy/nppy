import time
from tkinter import *


class DigitalClock:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.config(bg='red')
        self.master.overrideredirect(True)
        self.master.wm_attributes("-topmost", 1, "-transparentcolor", 'red')

        self.width, self.height = 240, 45
        self.screenwidth, self.screenheight = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry(f'{self.width}x{self.height}+{self.screenwidth - 260}+{self.screenheight - 90}')

        self.label = Label(self.master, bg='red', fg="#fc0000", font=('Courier', 16, 'bold'))
        self.label.pack()

        self.get_time()
        self.master.mainloop()

    def get_time(self):
        '''Get current date and time'''

        self.label.config(text=time.strftime('%d %b %a %Y\n%I:%M:%S %p'))
        self.master.after(200, self.get_time)


if __name__ == '__main__':
    DigitalClock()
