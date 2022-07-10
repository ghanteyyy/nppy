import os
import sys
import time
import datetime
import calendar
from tkinter import *


class Calendar:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.title('Calendar')
        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('icon.ico'))

        self.month_names = list(calendar.day_abbr)

        self.prev_button_img_obj = PhotoImage(file=self.resource_path('prev.png'))
        self.next_button_img_obj = PhotoImage(file=self.resource_path('next.png'))

        self.container_frame = Frame(self.master)
        self.container_frame.pack()

        self.label_text_var = StringVar()
        self.toggle_frame = Frame(self.master)
        self.prev_button = Label(self.toggle_frame, image=self.prev_button_img_obj)
        self.prev_button.grid(row=0, column=0)
        self.month_details = Label(self.toggle_frame, textvariable=self.label_text_var, width=20)
        self.month_details.grid(row=0, column=1)
        self.next_button = Label(self.toggle_frame, image=self.next_button_img_obj)
        self.next_button.grid(row=0, column=2)
        self.toggle_frame.pack(side=BOTTOM)

        self.make_calendar()
        self.prev_button.bind('<Button-1>', self.show_prev_month)
        self.next_button.bind('<Button-1>', self.show_next_month)
        self.prev_button.bind('<Enter>', lambda e: self.prev_button.config(cursor='hand2'))
        self.next_button.bind('<Enter>', lambda e: self.next_button.config(cursor='hand2'))
        self.master.after(10, lambda: self.initial_position())
        self.master.after(50, self.master.deiconify)

        self.master.mainloop()

    def initial_position(self):
        '''Position of the window when program opens for the first time'''

        self.master.update()

        win_width = 444
        win_height = 255
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.geometry(f'{win_width}x{win_height}+{screen_width - win_width // 2}+{screen_height - win_height}')

    def make_calendar(self, year=None, month=None):
        '''Display calendar'''

        if year:  # When the user has clicked next or previous button
            today_date = datetime.date(year=year, month=month, day=1)

            # Destroying previous dates
            # so that we can add new month dates
            # without overlapping with previous dates
            for children_widget in self.container_frame.winfo_children():
                children_widget.destroy()

        else:
            # When the program loads for the first time
            # Then showing the todays month calendar
            today_date = datetime.date.today()

        # Displaying days name
        for index, month_name in enumerate(self.month_names):
            month_frame = Frame(self.container_frame)
            month_frame.grid(row=0, column=index, padx=10)

            day_name_label = Label(month_frame, text=month_name, font=('Verdana', 15), fg='red' if month_name == 'Sun' else 'black')
            day_name_label.grid(row=0, column=0)

        self.year, self.month = today_date.year, today_date.month
        dates = calendar.monthcalendar(today_date.year, today_date.month)

        self.label_text_var.set(f"{today_date.strftime('%B')}, {today_date.year}")

        row = 1

        # Displaying dates with respective to days
        for date in dates:
            for index, d in enumerate(date):
                date_frame = Frame(self.container_frame)
                date_frame.grid(row=row, column=index, padx=10)
                date_label = Label(date_frame, font=('Verdana', 15))
                date_label.grid(row=0, column=0)

                # Setting border color of current date to blue
                if time.strftime('%m') == str(self.month).zfill(2) and time.strftime('%Y') == str(self.year) and time.strftime('%d') == str(d).zfill(2):
                    date_frame.config(highlightbackground="blue", highlightcolor="blue", highlightthickness=2, bd=0)

                # Setting the color of sunday to red because Sunday is holiday
                if index == 6:
                    date_label.config(fg='red')

                # Empty text when the dates is 0
                if d == 0:
                    date_label.config(text='')

                else:
                    date_label.config(text=d)

            row += 1

    def show_next_month(self, event=None):
        '''Display the calendar of next month when user click next button'''

        self.month += 1

        if self.month == 13:
            self.month = 1
            self.year += 1

        self.make_calendar(year=self.year, month=self.month)

    def show_prev_month(self, event=None):
        '''Display the calendar of previous month when user click previous button'''

        self.month -= 1

        if self.month == 0:
            self.month = 12
            self.year -= 1

        self.make_calendar(year=self.year, month=self.month)

    def resource_path(self, file_name):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    Calendar()
