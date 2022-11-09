import os
import sys
import json
import winreg
import ctypes
import calendar
import datetime
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from configparser import ConfigParser
from pystray._base import MenuItem as item
import pystray._win32
from PIL import Image
from dateutil.relativedelta import relativedelta


class _Entry:
    def __init__(self, frame, entry_style, default_text, width=30, trace=False):
        self.frame = frame
        self.trace = trace
        self.entry_style = entry_style

        self.IsDefault = True
        self.DEFAULT_TEXT = default_text

        self.var = StringVar()
        self.var.set(self.DEFAULT_TEXT)

        self.EntryStyle = ttk.Style()
        self.EntryStyle.configure(self.entry_style, foreground='grey')
        self.Entry = ttk.Entry(self.frame, width=width, textvariable=self.var, justify='center', style=self.entry_style)

        self.Entry.bind("<FocusIn>", self.focus_in)
        self.Entry.bind("<FocusOut>", self.focus_out)
        self.Entry.bind('<KeyPress>', self.KeyPressed)

    def focus_in(self, event=None):
        '''
        Remove temporary placeholder's text when
        user clicks to respective entry widget
        '''

        if self.IsDefault:
            self.var.set('')
            self.IsDefault = False
            self.EntryStyle.configure(self.entry_style, foreground='black')

    def focus_out(self, event=None):
        '''
        Remove temporary placeholder's text when
        user clicks out of respective entry widget
        '''

        if self.IsDefault is False and not self.var.get().strip():
            self.IsDefault = True
            self.var.set(self.DEFAULT_TEXT)
            self.EntryStyle.configure(self.entry_style, foreground='grey')

    def KeyPressed(self, event=None):
        '''
        Triggers when any key is pressed.

        It restricts user to enter other characters
        except numbers in fee Fee-Entry-Widget. It
        have no effects in Name-Entry-Widget.
        '''

        if self.trace:
            char = event.keysym

            if char.isdigit() is False and char not in ['BackSpace', 'Delete', 'Right', 'Left']:
                return 'break'

    def Reset(self):
        '''
        Set Entry values to default
        after clicking Submit button
        '''

        self.IsDefault = True
        self.var.set(self.DEFAULT_TEXT)
        self.EntryStyle.configure(self.entry_style, foreground='grey')


