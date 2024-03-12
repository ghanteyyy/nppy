import os
import sys
import calendar
import datetime
import threading
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import pystray._win32
from PIL import Image, ImageTk
from pystray._base import MenuItem as item
from dateutil.relativedelta import relativedelta
from db import DB
from config import Config


class _Entry:
    def __init__(self, frame, default_text, width=30, trace=False):
        self.frame = frame
        self.trace = trace
        self.entry_style = f'{default_text}.TEntry'

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
        Remove default text when user clicks to respective entry widget
        '''

        if self.IsDefault:
            self.var.set('')
            self.IsDefault = False
            self.EntryStyle.configure(self.entry_style, foreground='black')

    def focus_out(self, event=None):
        '''
        Remove default text when user clicks out of respective entry widget
        '''

        if self.IsDefault is False and not self.var.get().strip():
            self.IsDefault = True
            self.var.set(self.DEFAULT_TEXT)
            self.EntryStyle.configure(self.entry_style, foreground='grey')

    def KeyPressed(self, event=None):
        '''
        Triggers when any key is pressed.

        It restricts user to enter other characters except numbers in fee
        Fee-Entry-Widget. It have no effects in Name-Entry-Widget.
        '''

        if self.trace:
            char = event.keysym

            if char.isdigit() is False and char not in ['BackSpace', 'Delete', 'Right', 'Left']:
                return 'break'

    def Reset(self):
        '''
        Set Entry values to default after clicking Submit button
        '''

        self.IsDefault = True
        self.var.set(self.DEFAULT_TEXT)
        self.EntryStyle.configure(self.entry_style, foreground='grey')


class Tuition:
    def __init__(self):
        self.CanvasWidth = 857
        self.UpdateTimer = None
        self.WindowState = 'normal'
        self.IsScrollBarShown = False
        self.CurrentObtainedDate = ''

        self.CONFIG = Config()
        self.CONFIG.ToggleValues("Is-Running", True)

        self.DatabasePath = self.CONFIG.contents.get('db_dir', None)
        self.RanAtStartup = self.CONFIG.contents.get('From-StartUp', False)

        self.master = Tk()
        self.master.withdraw()
        self.master.title('TUITION')

        self.CoverImage = Image.open(resource_path('cover.jpg'))
        self.CoverImage.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        self.CoverImage = ImageTk.PhotoImage(self.CoverImage)

        self.Canvas = Canvas(self.master, width=855, height=364, highlightthickness=0)
        self.Canvas.pack(fill=BOTH, expand=True)

        self.CoverTitle = self.Canvas.create_image(0, 0, image=self.CoverImage, anchor='nw')

        self.NameEntry = _Entry(self.master, 'Name of Student', 50)
        self.Canvas.create_window(self.CanvasWidth // 2, 30, window=self.NameEntry.Entry, anchor=CENTER, height=35)

        self.FeeEntry = _Entry(self.master, 'Fee', 50, True)
        self.Canvas.create_window(self.CanvasWidth // 2, 75, window=self.FeeEntry.Entry, anchor=CENTER, height=35)

        self.months = list(calendar.month_abbr)[1:]
        self.MonthComboBox = ttk.Combobox(self.master, values=self.months, width=8, height=12)
        self.Canvas.create_window(self.CanvasWidth // 2 - 70, 115, window=self.MonthComboBox, anchor=CENTER, height=25)

        self.DayComboBox = ttk.Combobox(self.master, width=5, height=12)
        self.Canvas.create_window(self.CanvasWidth // 2, 115, window=self.DayComboBox, anchor=CENTER, height=25)

        self.SubmitButtonStyle = ttk.Style()
        self.SubmitButtonStyle.configure('Submit.TButton')
        self.submit_button = ttk.Button(self.master, text='Submit', cursor='hand2', style='Submit.TButton', command=self.SubmitButtonCommand)
        self.Canvas.create_window(self.CanvasWidth // 2 + 70, 115, window=self.submit_button, anchor=CENTER, height=30)

        self.TreeViewFrame = Frame(self.master, bg='silver')
        self.Canvas.create_window(428, 252, window=self.TreeViewFrame, anchor=CENTER)

        self.Columns = ['NAME', 'FEE', 'JOINED', 'PREV DATE', 'NEXT PAY', 'LEFT', 'LATE PAY']
        self.TreeView = ttk.Treeview(self.TreeViewFrame, show='headings', columns=self.Columns)
        self.TreeView.pack(side=LEFT)

        self.TreeView.heading('NAME', text='NAME')
        self.TreeView.column('NAME')
        self.TreeView.heading('FEE', text='FEE')
        self.TreeView.column('FEE', width=80, anchor='center')
        self.TreeView.heading('JOINED', text='JOINED')
        self.TreeView.column('JOINED', width=130, anchor='center')
        self.TreeView.heading('PREV DATE', text='PREV DATE')
        self.TreeView.column('PREV DATE', width=130, anchor='center')
        self.TreeView.heading('NEXT PAY', text='NEXT PAY')
        self.TreeView.column('NEXT PAY', width=130, anchor='center')
        self.TreeView.heading('LEFT', text='LEFT')
        self.TreeView.column('LEFT', width=80, anchor='center')
        self.TreeView.heading('LATE PAY', text='LATE PAY')
        self.TreeView.column('LATE PAY', width=80, anchor='center')

        self.scrollbar = ttk.Scrollbar(self.TreeViewFrame, orient="vertical", command=self.TreeView.yview)
        self.TreeView.config(yscrollcommand=self.scrollbar.set)

        self.master.config(bg='silver')

        self.SetDefaultDates()

        self.TreeView.bind('<Control-a>', self.SelectAll)
        self.TreeView.bind('<Button-3>', self.RightClick)
        self.TreeView.bind('<Delete>', self.DeleteDetails)
        self.master.bind('<Button-1>', self.FocusAnyWhere)
        self.DayComboBox.bind('<KeyPress>', self.ComboKeyPressed)
        self.master.protocol('WM_DELETE_WINDOW', self.HideWindow)
        self.TreeView.bind('<Motion>', self.RestrictResizingHeading)
        self.TreeView.bind('<ButtonPress-1>', self.RestrictResizingHeading)
        self.MonthComboBox.bind('<<ComboboxSelected>>', self.SetMonthRange)
        self.MonthComboBox.bind('<KeyPress>', lambda event=Event, _bool=True: self.ComboKeyPressed(event, _bool))

        self.master.after(250, self.CenterWindow)
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
            if _bool:
                month_combo_get = self.MonthComboBox.get().strip() + event.char

                if len(month_combo_get) > 3:
                    return 'break'

            if char.isdigit() is _bool:
                return 'break'

    def CenterWindow(self, extra_height=5):
        '''
        Set position of the window to the center of the screen when user open
        the program
        '''

        self.master.update()

        self.master.resizable(0, 0)

        self.master.iconphoto(False, PhotoImage(file=resource_path('icon.png')))
        width, height = self.master.winfo_width(), self.master.winfo_height() + extra_height
        screenwidth, screenheight = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        self.master.geometry(f'{width}x{height}+{screenwidth - width // 2}+{screenheight - height // 2}')

        self.CONFIG.ToggleValues('From-StartUp', False)

        if self.RanAtStartup and CheckIfItIsExecutable():
            self.HideWindow()

        else:
            self.master.deiconify()

            if not self.CONFIG.contents.get('db_dir', None):
                messagebox.showinfo('Tuition-INFO', 'Unable to locate the database path. Please select a database path')

                while True:
                    directory = filedialog.askdirectory(initialdir=os.getcwd)

                    if os.path.exists(directory):
                        self.DatabasePath = os.path.join(directory, 'database.db')

                        self.CONFIG.contents.update({'db_dir': self.DatabasePath})
                        self.CONFIG.WriteContents(self.CONFIG.contents)

                        break

                    messagebox.showerror('Tuition-INFO', 'Selected directory does not exists. Please try again')

            self.InsertToTreeView()
            self.UpdateLeftDays()
            self.ShowHideScrollBar()
            self.Minimize()

    def FocusAnyWhere(self, event=None):
        '''
        Focus to the click widget. Also remove the selection(s) if made in
        ttk.Treeview
        '''

        widget = event.widget
        selections = self.TreeView.selection()

        if self.ClickedAtEmptySpace(event) or isinstance(widget, ttk.Treeview) is False:
            if selections:
                self.TreeView.selection_remove(selections)

        widget.focus_set()

    def ClickedAtEmptySpace(self, event=None):
        '''
        Check if user has clicked in empty space
        '''

        return self.TreeView.identify('item', event.x, event.y) == ''

    def RestrictResizingHeading(self, event):
        '''
        Restrict user to resize the columns of Treeview
        '''

        if self.TreeView.identify_region(event.x, event.y) == "separator":
            return "break"

    def ShowHideScrollBar(self):
        childrens = self.TreeView.get_children()
        TreeViewHeight = self.TreeView.cget('height') + 1

        if len(childrens) >= TreeViewHeight:
            if self.IsScrollBarShown is False:
                self.IsScrollBarShown = True
                self.scrollbar.pack(side=RIGHT, fill='y')

        else:
            if self.IsScrollBarShown:
                self.scrollbar.pack_forget()
                self.IsScrollBarShown = False

    def ResetToDefaults(self):
        '''
        Reset Entry and dates values
        '''

        self.FeeEntry.Reset()
        self.NameEntry.Reset()
        self.SetDefaultDates()

    def SelectAll(self, event=None):
        '''
        Select all values of ttk.Treeview when user presses Control-A
        '''

        childrens = self.TreeView.get_children()
        self.TreeView.selection_add(childrens)

    def RightClick(self, event=None):
        '''
        When user right clicks inside list-box
        '''

        CurrentSelections = self.TreeView.selection()
        RightClickMenu = Menu(self.master, tearoff=False)

        if CurrentSelections:
            RightClickMenu.add_command(label='Delete', command=self.DeleteDetails)

        try:
            RightClickMenu.post(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def GetNextPaymentDate(self, PrevNextPayStr):
        '''
        Calculate next payment date when user adds data for the first time or
        when user gets monthly payment
        '''

        PrevNextPayObj = datetime.datetime.strptime(PrevNextPayStr, '%Y-%b-%d').date()
        next_payment = PrevNextPayObj + relativedelta(months=1)

        return next_payment.strftime('%Y-%b-%d')

    def DeleteDetails(self, event=None):
        '''
        When user selects items in treeview and clicks delete menu
        '''

        selections = self.TreeView.selection()

        for selection in selections:
            item = self.TreeView.item(selection)
            tags = item['tags'][0]

            DB(self.DatabasePath).DeleteUser(tags)

        self.TreeView.delete(*selections)
        self.ShowHideScrollBar()

    def SubmitButtonCommand(self):
        '''
        When user clicks SUBMIT button
        '''

        fee = self.FeeEntry.var.get().strip()
        name = self.NameEntry.var.get().strip()
        day = self.DayComboBox.get().strip()
        month = self.MonthComboBox.get().strip()

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
            next_pay = self.GetNextPaymentDate(joined_str)

            details = (name, fee, joined_str, next_pay)
            DB(self.DatabasePath).AddNewStudent(details)

            self.InsertToTreeView(new_added=True)
            self.ShowHideScrollBar()
            self.ResetToDefaults()

    def InsertToTreeView(self, new_added=False):
        '''
        Inserts data from database file to the TEXT widgets and also calculated
        the next payment date as well as the number of date left for the payment
        '''

        contents = DB(self.DatabasePath).RetrieveData()
        self.TreeView.delete(*self.TreeView.get_children())

        self.master.attributes('-topmost', True)

        for id, values in contents.items():
            fee = values['Fee']
            name = values['Name']
            left = values['Left']
            joined = values['Joined']
            next_pay = values['NextPay']
            late_pay = values['LatePay']
            prev_pay = values['PrevDate']

            today = datetime.date.today()
            today_str = today.strftime('%Y-%b-%d')

            if left <= 0:  # When its the day to get pay
                if new_added is False and messagebox.askyesno('Got Payment?', f'Did you get paid from {name}?'):
                    prev_pay = today_str

                    DB(self.DatabasePath).UpdatePreviousPay(id, prev_pay)
                    DB(self.DatabasePath).UpdateLateDates(id, prev_pay, late_pay)

                    next_pay = self.GetNextPaymentDate(next_pay)
                    DB(self.DatabasePath).UpdateNextPay(id, next_pay)

                    next_pay_obj = datetime.datetime.strptime(next_pay, '%Y-%b-%d').date()
                    left = (next_pay_obj - today).days

            values = (name, fee, joined, prev_pay, next_pay, f'{left} days', f'{late_pay} days')
            self.TreeView.insert('', END, values=values, tag=id)

        self.master.focus()
        self.master.attributes('-topmost', False)

    def SetDefaultDates(self):
        '''
        Set month and day combobox to current month and day when program loads
        for the first time
        '''

        today = datetime.datetime.today()
        self.DayComboBox.set(today.strftime('%d'))
        self.MonthComboBox.set(today.strftime('%b'))

        self.SetMonthRange()

    def SetMonthRange(self, event=None):
        '''
        Set day range to respective month selected month name from month-combobox
        '''

        day_range = self.DayComboBox.get().strip()
        month_name = self.MonthComboBox.get().strip().capitalize()

        today = datetime.date.today()

        if day_range.isdigit() is False:
            messagebox.showerror('ERR', 'Day must be number. Setting to DEFAULT value 1')
            return

        elif month_name not in self.months:
            messagebox.showerror('ERR', 'Invalid Month name. Setting to DEFAULT month JAN')
            return

        month_index = self.months.index(month_name) + 1
        month_range = calendar.monthrange(today.year, month_index)[1]

        if int(day_range) > month_range:
            messagebox.showerror('ERR', 'Day range is beyond the actual range. Setting to DEFAULT value 1')

        else:
            self.DayComboBox.config(values=list(range(1, month_range + 1)))

    def UpdateLeftDays(self):
        '''
        When the program keeps running and at 12:00 am decreasing the value of
        left days by 1
        '''

        if self.master.state() == 'normal':
            children = self.TreeView.get_children()

            for child in children:
                item = self.TreeView.item(child)

                values = item['values']
                prev_left = int(values[-2].split()[0])

                left_days = DB(self.DatabasePath).GetLeftAndLateDays(values[4])[0]

                if left_days < 0:
                    left_days = 0

                if prev_left != left_days:
                    values[-2] = f'{left_days} days'
                    self.TreeView.item(child, values=values, tags=item['tags'][0])

        self.UpdateTimer = self.master.after(10, self.UpdateLeftDays)

    def QuitWindow(self):
        '''
        Quit window from the system tray
        '''

        self.CONFIG.SetDefaultValues()

        self.icon.stop()
        self.master.quit()

        subprocess.call(f'taskkill /IM "[{os.path.basename(sys.executable)}]" /F', creationflags=0x08000000)

    def ShowWindow(self):
        '''
        Restore window from the system tray
        '''

        self.CONFIG.ToggleValues('Is-Minimized', False)

        self.icon.stop()
        self.CenterWindow(extra_height=0)

    def HideWindow(self):
        '''
        Hide window to the system tray
        '''

        self.RanAtStartup = False   # To ensure that the window does not get hidden always
        self.CONFIG.ToggleValues('Is-Minimized', True)

        if self.master.state != 'normal':
            self.master.withdraw()

        if self.UpdateTimer is not None:
            self.master.after_cancel(self.UpdateTimer)

        image = Image.open(resource_path("icon.png"))
        menu = (item('Quit', lambda: self.QuitWindow()), item('Show', lambda: self.ShowWindow(), default=True))
        self.icon = pystray.Icon("name", image, "Tuition", menu)

        thread = threading.Thread(target=self.icon.run)
        thread.start()

    def Minimize(self):
        '''
        Hide window to the system tray when user clicks the minimize button
        '''

        current_date = str(datetime.date.today())

        if self.CurrentObtainedDate != current_date:
            self.SetDefaultDates()
            self.CurrentObtainedDate = current_date

        state = self.master.state()
        is_minimized = self.CONFIG.contents['Is-Minimized']

        if state == 'iconic' or is_minimized is True:
            self.WindowState = 'iconic'
            self.HideWindow()

        else:
            self.master.after(250, self.Minimize)


def CheckIfItIsExecutable():
    '''
    Return the directory path if it is running as executable
    '''

    try:
        return sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

    except AttributeError:
        return False


def resource_path(file_name):
    '''
    Get absolute path to resource from temporary directory

    In development:
        Gets path of files that are used in this script like icons, images or
        file of any extension from current directory

    After compiling to .exe with pyinstaller and using --add-data flag:
        Gets path of files that are used in this script like icons, images or
        file of any extension from temporary directory
    '''

    base_path = CheckIfItIsExecutable()

    if base_path is False:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    config = Config().contents

    if config.get('From-StartUp', False) is False:
        if os.path.exists('Tuition-StartUp.exe'):
            subprocess.run(['Tuition-StartUp.exe'])

    is_running = config.get('Is-Running', False)

    if is_running is False:
        Tuition()
