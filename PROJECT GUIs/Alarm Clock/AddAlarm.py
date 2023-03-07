from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import Include
import _photo_image as pi
from ListAlarm import ListAlarm
from CustomDaysWin import CustomDays
from SelectToneWin import SelectToneWin


last_grab_window = []


class AddAlarm:
    '''
    Show alarms adding widgets
    '''

    def __init__(self, window, text_widget):
        '''
        param:
            window: Tk window
            text_widget: Text object where all the alarms gets added
        '''

        self.window = window
        self.pi = pi.Image()
        self.text_widget = text_widget

    def SetInitialWindowPosition(self):
        '''
        Set window initial position when it starts
        '''

        self.AddAlarmWindow.update()
        self.AddAlarmWindow.resizable(0, 0)
        last_grab_window.append(self.AddAlarmWindow)
        self.AddAlarmWindow.iconphoto(False, self.pi.icon_image)

        root_x = self.window.winfo_rootx()
        root_y = self.window.winfo_rooty()

        w = self.AddAlarmWindow.winfo_width() // 8
        h = self.AddAlarmWindow.winfo_height() // 2

        self.AddAlarmWindow.geometry(f'+{root_x + w}+{root_y + h}')
        self.AddAlarmWindow.deiconify()

    def ShowWidgets(self):
        '''
        Showing Alarm Add Widgets
        '''

        self.AddAlarmWindow = Toplevel(self.window)
        self.AddAlarmWindow.transient(self.window)
        self.AddAlarmWindow.withdraw()
        self.AddAlarmWindow.grab_set()

        Include.UpdateTitle(self.AddAlarmWindow, 'Add Alarm')

        self.container = Frame(self.AddAlarmWindow)
        self.container.pack(padx=20, pady=10)

        self.Frame1 = Frame(self.container)
        self.Frame1.pack(fill='x')

        self.am_pm_values = [v.center(17) for v in ["AM", "PM"]]
        self.time_nums = [str(h).zfill(2).center(18) for h in range(60)]
        self.repeat_values = [v.center(18) for v in ['Once', 'Daily', 'Mon-Fri', 'Custom']]

        self.hour_combo_box = ttk.Combobox(self.Frame1, values=self.time_nums[1:13], width=11, justify='center')
        self.hour_combo_box.set('Hour')
        self.hour_combo_box.pack(side=LEFT, padx=(5, 0))

        self.minute_combo_box = ttk.Combobox(self.Frame1, values=self.time_nums, width=11, justify='center')
        self.minute_combo_box.set('Minute')
        self.minute_combo_box.pack(side=LEFT, padx=(5, 0))

        self.am_pm_combo_box = ttk.Combobox(self.Frame1, values=self.am_pm_values, width=10, justify='center')
        self.am_pm_combo_box.set('AM / PM')
        self.am_pm_combo_box.pack(side=LEFT, padx=(5, 0))

        self.Frame2 = Frame(self.container)
        self.Frame2.pack(fill='x', pady=10)

        self.SelectTone = SelectToneWin(self.window, last_grab_window)

        self.tone_label = Label(self.Frame2, text='RingTone')
        self.tone_label.pack(side=LEFT)
        self.tone_button = Button(self.Frame2, text='Select Ringtone', cursor='hand2', relief=GROOVE, command=self.SelectTone.ShowWidgets)
        self.tone_button.pack(side=RIGHT)

        self.Frame3 = Frame(self.container)
        self.Frame3.pack(fill='x')

        self.repeat_label = Label(self.Frame3, text='Repeat')
        self.repeat_label.pack(side=LEFT)
        self.repeat_combo_box = ttk.Combobox(self.Frame3, values=self.repeat_values, width=12, justify='center')
        self.repeat_combo_box.set('Once')
        self.repeat_combo_box.pack(side=RIGHT)

        self.Frame4 = Frame(self.container)
        self.Frame4.pack(fill='x', pady=10)

        self.delete_after_label = Label(self.Frame4, text='Delete After Goes Off')
        self.delete_after_label.pack(side=LEFT)
        self.delete_after_button = Button(self.Frame4, image=self.pi.off_image, bd=0, cursor='hand2', text='off', command=self.DeleteAfterCommand)
        self.delete_after_button.pack(side=RIGHT)

        self.Frame5 = Frame(self.container)
        self.Frame5.pack(fill='x')

        self.alarm_label = Label(self.Frame5, text='Alarm Label')
        self.alarm_label.pack(side=LEFT)
        self.alarm_label_entry = ttk.Entry(self.Frame5, width=15)
        self.alarm_label_entry.pack(side=RIGHT)

        self.Frame6 = Frame(self.container)
        self.Frame6.pack(pady=(30, 5))

        self.ListAlarm = ListAlarm(self.window, self.text_widget)
        self.CustomDays = CustomDays(self.window, self.repeat_combo_box, last_grab_window)

        self.cancel_button = Button(self.Frame6, image=self.pi.cancel_alarm_image, bd=0, cursor='hand2', command=self.Quit)
        self.cancel_button.pack(side=LEFT, padx=10)
        self.submit_button = Button(self.Frame6, image=self.pi.tick_image, bd=0, cursor='hand2', command=self.SubmitButtonCommand)
        self.submit_button.pack(side=LEFT)

        self.SetInitialWindowPosition()

        self.repeat_combo_box.bind('<<ComboboxSelected>>', self.ComboSelect)
        self.AddAlarmWindow.bind('<Button>', self.FocusWhereClicked)

        self.AddAlarmWindow.protocol("WM_DELETE_WINDOW", self.Quit)
        self.AddAlarmWindow.mainloop()

    def FocusWhereClicked(self, event):
        '''
        Focus to the clicked widget
        '''

        event.widget.focus()

    def ComboSelect(self, event):
        '''
        Check if user has clicked Custom option in Combo-box
        '''

        combo_get = self.repeat_combo_box.get().strip()

        if combo_get == 'Custom':
            self.CustomDays.ShowWidgets()

    def DeleteAfterCommand(self):
        '''
        Toggle on-off button when clicked
        '''

        if self.delete_after_button.cget('text') == 'off':
            self.delete_after_button.config(image=self.pi.on_image, text='on')

        else:
            self.delete_after_button.config(image=self.pi.off_image, text='off')

    def SubmitButtonCommand(self):
        '''
        When user clicks the tick button after entering alarm details
        '''

        hour = self.hour_combo_box.get().strip()
        minute = self.minute_combo_box.get().strip()
        am_pm = self.am_pm_combo_box.get().strip()

        if hour in ['Hour', '']:
            messagebox.showerror('ERR', 'SS hour value')
            last_grab_window[-1].grab_set()

        elif minute in ['Minute', '']:
            messagebox.showerror('ERR', 'Invalid minute value')
            last_grab_window[-1].grab_set()

        elif am_pm in ['AM / PM', '']:
            messagebox.showerror('ERR', 'Invalid am/pm value')
            last_grab_window[-1].grab_set()

        else:
            _time = f'{hour}:{minute} {am_pm}'
            tone = self.SelectTone.audio_name
            repeat = self.repeat_combo_box.get().strip()
            delete_after = self.delete_after_button.cget('text') == 'on'
            alarm_label = self.alarm_label_entry.get().strip()

            if not alarm_label:
                alarm_label = 'Alarm'

            if repeat == 'Daily':
                repeat = self.CustomDays.all_days_abbr

            elif repeat == 'Mon-Fri':
                repeat = self.CustomDays.all_days_abbr[1:-1]

            elif repeat == 'Custom':
                repeat = self.CustomDays.days

            new_data = {
                _time:
                {
                    'Status': True,
                    'AlarmTone': tone,
                    'Repeat': repeat,
                    'Delete After Goes Off': delete_after,
                    'Alarm Label': alarm_label
                }
            }

            new_contents = Include.ReadJSON()
            new_contents.update(new_data)

            Include.WriteToJson(new_contents)
            self.Quit()

    def Quit(self):
        '''
        When user clicks (x) button or when user exits the "Add Alarm" window
        by clicking X in title-bar
        '''

        self.AddAlarmWindow.destroy()

        if last_grab_window:
            last_grab_window.pop()


if __name__ == '__main__':
    AddAlarm()
