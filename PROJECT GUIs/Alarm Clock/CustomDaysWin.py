import calendar
from tkinter import *
import tkinter.ttk as ttk
import _photo_image as pi
import Include


class CustomDays:
    '''
    When user selects Custom option from the drop-down option in Combo-box
    '''

    def __init__(self, window, combo_box, last_grab):
        self.days = []
        self.pi = pi.Image()
        self.last_grab = last_grab

        self.window = window
        self.combo_box = combo_box

        # Getting full week days names
        self.all_days = calendar.day_name
        self.all_days = [self.all_days[-1]] + self.all_days[:-1]

        # Getting short week days names
        self.all_days_abbr = calendar.day_abbr
        self.all_days_abbr = [self.all_days_abbr[-1]] + self.all_days_abbr[:-1]

    def SetInitialWindowPosition(self):
        '''
        Set window initial position when it starts
        '''

        self.CustomDaysWin.update()
        self.CustomDaysWin.resizable(0, 0)
        self.CustomDaysWin.iconphoto(False, self.pi.icon_image)

        self.last_grab.append(self.CustomDaysWin)

        root_x = self.window.winfo_rootx()
        root_y = self.window.winfo_rooty()

        width = int(self.CustomDaysWin.winfo_width()  * 2.63)
        height = self.CustomDaysWin.winfo_height()

        w = int(width // 9)
        h = int(height // 2.12)

        self.CustomDaysWin.geometry(f'{width}x{height}+{root_x + w}+{root_y + h}')
        self.CustomDaysWin.deiconify()

    def ShowWidgets(self):
        '''
        Showing window to Select Custom Days
        '''

        self.CustomDaysWin = Toplevel(self.window)
        self.CustomDaysWin.grab_set()
        self.CustomDaysWin.withdraw()

        Include.UpdateTitle(self.CustomDaysWin, 'Custom Days')

        self.ComboFrame = Frame(self.CustomDaysWin, width=100)
        self.ComboFrame.pack()

        self.combo_vars = [IntVar() for i in range(7)]

        for idx, var in enumerate(self.combo_vars):  # Inserting check-button as per the each week day
            combo_box = ttk.Checkbutton(self.ComboFrame, text=self.all_days[idx], variable=var, cursor='hand2')

            if idx % 2 == 0:
                pady = 5

            else:
                pady = 0

            combo_box.pack(anchor='w', pady=pady, fill='x', padx=20)

        self.SubmitButton = Button(self.ComboFrame, text='Submit', bd=0, cursor='hand2', bg='green', fg='white',
                                   activebackground='green', activeforeground='white', command=self.SubmitCommand)
        self.SubmitButton.pack(fill='x', ipady=5, pady=(10, 20))

        self.SetInitialWindowPosition()
        self.CustomDaysWin.protocol('WM_DELETE_WINDOW', self.Quit)
        self.CustomDaysWin.mainloop()

    def SubmitCommand(self):
        '''
        When user clicks Submit Button then remembering the respective names
        '''

        vars_get = [var.get() for var in self.combo_vars]
        self.days = [self.all_days_abbr[idx] for idx, value in enumerate(vars_get) if value == 1]

        if self.days:
            self.CustomDaysWin.destroy()

        else:
            self.Quit()

    def Quit(self):
        '''
        When user closes the Custom Days window
        then setting the repeat days to 'Once'
        '''

        self.days = 'Once'
        self.combo_box.set(self.days)
        self.CustomDaysWin.destroy()

        self.last_grab.pop()
        self.last_grab[-1].grab_set()
