import os
import time
import winsound

try:  # Python 3
    import tkinter.ttk as ttk
    from tkinter import Tk, Label, Button, IntVar

except (ImportError, ModuleNotFoundError):  # Python 2
    import ttk
    from Tkinter import Tk, Label, Button, IntVar


class Remainder_Window:
    def __init__(self):
        self.seen = {}
        self.birthdates = {}
        self.current_date = time.strftime('%m-%d')
        self.month_number = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    def get_birthdates(self, file, dic):
        '''Get birth dates from the file'''

        with open(file, 'r') as f:
            lines = f.readlines()

            for line in lines:
                split = line.strip('\n').split()

                if len(split) > 2:
                    name = f"{' '.join(split[:-1])}"

                else:
                    name = split[0]

                date = split[-1]

                if date == self.current_date:
                    dic.update({name: date})

    def Window(self, name, date):
        '''GUI window for showing of those whose birthday is today'''

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.resizable(0, 0)
        self.master.config(bg='red')
        self.master.overrideredirect(True)
        self.master.title('BIRTHDAY REMAINDER')
        self.master.wm_attributes('-topmost', 1)
        self.master.geometry(f'405x170+{self.master.winfo_screenwidth() - 406}+0')

        self.var = IntVar()
        self.style = ttk.Style()
        self.style.configure('Red.TCheckbutton', foreground='white', background='red')

        title = Label(self.master, text='REMAINDER', font=("Courier", 30), bg='red', fg='White')
        wishes = Label(self.master, text=f'Today is {name}\'s Birthday\n({date})', font=("Courier", 15), bg='red', fg='White', wraplength=450)
        check_button = ttk.Checkbutton(self.master, style='Red.TCheckbutton', text='Don\'t show again', variable=self.var)
        close_button = Button(self.master, text='CLOSE', font=("Courier", 12), bg='red', activeforeground='white', activebackground='red', fg='White', width=10, relief='ridge', command=lambda: self.quit_button(name, date))

        title.pack()
        wishes.pack()
        check_button.pack(side='bottom')
        close_button.pack(side='bottom')

        self.master.mainloop()

    def mark_as_seen(self, name, date):
        '''Store name and date if user selects "Don't show again"'''

        with open('mark_as_seen.txt', 'a') as file:
            file.write(f'{name} {date}\n')

    def quit_button(self, name, date):
        '''When user click the quit button'''

        if self.var.get() == 1:
            self.mark_as_seen(name, date)

        self.master.destroy()

    def already_seen(self, name, date):
        '''Check user has already seen the remainder'''

        if os.path.exists('mark_as_seen.txt'):
            self.get_birthdates('mark_as_seen.txt', self.seen)

        if name in self.seen and self.seen[name] == date:
            return True

        return False

    def destroy_seen(self):
        '''Removing "mark_as_seen.txt" at the next day of the birthday so that it can display at the next birthday'''

        if os.path.exists('mark_as_seen.txt'):
            modified_time = time.ctime(os.path.getmtime('mark_as_seen.txt')).split()
            real_time = f'{self.month_number[modified_time[1]]}-{modified_time[2]}'

            if self.current_date != real_time:
                os.remove('mark_as_seen.txt')

    def main(self):
        '''Main function of the entire script'''

        self.destroy_seen()
        self.get_birthdates('Birthday Remainder.txt', self.birthdates)

        for name, date in self.birthdates.items():
            if not self.already_seen(name, date):
                winsound.PlaySound('included files/tone.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
                self.Window(name, date)


if __name__ == '__main__':
    if os.path.exists('Birthday Remainder.txt'):
        Remainder_Window().main()
