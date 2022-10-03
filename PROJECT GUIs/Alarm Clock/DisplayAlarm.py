import os
import time
import calendar
from tkinter import *
from tkinter import font
import pygame
import Include


class DisplayAlarm:
    '''
    Show alarm reminder window
    '''

    def __init__(self):
        self.IsAlarmShown = False

        pygame.mixer.init()
        self.AllDaysAbbr = list(calendar.day_abbr)
        self.AllDaysAbbr = [self.AllDaysAbbr[-1]] + self.AllDaysAbbr[:-1]

        self.bg = '#3425ba'
        self.is_alarm_shown = False
        self.already_shown_alarms = []

        self.DisplayAlarmWin = Tk()
        self.DisplayAlarmWin.withdraw()
        self.DisplayAlarmWin.config(bg=self.bg)
        self.DisplayAlarmWin.overrideredirect(True)
        self.DisplayAlarmWin.attributes('-topmost', True)

        self.TimeLabel = Label(self.DisplayAlarmWin, bg=self.bg, fg='white', font=font.Font(size=30))
        self.TimeLabel.pack(padx=10, pady=(20, 0))

        self.SnoozeButton = Button(self.DisplayAlarmWin, text='Snooze (5 min)', width=25, bg='#03804e', bd=0,
                                   activebackground='#03804e', fg='white', activeforeground='white',
                                   font=font.Font(size=12, weight='bold'), cursor='hand2')
        self.SnoozeButton.pack(pady=(20, 0), ipady=5, ipadx=5, padx=10)

        self.QuitButton = Button(self.DisplayAlarmWin, text='Quit', bg='#ff2f05', activebackground='#ff2f05',
                                 fg='white', bd=0, width=25, activeforeground='white', cursor='hand2',
                                 font=font.Font(size=12, weight='bold'))
        self.QuitButton.pack(pady=5, ipady=5, ipadx=5, padx=10)

        self.SetInitialWindowPosition()
        self.DisplayAlarmWin.mainloop()

    def SetInitialWindowPosition(self):
        '''
        Set window initial position when it starts
        '''

        self.DisplayAlarmWin.update()

        win_width = self.DisplayAlarmWin.winfo_width()
        screen_width = self.DisplayAlarmWin.winfo_screenwidth()

        x = screen_width - win_width
        self.DisplayAlarmWin.geometry(f'+{x}+{0}')

        self.main()

    def GetCurrentTime(self):
        return time.strftime('%I:%M %p')

    def GetAlarmTone(self, audio_name):
        return os.path.join(r'assets\Audio', audio_name)

    def Snooze(self, audio_path, original_time):
        '''
        Show the alarm remainder window again after 5 minutes

        param:
            audio_path     : audio-path of the respective alarm
            original_time  : time of the alarm that is about to snoozed
        '''

        self.Quit()
        self.DisplayAlarmWin.after(1000 * 60 * 5, lambda: self.ShowAlarm(audio_path, original_time, True))

    def ShowAlarm(self, audio_path, _time=None, snooze=False):
        '''
        Showing alarm window

        param:
            audio_path  : audio-path of the respective alarm
            _time       : time value of the alarm that is to be displayed
            snooze      : If true, indicates that the alarm that is about to
                          get displayed is the alarm that is snoozed
        '''

        if self.IsAlarmShown:
            # Removing currently showing alarm window (if any)
            self.Quit()

        if snooze:
            # When snooze time comes to end. Then, check if the status
            # of that snoozed original time is still True or the original
            # time still exists in the file

            contents = Include.ReadJSON()

            if _time in contents and contents[_time]['Status'] is False:
                return

            _time = None

        if _time is None:
            # Getting current time after 5 minutes to set alarm label' text
            _time = self.GetCurrentTime()

        self.IsAlarmShown = True
        self.TimeLabel.config(text=_time)

        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(loops=-1)

        self.DisplayAlarmWin.deiconify()

    def main(self):
        '''
        Entry point of the program
        '''

        self.RemoveShownTime()

        contents = Include.ReadJSON()
        current_time = self.GetCurrentTime()

        for key, values in contents.items():
            if contents[key]['Status'] and key == current_time:
                curr_day = time.strftime('%a')
                repeat = contents[key]['Repeat']

                if repeat != 'Once' and curr_day not in repeat:
                    # When the alarm is in repeating mode but the current
                    # day is not in the repeating-days then skipping that alarm
                    continue

                elif key not in self.already_shown_alarms:
                    if self.is_alarm_shown:  # When already previous alarm is being shown
                        self.Quit()

                    self.is_alarm_shown = True
                    self.already_shown_alarms.append(key)

                    self.TimeLabel.config(text=key)
                    audio_path = self.GetAlarmTone(values['AlarmTone'])

                    self.ShowAlarm(audio_path, key)

                    self.SnoozeButton.config(command=lambda: self.Snooze(audio_path, key))
                    self.QuitButton.config(command=lambda event=Event, _time=key: self.Quit(event, _time))

        self.DisplayAlarmWin.after(250, self.main)

    def RemoveShownTime(self):
        '''
        Clear already shown alarms
        '''

        contents = Include.ReadJSON()

        for alarm in self.already_shown_alarms:
            curr_time = self.GetCurrentTime()

            if curr_time != alarm:  # When the current time is ahead  of content_time

                repeat = contents[alarm]['Repeat'] == 'Once'
                delete_after = contents[alarm]['Delete After Goes Off']

                if self.IsAlarmShown is False:
                    if delete_after:
                        # Deleting alarms whose "delete after it goes off" is True
                        contents.pop(alarm)
                        Include.WriteToJson(contents)
                        self.already_shown_alarms.remove(alarm)  # Removing the shown alarm

                    elif repeat:
                        # When repeating mode is in Once then changing its status to False
                        # so that the same alarm won't shows again in future days
                        contents[alarm]['Status'] = False
                        Include.WriteToJson(contents)
                        self.already_shown_alarms.remove(alarm)  # Removing the shown alarm

    def Quit(self, event=None, _time=None):
        '''
        When user click Quit button
        '''

        self.IsAlarmShown = False

        pygame.mixer.music.stop()
        self.DisplayAlarmWin.withdraw()


if __name__ == '__main__':
    DisplayAlarm()
