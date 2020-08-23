import os
import sys
import json
import calendar
import datetime
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.ttk import Scrollbar


class Tution:
    def __init__(self):
        self.success = False
        self.file_name = 'tution.json'

        self.master = Tk()
        self.master.title('TUTION')

        self.add_details_frame = Frame(self.master, bg='silver')

        self.entry_name_var = StringVar()
        self.entry_name_style = ttk.Style()
        self.entry_name_style.configure('EntryName.TEntry', foreground='grey')
        self.entry_name = ttk.Entry(self.add_details_frame, width=50, justify=CENTER, style='EntryName.TEntry', textvariable=self.entry_name_var)
        self.entry_name.insert(END, 'Name of Student')
        self.entry_name.pack(ipady=4, pady=5)

        self.entry_fee_var = StringVar()
        self.entry_fee_style = ttk.Style()
        self.entry_fee_style.configure('EntryFee.TEntry', foreground='grey')
        self.entry_fee = ttk.Entry(self.add_details_frame, width=50, justify=CENTER, style='EntryFee.TEntry', textvariable=self.entry_fee_var)
        self.entry_fee.insert(END, 'Fee')
        self.entry_fee.pack(ipady=4)

        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.date_frame = Frame(self.add_details_frame, bg='silver')
        self.month_combobox = ttk.Combobox(self.date_frame, values=self.months, width=8, height=12)
        self.month_combobox.set('Month')
        self.month_combobox.pack(side=LEFT, padx=5)

        self.day_combobox = ttk.Combobox(self.date_frame, values=list(range(1, 33)), width=5, height=12)
        self.day_combobox.set('Day')
        self.day_combobox.pack(side=LEFT, padx=5)

        self.submit_button = ttk.Button(self.date_frame, text='Submit', cursor='hand2', command=self.submit_button_command)
        self.submit_button.pack(ipadx=10)

        self.style = ttk.Style()
        self.style.configure('EntryFee.TRadiobutton', background='silver', foreground='black')
        self.radio_var = IntVar()
        self.radio_buttonframe = Frame(self.add_details_frame, bg='silver')
        self.add_radiobutton = ttk.Radiobutton(self.radio_buttonframe, text='ADD', value=1, variable=self.radio_var, cursor='hand2', style='EntryFee.TRadiobutton')
        self.add_radiobutton.pack(side=LEFT)

        self.remove_radiobutton = ttk.Radiobutton(self.radio_buttonframe, text='REMOVE', value=2, variable=self.radio_var, cursor='hand2', style='EntryFee.TRadiobutton')
        self.remove_radiobutton.pack(side=LEFT)

        self.date_frame.pack(pady=10)
        self.radio_buttonframe.pack()
        self.add_details_frame.pack(pady=10)

        self.container_frame = Frame(self.master, bg='silver')
        self.student_name_frame = Frame(self.container_frame, bg='silver')
        self.fee_frame = Frame(self.container_frame, bg='silver')
        self.join_date_frame = Frame(self.container_frame, bg='silver')
        self.prev_pay_frame = Frame(self.container_frame, bg='silver')
        self.next_pay_frame = Frame(self.container_frame, bg='silver')
        self.left_frame = Frame(self.container_frame, bg='silver')
        self.late_pay_frame = Frame(self.container_frame, bg='silver')

        self.label_font = ('Courier', 12)

        self.student_name_label = Label(self.student_name_frame, text='NAME', bg='silver', font=self.label_font)
        self.student_name_label.pack()
        self.student_name_text = Text(self.student_name_frame, width=18, height=10, cursor='arrow')
        self.student_name_text.pack(pady=5)

        self.fee_label = Label(self.fee_frame, text='FEE', bg='silver', font=self.label_font)
        self.fee_label.pack()
        self.fee_text = Text(self.fee_frame, width=10, height=10)
        self.fee_text.pack(pady=5)

        self.join_date_label = Label(self.join_date_frame, text='Joined', bg='silver', font=self.label_font)
        self.join_date_label.pack()
        self.join_date_text = Text(self.join_date_frame, width=13, height=10)
        self.join_date_text.pack(pady=5)

        self.prev_pay_label = Label(self.prev_pay_frame, text='Prev Pay', bg='silver', font=self.label_font)
        self.prev_pay_label.pack()
        self.prev_pay_text = Text(self.prev_pay_frame, width=13, height=10)
        self.prev_pay_text.pack(pady=5)

        self.next_pay_label = Label(self.next_pay_frame, text='Next Pay', bg='silver', font=self.label_font)
        self.next_pay_label.pack()
        self.next_pay_text = Text(self.next_pay_frame, width=13, height=10)
        self.next_pay_text.pack(pady=5)

        self.left_label = Label(self.left_frame, text='LEFT', bg='silver', font=self.label_font)
        self.left_label.pack()
        self.left_text = Text(self.left_frame, width=13, height=10)
        self.left_text.pack(pady=5)

        self.late_pay_label = Label(self.late_pay_frame, text='LATE PAY', bg='silver', font=self.label_font)
        self.late_pay_label.pack()

        self.late_pay_text_frame = Frame(self.late_pay_frame)
        self.late_pay_text = Text(self.late_pay_text_frame, width=13, height=10)
        self.late_pay_text.pack(side=LEFT)

        # Adding scrollbar
        self.text_widgets = [self.student_name_text, self.fee_text, self.join_date_text, self.left_text]

        self.scrollbar = Scrollbar(self.late_pay_text_frame, orient="vertical", command=self.multiple_yview)
        self.scrollbar.pack(side=LEFT, fill='y')
        self.late_pay_text_frame.pack(pady=5)

        for widgets in self.text_widgets:  # Setting scrollbar for all text_widgets
            widgets.config(yscrollcommand=self.scrollbar.set)

        self.student_name_frame.pack(side=LEFT)
        self.fee_frame.pack(side=LEFT)
        self.join_date_frame.pack(side=LEFT)
        self.prev_pay_frame.pack(side=LEFT)
        self.next_pay_frame.pack(side=LEFT)
        self.left_frame.pack(side=LEFT)
        self.late_pay_frame.pack(side=LEFT)

        self.container_frame.pack(padx=3)

        self.master.bind('<Button-1>', self.widgets_bindings)
        self.entry_name.bind('<FocusIn>', self.widgets_bindings)
        self.entry_fee.bind('<FocusIn>', self.widgets_bindings)
        self.entry_fee.bind('<FocusOut>', lambda event, focus_out=True: self.widgets_bindings(event, focus_out))

        self.master.after(0, self.center_window)
        self.master.config(bg='silver')
        self.master.mainloop()

    def center_window(self):
        '''Set position of the window to the center of the screen when user open the program'''

        self.master.withdraw()
        self.master.update()

        self.master.resizable(0, 0)
        self.master.iconbitmap(self.resource_path('included_files\\icon.ico'))
        width, height = self.master.winfo_width(), self.master.winfo_height()
        screenwidth, screenheight = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{width}x{height}+{screenwidth - width // 2}+{screenheight - height // 2}')

        self.insert_at_first()
        self.master.deiconify()

    def widgets_bindings(self, event, focus_out=False):
        '''Remove or Add the default text when user clicks in or out of the entry widget'''

        name = self.entry_name_var.get().strip()
        fee = self.entry_fee_var.get().strip()

        if event.widget == self.entry_name or focus_out:
            if name == 'Name of Student' and not focus_out:
                self.entry_name_style.configure('EntryName.TEntry', foreground='black')
                self.entry_name_var.set('')

            if not fee:
                self.entry_fee_var.set('Fee')
                self.entry_fee_style.configure('EntryFee.TEntry', foreground='grey')

        elif event.widget == self.entry_fee:
            if fee == 'Fee':
                self.entry_fee_var.set('')
                self.entry_fee_style.configure('EntryFee.TEntry', foreground='black')

            if not name:
                self.entry_name_var.set('Name of Student')
                self.entry_name_style.configure('EntryName.TEntry', foreground='grey')

        elif event.widget not in [self.entry_name, self.entry_fee]:
            if not name:
                self.entry_name_var.set('Name of Student')
                self.entry_name_style.configure('EntryName.TEntry', foreground='grey')

            if not fee:
                self.entry_fee_var.set('Fee')
                self.entry_fee_style.configure('EntryFee.TEntry', foreground='grey')

            self.master.focus()

    def multiple_yview(self, *args):
        '''Creating commands of y-view for  all the TEXT widget'''

        for widgets in self.text_widgets:
            widgets.yview(*args)

    def read_json(self):
        '''Reading data from the .json file.'''

        try:
            with open(self.file_name, 'r') as f:
                contents = json.load(f)

                if not contents:
                    contents = {}

        except FileNotFoundError:
            with open(self.file_name, 'w'):
                contents = {}

        except json.decoder.JSONDecodeError:
            messagebox.showerror('JSON Error', 'You json file is either empty or corrupted so we could not load the data')
            contents = {}

        return contents

    def write_json(self, contents):
        '''Storing data to the .json file'''

        with open(self.file_name, 'w') as f:
            json.dump(contents, f, indent=4)

    def get_next_payment_date(self, joined_str, opt=False):
        '''Calculate next payment date when user adds data for the first time or when user gets monthly payment'''

        days = 0
        today = datetime.date.today().month
        joined_obj = datetime.datetime.strptime(joined_str, '%Y-%b-%d')
        difference = joined_obj - datetime.timedelta(days=joined_obj.day)
        _from = joined_obj.month

        if opt or _from == today:
            _to = today + 1

        else:
            _to = today

        if _from == 12:
            month_list = [12]

        else:
            month_list = list(range(_from, _to))

        for month in month_list:
            days += calendar.monthrange(joined_obj.year, month)[1]

        next_payment = difference + datetime.timedelta(days=days + joined_obj.day)

        return f'{next_payment.year}-{calendar.month_abbr[next_payment.month]}-{str(next_payment.day).zfill(2)}'

    def add_command(self, name, fee, month, day, var):
        '''When user selects REMOVE checkbutton and clicks SUBMIT button'''

        joined_str = f'{datetime.date.today().year}-{month}-{str(day).zfill(2)}'
        next_pay = self.get_next_payment_date(joined_str)

        head = self.read_json()

        if name in head:
            messagebox.showerror('Exists', f'{name} is already in the file')

        else:
            tails = {name: {'fee': fee, 'joined': joined_str, 'prev_pay': [], 'late_pay': {}, 'next_pay': next_pay}}

            head.update(tails)
            self.success = True

            return head

    def remove_command(self, name):
        '''When user selects ADD checkbutton and clicks SUBMIT button'''

        contents = self.read_json()

        try:
            contents.pop(name)
            self.success = True

            return contents

        except KeyError:
            messagebox.showerror('Invalid Value', f'{name.upper()} not found in the file')

    def submit_button_command(self):
        '''When user clicks SUBMIT button '''

        var = self.radio_var.get()
        fee = self.entry_fee_var.get().strip()
        name = self.entry_name_var.get().strip()
        day = self.day_combobox.get().strip()
        month = self.month_combobox.get().strip()

        if name in ['Name of Student', '']:
            messagebox.showerror('Invalid Name', 'Name of Student is invalid.')

        elif var not in [1, 2]:
            messagebox.showerror('Invalid button', 'You must select either ADD or REMOVE as per your intentions.')

        elif var == 2:
            contents = self.remove_command(name)

        elif not fee.isdigit():
            messagebox.showerror('Invalid Fee', 'Fee is expected in numbers.')

        elif month not in self.months:
            messagebox.showerror('Invalid Month', 'Month is expected between Jan-Dec.')

        elif not day.isdigit() or int(day) > 32:
            messagebox.showerror('Invalid Day', 'Day is expected between 1-32.')

        else:
            contents = self.add_command(name, fee, month, day, var)

        if self.success:
            self.success = False
            self.write_json(contents)

            self.reset()
            self.insert_at_first()

    def reset(self):
        '''Reset entries buttons and radiobutton to initial state'''

        self.entry_fee_style.configure('EntryFee.TEntry', foreground='silver')
        self.entry_name_style.configure('EntryName.TEntry', foreground='silver')

        for widget, text in {self.entry_name: 'Name of Student', self.entry_fee: 'Fee'}.items():
            widget.delete(0, END)
            widget.insert(END, text)

        self.day_combobox.set('Day')
        self.month_combobox.set('Month')

        self.radio_var.set(0)
        self.master.focus()

    def config_text_widget(self, state, clear=False):
        '''Enabling TEXT widgets to insert datas and Disabling them after all data has been inserted'''

        widgets = [self.fee_text, self.left_text, self.student_name_text, self.prev_pay_text, self.next_pay_text, self.join_date_text, self.late_pay_text]

        for widget in widgets:
            widget.config(state=state, cursor='arrow')

            if clear:
                widget.delete('1.0', END)

    def insert_at_first(self):
        '''Inserts data from .json file to the TEXT widgets and also calculated the next payment date as well as the number of date left for the payment'''

        contents = self.read_json()
        self.config_text_widget(state=NORMAL, clear=True)

        for key, value in contents.items():
            name = key
            fee = value['fee']
            joined = value['joined']
            prev_pay = value['prev_pay']
            next_pay = value['next_pay']

            today = datetime.date.today()
            next_pay_obj = datetime.datetime.strptime(next_pay, '%Y-%b-%d')
            next_pay_obj = datetime.date(year=next_pay_obj.year, month=next_pay_obj.month, day=next_pay_obj.day)

            left = (next_pay_obj - today).days

            if prev_pay:
                prev_pay = prev_pay[-1]
                prev_pay_obj = datetime.datetime.strptime(prev_pay, '%Y-%b-%d')
                prev_pay_obj = datetime.date(year=prev_pay_obj.year, month=prev_pay_obj.month, day=prev_pay_obj.day)

            else:
                prev_pay = 'Not Yet'
                joined_obj = datetime.datetime.strptime(joined, '%Y-%b-%d')
                prev_pay_obj = datetime.date(year=joined_obj.year, month=joined_obj.month, day=joined_obj.day)

            if left <= 0:  # When its the day to get pay
                if messagebox.askyesno('Got Payemnt?', f'Did you get paid from {name}?'):
                    late_pay = today.day - prev_pay_obj.day

                    prev_pay = f'{today.year}-{calendar.month_abbr[today.month]}-{str(today.day).zfill(2)}'
                    contents[name]['prev_pay'].append(prev_pay)

                    next_pay = self.get_next_payment_date(joined, opt=True)
                    next_pay_obj = datetime.datetime.strptime(next_pay, '%Y-%b-%d')
                    next_pay_obj = datetime.date(year=next_pay_obj.year, month=next_pay_obj.month, day=next_pay_obj.day)
                    left = (next_pay_obj - today).days

                    contents[name]['next_pay'] = next_pay
                    contents[name]['late_pay'][str(today)] = f'{late_pay} days'

                    late_pay = contents[name]['late_pay'][str(today)]

                else:  # If user don't get payment in exact next_pay date
                    late_pay = f'{today.day - next_pay_obj.day} days'

                if left < 0:
                    left = '0'

            else:  # When its not the time to get pay
                if contents[name]['late_pay']:  # If there is last payment in the file
                    last_key = list(contents[name]['late_pay'].keys())[-1]
                    late_pay = contents[name]['late_pay'][last_key]

                else:  # If there is not last payment in the file
                    late_pay = '0 days'

            for widget, text in {self.fee_text: fee, self.left_text: f'{left} days', self.join_date_text: joined, self.next_pay_text: next_pay, self.late_pay_text: late_pay, self.student_name_text: name, self.prev_pay_text: prev_pay}.items():
                widget.insert(END, f'{text}\n')

        self.master.focus()
        self.write_json(contents)
        self.config_text_widget(state=DISABLED)

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Tution()
