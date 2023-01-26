from tkinter import *
from tkinter.font import Font
import Include
import _photo_image as pi


class ListAlarm:
    '''
    Add alarm to the text-widget
    '''

    def __init__(self, window, text_widget):
        self.pi = pi.Image()
        self.window = window
        self.text_widget = text_widget
        self.error_msg = Label(self.text_widget, text='No alarms yet', fg='grey')

    def ListWidgets(self, contents=None, new=False):
        '''
        Insert alarm from the file to the text-widget

        param:
            contents: When None, it implies that all the alarms should be read from
                      the file. When not None, it implies that only new alarm is to
                      be displayed

                new:  Delete all existing widgets from the text-widget so that all
                      the alarms can be added from the file with modified details
                      if set True
        '''

        if new is True:
            self.text_widget.delete('1.0', END)

        if contents is None:
            contents = Include.ReadJSON()

        if contents:
            self.error_msg.place_forget()

        else:
            self.error_msg.place(relx=0.5, rely=0.5, anchor="c")

        for key, value in contents.items():
            self.text_widget.insert(END, '\n   ')

            frame = Frame(self.text_widget, highlightbackground="grey", highlightthickness=1, width=350, height=150)
            frame.propagate(0)

            left_frame = Frame(frame)
            left_frame.pack(side=LEFT, anchor='w', padx=10)

            alarm_label = Label(left_frame, text=value['Alarm Label'], font=Font(slant='italic'), wraplength=200)
            alarm_label.pack(anchor='w', padx=10)

            time_label = Label(left_frame, text=key, font=Font(size=20, weight='bold'))
            time_label.pack(anchor='w', pady=10, padx=10)

            repeat_values = value['Repeat']

            if isinstance(repeat_values, list):
                repeat_values = '  '.join(repeat_values)

            repeat_label = Label(left_frame, text=repeat_values)
            repeat_label.pack(anchor='w', padx=10, pady=(0, 10))

            right_frame = Frame(frame)
            right_frame.pack(side=RIGHT, padx=(30, 15), pady=(15, 0), fill='y')

            status = value['Status']

            if status:
                text = 'on'
                img = self.pi.on_image

            else:
                text = 'off'
                img = self.pi.off_image

            status_button = Button(right_frame, text=text, image=img, bd=0, cursor='hand2')
            status_button.pack(pady=20)

            delete_button = Button(right_frame, image=self.pi.del_image, bd=0, cursor='hand2', )
            delete_button.pack()

            self.text_widget.window_create(END, window=frame)
            self.text_widget.insert(END, '\n')

            self.window.update()
            status_button.bind('<Button-1>', lambda event=Event, action='pause': self.PauseRemoveAlarm(event, action))
            delete_button.bind('<Button-1>', lambda event=Event, action='delete': self.PauseRemoveAlarm(event, action))

    def GetCorrespondingTime(self, widget):
        '''
        Extract time value from the left-frame of the text-widget of the
        clicked button either toggle button or delete button

        param:
            widget: Clicked button-object from the displayed alarm in text-widget
        '''

        widget_parent = widget

        for _ in range(2):
            widget_parent = widget_parent.winfo_parent()
            widget_parent = self.window.nametowidget(widget_parent)

        left_frame = widget_parent.winfo_children()[0]
        left_frame = self.window.nametowidget(left_frame)

        left_frame_time_label = left_frame.winfo_children()[1]
        left_frame_time_label = self.window.nametowidget(left_frame_time_label)

        return left_frame_time_label.cget('text')

    def PauseRemoveAlarm(self, event, action):
        '''
        Pause the alarm when clicked to toggle button and remove the alarm when
        clicked to delete button

        param:
            event: Event object automatically generated when clicked to any buttons

            action: "pause" to pause or unpause the alarm when clicked to toggle
                    button "delete" to delete the alarm when clicked to delete button
        '''

        _time = self.GetCorrespondingTime(event.widget)

        contents = Include.ReadJSON()
        status = not contents[_time]['Status']

        if action == 'pause':
            contents[_time]['Status'] = status

        else:
            contents.pop(_time)

        Include.WriteToJson(contents)
