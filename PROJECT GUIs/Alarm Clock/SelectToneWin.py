import os
from tkinter import *
import tkinter.ttk as ttk
import pygame
import Include
import _photo_image as pi


class SelectToneWin:
    '''
    Show window to Select Alarm Tone
    '''

    def __init__(self, window, last_grab):
        '''
        param:
            window: Tk window
        '''

        pygame.mixer.init()

        self.window = window
        self.pi = pi.Image()
        self.last_grab = last_grab

    def SetInitialWindowPosition(self):
        '''
        Set window initial position when it starts
        '''

        self.ToneWin.update()
        self.ToneWin.resizable(0, 0)
        self.last_grab.append(self.ToneWin)
        self.ToneWin.iconphoto(False, self.pi.icon_image)

        root_x = self.window.winfo_rootx()
        root_y = self.window.winfo_rooty()

        w = int(self.ToneWin.winfo_width() // 9)
        h = int(self.ToneWin.winfo_height() // 2.5)

        self.ToneWin.geometry(f'+{root_x + w}+{root_y + h}')
        self.ToneWin.deiconify()

    def ShowWidgets(self):
        '''
        Showing Select Alarm Tone window
        '''

        self.audio_name = ''
        self.prev_index = None

        self.audio_path = 'assets\\Audio'
        self.all_audios = os.listdir(self.audio_path)

        self.ToneWin = Toplevel(self.window)
        self.ToneWin.grab_set()

        self.ToneWin.withdraw()
        Include.UpdateTitle(self.ToneWin, 'Select Audio')

        self.AudioVar = Variable(value=self.all_audios)

        self.AlarmListsFrame = Frame(self.ToneWin)
        self.AlarmListsFrame.pack()

        self.AlarmLists = Listbox(self.AlarmListsFrame, width=55, height=15, listvariable=self.AudioVar, activestyle='none')
        self.AlarmLists.pack(expand=True, fill=BOTH, side=LEFT)

        self.ScrollBar = ttk.Scrollbar(self.AlarmListsFrame, command=self.AlarmLists.yview)
        self.ScrollBar.pack(side=RIGHT, fill='y')
        self.AlarmLists.config(yscrollcommand=self.ScrollBar.set)

        self.AddButton = Button(self.ToneWin, text='Submit', bd=0, bg='green', fg='white', cursor='hand2',
                                activebackground='green', activeforeground='white', command=self.SubmitCommand)
        self.AddButton.pack(fill='x', ipady=5)

        self.SetInitialWindowPosition()
        self.ToneWin.protocol('WM_DELETE_WINDOW', self.Quit)
        self.AlarmLists.bind('<Double-Button-1>', self.DoubleClick)
        self.ToneWin.mainloop()

    def DoubleClick(self, event):
        '''
        Play or Pause audio when clicked to respective audio name in ListBox
        '''

        curr_sel = self.AlarmLists.curselection()

        if curr_sel:
            curr_sel = curr_sel[0]
            self.audio_name = self.AlarmLists.get(curr_sel)

            if self.prev_index == curr_sel:  # When current playing and user clicked audio are the same
                if pygame.mixer.music.get_busy():
                    # Pausing if currently playing
                    pygame.mixer.music.pause()

                else:
                    # Resuming if already paused
                    pygame.mixer.music.unpause()

            else:
                if self.prev_index is not None:
                    # Changing previous playing audio background and foreground color to default
                    self.AlarmLists.itemconfig(self.prev_index, bg='white', fg='black')

                # Changing current playing audio background color to black and foreground color to white
                self.AlarmLists.itemconfig(curr_sel, bg='black', fg='white')
                self.prev_index = curr_sel  # Changing the previous index to current clicked index

                path = os.path.join(self.audio_path, self.audio_name)  # Setting whole audio path with got audio name

                # Playing audio
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(loops=-1)

    def SubmitCommand(self):
        '''
        When user clicks Submit button in Select Alarm Tone window
        '''

        if not self.audio_name:
            # When user clicks submit the Select Alarm Tone window without
            # selecting any audio then setting the default alarm to Alarm.mp3
            self.audio_name = 'Alarm.mp3'

        self.Quit()

    def Quit(self):
        '''
        Set background and foreground color of selected value in Listbox to white
        and black respectively. Also stopping the currently playing audio.
        '''

        if self.prev_index:
            self.AlarmLists.itemconfig(self.prev_index, background='white', foreground='black')

        pygame.mixer.music.stop()
        self.ToneWin.destroy()

        self.last_grab.pop()
        self.last_grab[-1].grab_set()
