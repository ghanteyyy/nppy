import hashlib
import subprocess
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image
import pystray._win32
from pystray._base import MenuItem as item
import _photo_image as pi
from AddAlarm import AddAlarm
from ListAlarm import ListAlarm
import Include


class AlarmClock:
    def __init__(self):
        subprocess.Popen(['python', 'DisplayAlarm.py'])

        self.PrevHash = None
        self.WindowState = 'normal'

        self.window = Tk()
        self.pi = pi.Image()
        self.window_bg_color = self.window.cget('bg')

        self.window.withdraw()
        self.window.config(bg=self.window_bg_color)
        self.window.iconphoto(False, self.pi.icon_image)

        self.TextWidgetFrame = Frame(self.window)
        self.TextWidgetFrame.pack()

        self.TextWidget = Text(self.TextWidgetFrame, bd=0, width=50, height=30, cursor='arrow', bg=self.window_bg_color)
        self.TextWidget.pack(side=LEFT)

        self.TextWidgetScrollBar = ttk.Scrollbar(self.TextWidgetFrame, orient='vertical', command=self.TextWidget.yview)
        self.TextWidgetScrollBar.pack(side=RIGHT, fill='y')
        self.TextWidget.config(yscrollcommand=self.TextWidgetScrollBar.set)

        self.add_alarm = AddAlarm(self.window, self.TextWidget)

        self.AddAlarmButton = Button(self.window, image=self.pi.add_image, bd=0, cursor='hand2', bg=self.window_bg_color,
                                     activebackground=self.window_bg_color, command=self.add_alarm.ShowWidgets)
        self.AddAlarmButton.pack()

        self.ListAlarm = ListAlarm(self.window, self.TextWidget)

        Include.UpdateTitle(self.window, 'Alarm Clock')
        self.SetInitialWindowPosition()
        self.Minimize()

        self.window.bind('<MouseWheel>', self.MouseWheel)
        self.window.bind('<Tab>', self.RestrictDefaultBindings)
        self.window.protocol('WM_DELETE_WINDOW', self.withdraw_window)
        self.TextWidget.bind('<Button-1>', self.RestrictDefaultBindings)

        self.window.mainloop()

    def SetInitialWindowPosition(self):
        '''
        Set window initial position when it starts
        '''

        self.window.update()

        window_width, window_height = self.window.winfo_reqwidth() // 2, self.window.winfo_reqheight() //2
        screen_width, screen_height = self.window.winfo_screenwidth() // 2, self.window.winfo_screenheight() // 2

        x_pos = screen_width - window_width
        y_pos = screen_height - window_height

        self.window.geometry(f'+{x_pos}+{y_pos}')
        self.window.resizable(False, False)

        self.ListAlarm.ListWidgets()
        self.RedrawChangedWidgets()
        self.window.after(0, self.window.deiconify)

    def RestrictDefaultBindings(self, event):
        '''
        Restrict text-widget to insert cursor when user
        tries by clicking into it or by using TAB key
        '''

        return 'break'

    def MouseWheel(self, event):
        '''
        Make text-widget to scroll when user moves
        scroll button hovering to text-widget-windows
        '''

        self.TextWidget.yview_scroll(int(-1*(event.delta/120)), "units")

    def RedrawChangedWidgets(self):
        '''
        Redraw widgets in text-widget whenever the value
        in it changes. Changes are triggered when the
        alarms are deleted, paused or unpaused
        '''

        contents = Include.ReadJSON()
        all_alarms_from_text_widget = set()

        # Getting the hash of current contents in alarm.json file
        CurrHash = hashlib.md5(bytes(str(contents), encoding='utf-8')).digest()

        if self.PrevHash is None:
            # When self.PrevHash is None, it means that no
            # widgets has been inserted in text-widget

            self.PrevHash = CurrHash

        elif self.PrevHash != CurrHash:
            # When previous and current hash are not equal
            # then it means the changes has been made

            self.PrevHash = CurrHash

            for window in self.TextWidget.window_names():
                # text_widget.get_names() returns the widget as a string
                # so we have to convert that string to tkinter object
                frame = self.window.nametowidget(window)

                # Getting children widgets of that frame
                leftFrame, rightFrame = frame.winfo_children()

                # Extracting time from each window present in text-widget
                alarm_label = leftFrame.winfo_children()[1]['text']
                all_alarms_from_text_widget.add(alarm_label)

                if alarm_label in contents:  # If the time from each window is in alarm.json file exists
                    # Getting the status value from the file of the extracted time from the widget
                    content_status = contents[alarm_label]['Status']

                    # Selecting the toggle button from
                    # each window and getting its text
                    status_widget = rightFrame.winfo_children()[0]
                    widget_status = status_widget['text']

                    if content_status != widget_status:
                        # When the value of status inside file and in the label-widget of tex-widget
                        # are different then toggling its value from on to off or vice-versa.
                        if content_status:
                            text_status = 'on'
                            img = self.pi.on_image

                        else:
                            text_status = 'off'
                            img = self.pi.off_image

                        status_widget.config(text=text_status, image=img)
                        status_widget.image = img

                else:
                    # When the extracted time from the widget in text-widget is not in file then it
                    # implies that some alarms are deleted so, re-inserting all alarms present in the file
                    self.ListAlarm.ListWidgets(new=True)
                    break

            # Remove alarm present in text-widget from the json file. If there
            # exists any remaining alarm then inserting it one by one to text-widget
            all_alarms_from_file = set(contents.keys())
            difference = all_alarms_from_file - all_alarms_from_text_widget

            if difference:
                for diff in difference:
                    content = {
                        diff:
                            contents[diff]
                    }
                    self.ListAlarm.ListWidgets(content)

        self.window.after(250, self.RedrawChangedWidgets)

    def Minimize(self):
        '''
        Hide window to the system tray when user clicks the minimize button
        '''

        state = self.window.state()

        if (state, self.WindowState) == ('iconic', 'normal'):
            self.WindowState = 'iconic'
            self.withdraw_window()

        elif (state, self.WindowState) == ('normal', 'iconic'):
            self.WindowState = 'normal'

        self.window.after(250, self.Minimize)

    def withdraw_window(self):
        '''
        Hide window to the system tray
        '''

        self.window.withdraw()

        image = Image.open(Include.ResourcePath("icon.png"))
        menu = (item('Quit', lambda: self.Quit()), item('Show', lambda: self.show_window(), default=True))
        self.icon = pystray.Icon("name", image, "Alarm Clock", menu)

        self.icon.run()

    def show_window(self):
        '''
        Restore window from the system tray
        '''

        self.icon.stop()
        self.window.deiconify()

    def Quit(self):
        '''
        When user clicks Quit menu by right-clicking
        to the icon in system-try
        '''

        self.icon.stop()

        self.window.quit()
        self.window.destroy()


if __name__ == '__main__':
    AlarmClock()