class Tuition:
    def __init__(self):
        self.tag = 0
        self.UpdateTimer = None
        self.WindowState = 'normal'
        self.IsAddedFirstTime = False

        self.configFile = os.path.join(os.environ['USERPROFILE'], r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Tuition\settings.ini')
        self.startupFile = os.path.join(os.path.dirname(sys.executable), 'Tuition-StartUp.exe')
        self.file_name = os.path.join(os.path.dirname(self.configFile), 'tuition.json')

        self.master = Tk()
        self.master.withdraw()
        self.master.title('TUITION')

        self.add_details_frame = Frame(self.master, bg='silver')

        self.entry_name = _Entry(self.add_details_frame, 'EntryName.TEntry', 'Name of Student', 50)
        self.entry_name.Entry.pack(ipady=4, pady=5)

        self.entry_fee = _Entry(self.add_details_frame, 'EntryFee.TEntry', 'Fee', 50, True)
        self.entry_fee.Entry.pack(ipady=4)

        self.months = list(calendar.month_abbr)[1:]
        self.date_frame = Frame(self.add_details_frame, bg='silver')
        self.month_combobox = ttk.Combobox(self.date_frame, values=self.months, width=8, height=12)
        self.month_combobox.pack(side=LEFT, padx=5)

        self.day_combobox = ttk.Combobox(self.date_frame, width=5, height=12)
        self.day_combobox.pack(side=LEFT, padx=5)

        self.SubmitButtonStyle = ttk.Style()
        self.SubmitButtonStyle.configure('Submit.TButton', background='silver')
        self.submit_button = ttk.Button(self.date_frame, text='Submit', cursor='hand2', style='Submit.TButton', command=self.submit_button_command)
        self.submit_button.pack(ipadx=10)

        self.date_frame.pack(pady=10)
        self.add_details_frame.pack(pady=10)

        self.TreeFrame = Frame(self.master, bg='silver')
        self.TreeFrame.pack(padx=3)

        self.Columns = ['NAME', 'FEE', 'JOINED', 'PREV DATE', 'NEXT PAY', 'LEFT', 'LATE PAY']
        self.Tree = ttk.Treeview(self.TreeFrame, show='headings', columns=self.Columns)
        self.Tree.pack(side=LEFT)

        self.Tree.heading('NAME', text='NAME')
        self.Tree.column('NAME')
        self.Tree.heading('FEE', text='FEE')
        self.Tree.column('FEE', width=80, anchor='center')
        self.Tree.heading('JOINED', text='JOINED')
        self.Tree.column('JOINED', width=130, anchor='center')
        self.Tree.heading('PREV DATE', text='PREV DATE')
        self.Tree.column('PREV DATE', width=130, anchor='center')
        self.Tree.heading('NEXT PAY', text='NEXT PAY')
        self.Tree.column('NEXT PAY', width=130, anchor='center')
        self.Tree.heading('LEFT', text='LEFT')
        self.Tree.column('LEFT', width=80, anchor='center')
        self.Tree.heading('LATE PAY', text='LATE PAY')
        self.Tree.column('LATE PAY', width=80, anchor='center')

        self.scrollbar = ttk.Scrollbar(self.TreeFrame, orient="vertical", command=self.Tree.yview)
        self.Tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill='y')

        self.master.after(0, self.center_window)
        self.master.config(bg='silver')

        self.Minimize()
        self.SetDefaultDates()

        self.Tree.bind('<Control-a>', self.SelectAll)
        self.Tree.bind('<Button-3>', self.RightClick)
        self.master.bind('<Button-1>', self.focus_anywhere)
        self.Tree.bind('<Motion>', self.RestrictResizingHeading)
        self.day_combobox.bind('<KeyPress>', self.ComboKeyPressed)
        self.master.protocol('WM_DELETE_WINDOW', self.withdraw_window)
        self.month_combobox.bind('<<ComboboxSelected>>', self.SetMonthRange)
        self.month_combobox.bind('<KeyPress>', lambda event=Event, _bool=True: self.ComboKeyPressed(event, _bool))

        self.master.mainloop()

    def ComboKeyPressed(self, event=None, _bool=False):
        '''
        When user types in Month Combobox then:
            i. Restricting user to input digit.
            ii. Restricting user to input more than three letters

        When user types in Day Combobox then:
            i. Restricting user to input letters
        '''

        char = event.keysym

        if char not in ['BackSpace', 'Delete', 'Left', 'Right']:
            if _bool is True:
                month_combo_get = self.month_combobox.get().strip() + event.char

                if len(month_combo_get) > 3:
                    return 'break'

            if char.isdigit() is _bool:
                return 'break'

    def center_window(self):
        '''
        Set position of the window to the center
        of the screen when user open the program
        '''

        self.master.update()

        self.master.resizable(0, 0)
        self.master.iconbitmap(resource_path('icon.ico'))
        width, height = self.master.winfo_width(), self.master.winfo_height() + 5
        screenwidth, screenheight = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{width}x{height}+{screenwidth - width // 2}+{screenheight - height // 2}')

        self.AddToStartUp()
        self.RanAtStartup = self.AlterConfigFile() == 'True'

        if self.RanAtStartup:
            self.withdraw_window()

        else:
            self.insert_at_first()
            self.master.deiconify()

        self.UpdateListBox()

    def focus_anywhere(self, event=None):
        '''
        Focus to the click widget. Also remove the
        selection(s) if made in ttk.Treeview
        '''

        widget = event.widget
        selections = self.Tree.selection()

        if self.ClickedAtEmptySpace(event) or isinstance(widget, ttk.Treeview) is False:
            if selections:
                self.Tree.selection_remove(selections)

        widget.focus()

    def ClickedAtEmptySpace(self, event=None):
        '''Check if user has clicked in empty space'''

        return self.Tree.identify('item', event.x, event.y) == ''

    def RestrictResizingHeading(self, event):
        '''Restrict user to resize the columns of Treeview '''

        if self.Tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def SelectAll(self, event=None):
        '''Select all values of ttk.Treeview when user presses control-A'''

        childrens = self.Tree.get_children()
        self.Tree.selection_add(childrens)

    def RightClick(self, event=None):
        '''When user right clicks inside list-box'''

        CurrentSelections = self.Tree.selection()
        RightClickMenu = Menu(self.master, tearoff=False)

        if CurrentSelections:
            RightClickMenu.add_command(label='Delete', command=self.delete_details)

        try:
            RightClickMenu.post(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def read_json(self):
        '''Reading data from the .json file.'''

        try:
            with open(self.file_name, 'r') as f:
                contents = json.load(f)

        except FileNotFoundError:
            with open(self.file_name, 'w'):
                contents = {}

        except json.decoder.JSONDecodeError:
            contents = {}

        return contents

    def write_json(self, contents):
        '''Storing data to the .json file'''

        with open(self.file_name, 'w') as f:
            json.dump(contents, f, indent=4)

    def get_next_payment_date(self, joined_str):
        '''
        Calculate next payment date when user adds data for
        the first time or when user gets monthly payment
        '''

        today = datetime.date.today()
        joined_obj = datetime.datetime.strptime(joined_str, '%Y-%b-%d')
        joined_obj = datetime.date(joined_obj.year, joined_obj.month, joined_obj.day)

        difference = relativedelta(today, joined_obj)
        diff_days = abs(today.day - joined_obj.day)

        if difference.months == 0:
            diff_days = difference.days

        elif joined_obj > today:
            today = joined_obj
            diff_days = 0

        next_payment = today - relativedelta(days=diff_days) + relativedelta(months=1)
        return next_payment.strftime('%Y-%b-%d')

    def delete_details(self):
        '''When user selects items in treeview and clicks delete menu'''

        is_error_shown = False
        contents = self.read_json()
        selections = self.Tree.selection()

        for selection in selections:
            value = self.Tree.item(selection)['values'][0]

            try:
                contents.pop(value)

            except KeyError:
                if is_error_shown is False:
                    is_error_shown = True
                    messagebox.showerror('ERR', f'Some values are not found in the file. Ignoring them.')

        self.write_json(contents)
        self.insert_at_first()

    def submit_button_command(self):
        '''When user clicks SUBMIT button '''

        fee = self.entry_fee.var.get().strip()
        name = self.entry_name.var.get().strip()
        day = self.day_combobox.get().strip()
        month = self.month_combobox.get().strip()

        if name in ['Name of Student', '']:
            messagebox.showerror('Invalid Name', 'Name of Student is invalid.')

        elif fee.isdigit() is False:
            messagebox.showerror('Invalid Fee', 'Fee is expected in numbers.')

        elif month not in self.months:
            messagebox.showerror('Invalid Month', 'Month is expected between Jan-Dec.')

        elif not day.isdigit() or int(day) > 32:
            messagebox.showerror('Invalid Day', 'Day is expected between 1-32.')

        else:
            joined_str = f'{datetime.date.today().year}-{month}-{str(day).zfill(2)}'
            next_pay = self.get_next_payment_date(joined_str)

            head = self.read_json()

            if name in head:
                messagebox.showerror('Exists', f'{name} is already in the file')

            else:
                tails = {name: {'fee': fee, 'joined': joined_str, 'prev_pay': [], 'late_pay': {}, 'next_pay': next_pay}}
                head.update(tails)

                self.write_json(head)
                self.IsAddedFirstTime = True

                self.entry_fee.Reset()
                self.entry_name.Reset()

                self.master.focus()
                self.insert_at_first()

    def insert_at_first(self):
        '''
        Inserts data from .json file to the TEXT widgets and also calculated
        the next payment date as well as the number of date left for the payment
        '''

        self.tag = 0

        contents = self.read_json()
        self.Tree.delete(*self.Tree.get_children())

        self.master.attributes('-topmost', True)

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

            else:
                prev_pay = 'Not Yet'

            if left <= 0:  # When its the day to get pay
                if self.IsAddedFirstTime:
                    late_pay = '0'

                else:
                    late_pay = (today - next_pay_obj).days

                if self.IsAddedFirstTime is False and messagebox.askyesno('Got Payment?', f'Did you get paid from {name}?'):
                    prev_pay = f'{today.year}-{calendar.month_abbr[today.month]}-{str(today.day).zfill(2)}'
                    contents[name]['prev_pay'].append(prev_pay)

                    next_pay = self.get_next_payment_date(joined)
                    next_pay_obj = datetime.datetime.strptime(next_pay, '%Y-%b-%d')
                    next_pay_obj = datetime.date(year=next_pay_obj.year, month=next_pay_obj.month, day=next_pay_obj.day)
                    left = (next_pay_obj - today).days

                    contents[name]['next_pay'] = next_pay
                    contents[name]['late_pay'][str(today)] = f'{late_pay} days'

                    late_pay = contents[name]['late_pay'][str(today)]

                else:
                    late_pay = f'{late_pay} days'

                if left < 0:  # When user does not get paid then it becomes late_pay where left becomes negative. So, in that case left becomes 0
                    left = '0'

            else:  # When its not the time to get pay
                if contents[name]['late_pay']:  # If there is last payment in the file
                    last_key = list(contents[name]['late_pay'].keys())[-1]
                    late_pay = contents[name]['late_pay'][last_key]

                else:  # If there is not last payment in the file
                    late_pay = '0 days'

            values = (name, fee, joined, prev_pay, next_pay, f'{left} days', late_pay)
            self.Tree.insert('', END, values=values, tag=self.tag)

            self.tag += 1

        self.master.focus()
        self.write_json(contents)

        self.master.attributes('-topmost', False)

    def SetDefaultDates(self):
        '''
        Set month and day combobox to current month
        and day when program loads for the first time
        '''

        today = datetime.datetime.today()
        self.month_combobox.set(today.strftime('%b'))
        self.day_combobox.set(today.strftime('%d'))

        self.SetMonthRange()

    def SetMonthRange(self, event=None):
        '''
        Set day range to respective month
        selected month name from month-combobox
        '''

        day_range = self.day_combobox.get().strip()
        month_name = self.month_combobox.get().strip().capitalize()

        today = datetime.date.today()

        if day_range.isdigit() is False:
            messagebox.showerror('ERR', 'Day must be number. Setting to DEFAULT value 1')
            return

        elif month_name not in self.months:
            messagebox.showerror('ERR', 'Invalid Month name. Setting to DEFAULT month JAN')
            return

        month_index = list(calendar.month_abbr).index(month_name)
        month_range = calendar.monthrange(today.year, month_index)[1]

        if int(day_range) > month_range:
            messagebox.showerror('ERR', 'Day range is beyond the actual range. Setting to DEFAULT value 1')

        else:
            self.day_combobox.config(values=list(range(1, month_range + 1)))

    def UpdateListBox(self):
        '''
        When the program keeps running and at 12:00 am the value of
        left days decreases by 1. So, updating this left days value.
        '''

        if self.master.state() == 'normal':
            children = self.Tree.get_children()

            for child in children:
                item = self.Tree.item(child)

                values = item['values']
                prev_left = int(values[-2].split()[0])

                today = datetime.date.today()
                next_pay = datetime.datetime.strptime(values[4], '%Y-%b-%d')
                next_pay_obj = datetime.date(year=next_pay.year, month=next_pay.month, day=next_pay.day)

                actual_left = (next_pay_obj - today).days

                if actual_left < 0:
                    actual_left = 0

                if prev_left != actual_left:
                    values[-2] = f'{actual_left} days'
                    self.Tree.item(child, values=values, tags=item['tags'][0])

        self.UpdateTimer = self.master.after(10, self.UpdateListBox)

    def quit_window(self):
        '''Quit window from the system tray'''

        self.icon.stop()
        self.master.quit()
        subprocess.call('taskkill /IM "{sys.executable}" /F', creationflags=0x08000000)

    def show_window(self):
        '''Restore window from the system tray'''

        self.icon.stop()

        self.master.after(250, self.insert_at_first)
        self.master.after(0, self.master.deiconify)
        self.master.after(250, self.UpdateListBox)

    def withdraw_window(self):
        '''Hide window to the system tray'''

        self.master.withdraw()
        self.master.after_cancel(self.UpdateTimer)

        image = Image.open(resource_path("icon.ico"))
        menu = (item('Quit', lambda: self.quit_window()), item('Show', lambda: self.show_window(), default=True))
        self.icon = pystray.Icon("name", image, "Tuition", menu)
        self.icon.run()

    def Minimize(self):
        '''Hide window to the system tray when user clicks the minimize button'''

        state = self.master.state()

        if (state, self.WindowState) == ('iconic', 'normal'):
            self.WindowState = 'iconic'
            self.withdraw_window()

        elif (state, self.WindowState) == ('normal', 'iconic'):
            self.WindowState = 'normal'

        self.master.after(250, self.Minimize)

    def AlterConfigFile(self):
        '''Read and Write the config file'''

        config = ConfigParser()
        config.read(self.configFile)

        dirpath = os.path.dirname(self.configFile)

        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        if 'STATUS' in config:
            status = config['STATUS']['Startup']

        else:
            status = False

        config['STATUS'] = {'Startup': False}
        config['PATH'] = {'EXE PATH': sys.executable}

        with open(self.configFile, 'w') as file:
            config.write(file)

        return status

    def AddToStartUp(self):
        '''Adding Tuition-Startup.exe to startup'''

        if os.path.exists(self.startupFile):
            if os.path.exists(self.startupFile):
                areg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)

                try:
                    akey = winreg.OpenKey(areg, f'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\Tuition-StartUp', 0, winreg.KEY_WRITE)
                    areg.Close()
                    akey.Close()

                except WindowsError:
                    key = winreg.OpenKey(areg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
                    winreg.SetValueEx(key, 'Tuition-StartUp', 0, winreg.REG_SZ, self.startupFile)

                    areg.Close()
                    key.Close()


def resource_path(file_name):
    '''
    Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
    '''

    try:
        base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

    except AttributeError:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    handle = ctypes.windll.user32.FindWindowW(None, "Tuition")

    if handle:  # When the program is already running
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.iconbitmap(resource_path('icon.ico'))
        res = messagebox.showinfo("ERR", "Already running ...")

        if res == 'ok':
            root.quit()
            root.destroy()

        root.mainloop()

    else:
        Tuition()
