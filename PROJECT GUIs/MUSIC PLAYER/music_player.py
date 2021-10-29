import os
import sys
import time
import json
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import pygame
from mutagen.mp3 import MP3
from ttkbootstrap import Style


'''To setup ttkbootstrap:
        1. Install ttkbootstrap using python -m pip install ttkbootstrap
        2. Create themes using python -m ttkcreator
        3. Specify your desired color and save the themes'''


class Music_Player:
    def __init__(self):
        pygame.mixer.init()

        self.AudioFiles = dict()
        self.extensions = [('Music Files', '*.mp3')]
        self.PlaylistPath = self.ResourcePath('playlists.json')
        self.AudioName = None  # Store currently playing song's name
        self.CurrentPlayingIndex = -1  # Index of current playing audio
        self.EOF = False  # Trigger to check if the last songs is about to play
        self.RemTimer = None  # Stores an alarm to call change_time function in every 500 ms
        self.PreviousVolume = None  # Store previous value of volumen before muting and unmuting
        self.ScaleTimer = None  # Stores an alarm to call update_scale function in every 1000 ms
        self.ShowRemTime = False  # Trigger to check if remaining time has showed in total time button
        self.PreviousScaleValue = 0  # Store previous position of AudioSlider to avoid dragging in same position
        self.isButtonInMotion = False  # Trigger to check if audio_slider is in motion. True for the audio_slider is being dragged
        self.isPlaying = None  # Trigger to check if the song is playing. None for has not started playing yet, True for playing and False for pause

        self.master = Tk()
        self.master.withdraw()
        self.master.iconbitmap(self.ResourcePath('icon.ico'))
        self.master.title('Music Player')

        self.PlayImage = PhotoImage(file=self.ResourcePath('Play.png'))
        self.StopAudioImage = PhotoImage(file=self.ResourcePath('Stop.png'))
        self.NextImage = PhotoImage(file=self.ResourcePath('Next.png'))
        self.MuteImage = PhotoImage(file=self.ResourcePath('Mute.png'))
        self.PauseImage = PhotoImage(file=self.ResourcePath('Pause.png'))
        self.UnmuteImage = PhotoImage(file=self.ResourcePath('Unmute.png'))
        self.PreviousImage = PhotoImage(file=self.ResourcePath('Previous.png'))

        self.Menu = Menu(self.master)
        self.FileMenu = Menu(self.Menu, tearoff=0)
        self.Menu.add_cascade(label='File', menu=self.FileMenu)
        self.master.config(menu=self.Menu)

        self.FileMenu.add_command(label='Open', accelerator='Ctrl + O', command=self.OpenFiles)
        self.FileMenu.add_command(label='Open Playlist', accelerator='Ctrl + P', command=self.GetPlaylist)
        self.FileMenu.add_command(label='Save Playlist', accelerator='Ctrl + Shift + P', command=self.SavePlaylist)
        self.FileMenu.add_command(label='Exit', accelerator='Ctrl + Q', command=self.master.destroy)

        self.AudioListBoxVar = Variable()
        self.AudioListBox = Listbox(self.master, listvariable=self.AudioListBoxVar, activestyle='none', height=10, width=100, bg='#f9f9fa', fg='purple', selectmode=MULTIPLE)
        self.AudioListBox.pack(fill='x')

        self.TotalTimeVar = StringVar()
        self.TotalTimeVar.set('--:--')
        self.EscapedTimeVar = StringVar()
        self.EscapedTimeVar.set('--:--')
        self.TimeFrame = Frame(self.master)
        self.EscapedTimeLabel = Label(self.TimeFrame, textvariable=self.EscapedTimeVar, bd=0, takefocus=False)
        self.EscapedTimeLabel.pack(side=LEFT)
        self.TotalTimeLabel = Label(self.TimeFrame, textvariable=self.TotalTimeVar, bd=0)
        self.TotalTimeLabel.pack(side=RIGHT)
        self.TimeFrame.pack(fill='x')

        self.style = Style()
        self.AudioSliderVar = IntVar()
        self.AudioSlider = ttk.Scale(self.master, from_=0, to=100, style='info.Horizontal.TScale', variable=self.AudioSliderVar)
        self.AudioSlider.pack(fill='x')

        self.VolumeSliderVar = IntVar()
        self.VolumeLabelVar = StringVar()
        self.VolumeLabelVar.set('100%')
        self.VolumeSliderVar.set(100)

        self.BottomFrame = Frame(self.master)
        self.BottomFrame.pack(side=BOTTOM, fill='x')
        self.ButtonsAttributes = {'bd': '0', 'bg': 'white', 'activebackground': 'white', 'takefocus': False}

        self.ButtonsFrame = Frame(self.BottomFrame)
        self.PlayButton = Button(self.ButtonsFrame, image=self.PlayImage, **self.ButtonsAttributes, command=self.PlayOrPauseAudio)
        self.PlayButton.pack(side=LEFT)
        self.PreviousButton = Button(self.ButtonsFrame, image=self.PreviousImage, **self.ButtonsAttributes, command=lambda: self.PreviousNextSong(button_name='prev'))
        self.PreviousButton.pack(side=LEFT, padx=2, ipady=5)
        self.StopAudioButton = Button(self.ButtonsFrame, image=self.StopAudioImage, **self.ButtonsAttributes, command=self.StopAudio)
        self.StopAudioButton.pack(side=LEFT)
        self.NextButton = Button(self.ButtonsFrame, image=self.NextImage, **self.ButtonsAttributes, command=self.PreviousNextSong)
        self.NextButton.pack(side=LEFT, padx=2)
        self.ButtonsFrame.pack(side=LEFT)

        self.VolumeFrame = Frame(self.BottomFrame)
        self.MuteUnmuteButton = Button(self.VolumeFrame, image=self.UnmuteImage, **self.ButtonsAttributes, command=self.MuteUnmuteVolume)
        self.MuteUnmuteButton.pack(side=LEFT)
        self.VolumeSlider = ttk.Scale(self.VolumeFrame, from_=0, to=100, variable=self.VolumeSliderVar, style='success.Horizontal.TScale', takefocus=False, command=self.ChangeVolume)
        self.VolumeSlider.pack(side=LEFT)
        self.VolumeLabel = Label(self.VolumeFrame, textvariable=self.VolumeLabelVar, width=4, font=font.Font(weight='bold'))
        self.VolumeLabel.pack(side=LEFT)
        self.VolumeFrame.pack(side=RIGHT)

        self.InitialPosition()

        self.master.bind('<s>', self.StopAudio)
        self.master.bind('<S>', self.StopAudio)
        self.master.bind('<space>', self.SpaceBind)
        self.master.bind('<Return>', self.ReturnBind)
        self.master.bind('<m>', self.MuteUnmuteVolume)
        self.master.bind('<M>', self.MuteUnmuteVolume)
        self.master.bind('<Up>', self.UpDownDirection)
        self.master.bind('<Control-o>', self.OpenFiles)
        self.master.bind('<Control-O>', self.OpenFiles)
        self.master.bind('<Down>', self.UpDownDirection)
        self.master.bind('<Control-p>', self.GetPlaylist)
        self.master.bind('<Delete>', self.RemoveFromList)
        self.master.bind('<Control-P>', self.SavePlaylist)
        self.AudioSlider.bind('<Button-3>', self.SkipAudio)
        self.AudioListBox.bind('<Button-3>', self.RightClick)
        self.AudioListBox.bind('<Button-1>', self.SingleClick)
        self.AudioSlider.bind('<B1-Motion>', self.ClickInMotion)
        self.AudioSlider.bind('<B3-Motion>', self.ClickInMotion)
        self.AudioListBox.bind('<Double-Button-1>', self.DoubleClick)
        self.TotalTimeLabel.bind('<Button-1>', self.ShowRemainingTime)
        self.master.bind('<Control-q>', lambda e: self.master.destroy())
        self.master.bind('<Control-Q>', lambda e: self.master.destroy())
        self.AudioSlider.bind('<ButtonRelease-1>', self.ClickInMotionReleased)
        self.AudioSlider.bind('<ButtonRelease-3>', self.ClickInMotionReleased)
        self.AudioListBox.bind('<Shift-Button-1>', self.shift_multiple_selection)
        self.master.bind('<n>', lambda event: self.PreviousNextSong(event, 'next'))
        self.master.bind('<N>', lambda event: self.PreviousNextSong(event, 'next'))
        self.master.bind('<p>', lambda event: self.PreviousNextSong(event, 'prev'))
        self.master.bind('<P>', lambda event: self.PreviousNextSong(event, 'prev'))
        self.AudioListBox.bind('<Control-Button-1>', self.MultipleSelectionOneByOne)
        self.master.bind('<Control-Right>', lambda event: self.SkipAudio(event, 'forward'))
        self.master.bind('<Control-Left>', lambda event: self.SkipAudio(event, 'backward'))
        self.master.bind('<Control-a>', lambda e: self.AudioListBox.selection_set(0, 'end'))
        self.master.bind('<Control-A>', lambda e: self.AudioListBox.selection_set(0, 'end'))
        self.master.bind('<Left>', lambda event, change='decrease': self.ChangeVolume(event, change))
        self.master.bind('<Right>', lambda event, change='increase': self.ChangeVolume(event, change))
        self.AudioListBox.bind('<Left>', lambda event, change='decrease': self.ChangeVolume(event, change))
        self.AudioListBox.bind('<Right>', lambda event, change='increase': self.ChangeVolume(event, change))
        self.AudioSlider.bind('<Button-1>', lambda event: self.SeekSingleClick(event, self.AudioSlider, self.SkipAudio))
        self.VolumeSlider.bind('<Button-1>', lambda event: self.SeekSingleClick(event, self.VolumeSlider, self.ChangeVolume, True))

        self.master.mainloop()

    def InitialPosition(self):
        '''Set window position to the center when program starts first time'''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width() // 2
        height = self.master.winfo_height() // 2
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.geometry(f'+{screen_width - width}+{screen_height - height}')
        self.master.deiconify()

    def ClickedAtEmptySpace(self, event=None):
        '''Check if user has clicked in empty space'''

        abs_coord_y = self.master.winfo_pointery() - self.master.winfo_rooty()

        lastIndex = len(self.AudioListBox.get(0, 'end')) - 1
        bbox = self.AudioListBox.bbox(lastIndex)

        if bbox:
            return abs_coord_y > bbox[1] + bbox[-1]

    def SeekSingleClick(self, event, widget, function, seek=False):
        '''Hijacking Single Left Click to work like Single Right Click
           to change the value of Scale to the position it is clicked

           Setting seek parameter to True activates audio_slider but
           not seek_scale when there is no audio in audio_list'''

        if self.PreviousVolume and seek:  # Unmuting sound when user clicks anywhere in volume slider
            self.MuteUnmuteVolume()

        if self.AudioListBoxVar.get() or seek:
            if event.y not in [0, 1, 2, 3, 4, 12, 13, 14, 15]:
                # I have noticed that we can click on some regions outside of ttk.Scale
                # making audio repeating at the same position. Those regions in event.y
                # are [0, 1, 2, 3, 4, 12, 13, 14, 15] where [0, 1, 2, 3, 4] are the top
                # regions of and [12 ,13, 14, 15] are the bottom regions of ttk.Scale.
                # When user clicks to these regions must be ignored.
                widget.event_generate('<Button-3>', x=event.x, y=event.y)
                function()

        return 'break'

    def ClickInMotion(self, event=None):
        '''When user holds left button and starts to drag left or right'''

        if self.isButtonInMotion is False:
            self.isButtonInMotion = True

    def ClickInMotionReleased(self, event=None):
        '''When user stops dragging left or right'''

        if self.isButtonInMotion:
            self.isButtonInMotion = False

            if self.PreviousScaleValue != self.AudioSliderVar.get():
                self.PreviousScaleValue = self.AudioSliderVar.get()
                self.SkipAudio()

    def SingleClick(self, event=None):
        '''When user single left clicks'''

        if not self.AudioFiles:
            # If there is no songs played yet but user left clicks
            # then make single left click event as double left click

            self.OpenFiles()
            return 'break'

        if self.ClickedAtEmptySpace():
            return 'break'

        if self.AudioListBox.itemcget(self.AudioListBox.nearest(event.y), 'bg') == 'grey':
            self.AudioListBox.select_clear(0, 'end')
            self.SelectIndex = self.AudioListBox.nearest(event.y)
            return 'break'

        self.AudioListBox.selection_clear(0, 'end')
        self.SelectIndex = self.AudioListBox.nearest(event.y)

    def DoubleClick(self, event=None):
        '''When user right clicks'''

        if self.ClickedAtEmptySpace():
            # When some files are opened and user double clicks
            # on the empty spaces then open file_dialog to open additional audio files
            self.OpenFiles()

        else:
            # Play the selected song when user double clicks on it
            self.isPlaying = None
            self.AudioListBox.selection_set(self.SelectIndex)

            if self.CurrentPlayingIndex > -1:
                self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='white', fg='purple')

            self.PlayOrPauseAudio()

    def OpenFiles(self, event=None, files=None):
        '''Open dialog box to select audio files'''

        if files is None:
            files = filedialog.askopenfilenames(filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

        if files:
            self.AudioFiles.update({os.path.basename(f): f for f in files})
            self.AudioListBoxVar.set(list(self.AudioFiles.keys()))

            if self.CurrentPlayingIndex == -1:
                self.SelectIndex = 0

            if self.isPlaying is None and not self.AudioListBox.curselection():
                self.AudioListBox.selection_set(0)

            if len(self.AudioFiles) == 1:  # Play audio if user opens only 1 audio file
                self.PlayOrPauseAudio()

        return 'break'

    def ReturnBind(self, event=None):
        '''When user press Enter key'''

        CurrentSelection = self.AudioListBox.curselection()

        if CurrentSelection:
            CurrentSelection = CurrentSelection[0]

            if self.AudioName != self.AudioListBox.get(CurrentSelection):
                self.isPlaying = None

                if self.CurrentPlayingIndex > -1:
                    self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='white', fg='purple')

        self.PlayOrPauseAudio()

    def SpaceBind(self, event=None):
        '''When user presses SPACE key'''

        CurrentIndex = self.AudioListBox.curselection()

        if CurrentIndex:
            CurrentIndex = CurrentIndex[0]

            if CurrentIndex != self.CurrentPlayingIndex:
                self.isPlaying = None
                self.CurrentPlayingIndex = CurrentIndex
                self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='white', fg='purple')

        self.PlayOrPauseAudio()

    def PlayOrPauseAudio(self, event=None):
        '''Play or pause audio when play or pause button is pressed'''

        try:
            if self.isPlaying is None:  # When any audio is not played before
                CurrentSelection = self.AudioListBox.curselection()

                if CurrentSelection:
                    CurrentSelection = CurrentSelection[0]

                else:
                    CurrentSelection = 0

                self.CurrentPlayingIndex = self.SelectIndex = CurrentSelection
                self.AudioListBox.selection_set(self.CurrentPlayingIndex)
                self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='grey', fg='white')
                self.AudioListBox.selection_clear(0, 'end')
                self.AudioName = self.AudioListBox.get(self.CurrentPlayingIndex)
                self.CurrentAudioPath = self.AudioFiles[self.AudioName]

                self.isPlaying = True  # Here, True represents that the music is being played.
                img = self.PauseImage
                pygame.mixer.music.load(self.CurrentAudioPath)  # Loading selected file for playing
                pygame.mixer.music.play()  # Start playing loaded file

                self.TotalTime = MP3(self.CurrentAudioPath).info.length  # Getting audio length
                self.AudioSlider.config(to=int(self.TotalTime))
                self.AudioSliderVar.set(0)
                self.AudioListBox.see(self.CurrentPlayingIndex)  # Scrolling to currently playing audio
                self.TotalTimeVar.set(time.strftime('%H:%M:%S', time.gmtime(self.TotalTime)))
                self.AudioListBox.selection_clear(0, 'end')

                if self.CurrentPlayingIndex != len(self.AudioFiles) - 1:
                    self.EOF = False  # Here, setting self.EOF to False means last song is not being played yet

                if self.ScaleTimer:
                    self.master.after_cancel(self.ScaleTimer)

                self.UpdateScale()

            elif self.isPlaying is True:  # Pausing audio when another audio is playing
                pygame.mixer.music.pause()
                img = self.PlayImage
                self.isPlaying = False
                self.master.after_cancel(self.ScaleTimer)

            elif self.isPlaying is False:  # Resume playing audio from where the audio is paused
                self.isPlaying = True
                img = self.PauseImage
                pygame.mixer.music.play(start=self.AudioSliderVar.get())
                self.UpdateScale()

            self.PlayButton.config(image=img)

        except pygame.error:
            self.isPlaying = None
            messagebox.showinfo('ERR', 'Audio format not supported')

        except TclError:  # when user tries to play audio when no audio was added before
            pass

    def StopAudio(self, event=None):
        '''Stop playing audio'''

        if self.isPlaying:
            pygame.mixer.music.stop()

            if self.ScaleTimer:
                self.master.after_cancel(self.ScaleTimer)

            self.AudioSliderVar.set(0)
            self.isPlaying = None
            self.AudioListBox.itemconfig(self.CurrentPlayingIndex, fg='purple', bg='white')
            self.CurrentPlayingIndex -= 1
            self.TotalTimeVar.set('--:--')
            self.EscapedTimeVar.set('--:--')
            self.AudioListBox.selection_clear(0, 'end')
            self.PlayButton.config(image=self.PlayImage)

    def UpdateScale(self, event=None):
        '''Continuously update escaping time and slider values
           until songs comes to end'''

        self.CurrentPos = pygame.mixer.music.get_pos() / 1000

        if self.AudioSliderVar.get() > int(self.CurrentPos):
            self.CurrentPos = self.AudioSliderVar.get() + 1

        self.EscapedTimeVar.set(time.strftime('%H:%M:%S', time.gmtime(self.CurrentPos)))
        self.AudioSliderVar.set(int(self.CurrentPos))

        if self.CurrentPlayingIndex == len(self.AudioFiles) - 1 and self.EOF is False:
            self.EOF = True

        if int(self.CurrentPos) == int(self.TotalTime):  # Checking if audio has complete playing
            self.master.after_cancel(self.ScaleTimer)
            self.isPlaying = None

            self.AudioSliderVar.set(0)
            self.TotalTimeVar.set('--:--')
            self.EscapedTimeVar.set('--:--')

            if self.EOF:
                self.EOF = False
                self.AudioListBox.see(0)
                self.ShowRemTime = False
                self.PlayButton.config(image=self.PlayImage)

                self.master.after_cancel(self.RemTimer)
                self.AudioListBox.selection_clear(0, 'end')
                self.AudioListBox.selection_set(0)

                self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='white', fg='purple')

            else:
                self.PreviousNextSong(button_name='next')

        else:
            self.ScaleTimer = self.master.after(1000, self.UpdateScale)

    def SkipAudio(self, event=None, direction=None):
        '''Skip song as the user moves the slider'''

        if self.isPlaying:
            SkipAt = self.AudioSliderVar.get()

            if direction == 'forward':
                SkipAt += 5

                if SkipAt >= self.TotalTime:
                    self.PreviousNextSong()
                    return

            elif direction == 'backward':
                SkipAt -= 5

                if SkipAt <= 0:
                    SkipAt = 0

            self.AudioSliderVar.set(SkipAt)

            if self.isPlaying:
                pygame.mixer.music.play(start=SkipAt)

            self.EscapedTimeVar.set(time.strftime('%H:%M:%S', time.gmtime(SkipAt)))

    def PreviousNextSong(self, event=None, button_name=None):
        '''Play previous and present audio present in list-box'''

        try:
            if self.CurrentPlayingIndex > -1:
                from_list_box = self.AudioListBoxVar.get()

                if button_name == 'prev':  # If previous buttons is clicked
                    if self.CurrentPlayingIndex == 0:
                        return

                    self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='white', fg='purple')
                    self.CurrentPlayingIndex -= 1

                else:  # If next button is clicked
                    if self.CurrentPlayingIndex == len(from_list_box) - 1:
                        return

                    self.AudioListBox.itemconfig(self.CurrentPlayingIndex, bg='white', fg='purple')
                    self.CurrentPlayingIndex += 1

                self.AudioListBox.selection_clear(0, 'end')
                self.AudioListBox.see(self.CurrentPlayingIndex)
                self.AudioListBox.selection_set(self.CurrentPlayingIndex)
                self.isPlaying = None
                self.PlayOrPauseAudio()

        except TclError:
            pass

    def GetPlaylist(self, event=None):
        '''Get audio path stored in a file'''

        try:
            with open(self.PlaylistPath, 'r') as f:
                contents = json.load(f)

                if not contents:
                    contents = {}

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            contents = {}
            messagebox.showerror('ERR', 'Either playlists file is corrupt or does not exist')

        if contents:
            files = list(contents['playlists'].values())

            for name, path in contents['playlists'].items():
                if not os.path.exists(path):
                    files.remove(path)

            self.OpenFiles(files=files)

    def SavePlaylist(self, event=None):
        '''Save audio path present in list-box'''

        if self.AudioListBoxVar.get():
            with open(self.PlaylistPath, 'w') as f:
                contents = {'playlists': self.AudioFiles}
                json.dump(contents, f, indent=4)
                messagebox.showinfo('Saved!', 'Playlist Saved !!')

        else:
            messagebox.showinfo('ERR', 'No audio found to save in Playlist')

    def ShowRemainingTime(self, event=None):
        '''Show remaining time of current playing audio'''

        if self.isPlaying and self.CurrentPlayingIndex > -1:
            if self.ShowRemTime is False:  # If remaining time has not been shown
                self.ShowRemTime = True
                self.ChangeTime()

            else:  # Remaining time has already been show
                self.ShowRemTime = False
                self.master.after_cancel(self.RemTimer)
                self.TotalTimeVar.set(time.strftime('%H:%M:%S', time.gmtime(self.TotalTime)))

    def ChangeTime(self):
        '''Calculate remaining time of currently playing song'''

        gmtime = time.gmtime(self.TotalTime - self.CurrentPos)
        self.TotalTimeVar.set(time.strftime('-%H:%M:%S', gmtime))
        self.RemTimer = self.master.after(500, self.ChangeTime)

    def MuteUnmuteVolume(self, event=None):
        '''Mute and Unmute volume'''

        if self.PreviousVolume is None:  # Volume is not muted before
            self.PreviousVolume = int(self.VolumeLabelVar.get()[:-1])
            self.MuteUnmuteButton.config(image=self.MuteImage)
            self.VolumeSlider.config(state='disabled')
            self.VolumeLabelVar.set('0%')
            pygame.mixer.music.set_volume(0)
            self.VolumeSliderVar.set(0)

        else:  # Volume is muted before
            self.VolumeSlider.config(state='normal')
            self.VolumeSliderVar.set(self.PreviousVolume)
            pygame.mixer.music.set_volume(self.PreviousVolume / 100)
            self.VolumeLabelVar.set(f'{self.PreviousVolume}%')
            self.MuteUnmuteButton.config(image=self.UnmuteImage)
            self.PreviousVolume = None

    def ChangeVolume(self, event=None, change=None):
        '''Increase or decrease volume when user drags volume bar or
           when user presses right arrow or left arrow
            Here volume value is between 0-1'''

        CurrentVolume = self.VolumeSliderVar.get()

        if change == 'increase':
            CurrentVolume += 5

            if CurrentVolume >= 100:
                CurrentVolume = 100

        elif change == 'decrease':
            CurrentVolume -= 5

            if CurrentVolume <= 0:
                CurrentVolume = 0

        if CurrentVolume == 0:
            self.PreviousVolume = None

        else:
            self.PreviousVolume = CurrentVolume

        self.MuteUnmuteVolume()
        self.VolumeSliderVar.set(CurrentVolume)
        CurrentVolume /= 100
        pygame.mixer.music.set_volume(CurrentVolume)
        self.VolumeLabelVar.set(f'{int(CurrentVolume * 100)}%')

        return 'break'

    def RightClick(self, event=None):
        '''When user right clicks inside list-box'''

        CurrentSelection = self.AudioListBox.curselection()
        RightClickMenu = Menu(self.master, tearoff=False)

        if len(CurrentSelection) >= 1:  # If multiple selection is done
            RightClickMenu.add_command(label='Remove from list', command=self.RemoveFromList)
            RightClickMenu.add_command(label='Remove from playlist', command=self.remove_from_playlist)

        else:
            if self.AudioListBoxVar.get():
                if self.ClickedAtEmptySpace():
                    self.AudioListBox.selection_clear(0, 'end')
                    RightClickMenu.add_command(label='Open', command=self.OpenFiles)

                else:  # When right click is clicked on the top of listbox's value before left click
                    self.AudioListBox.selection_clear(0, 'end')
                    self.AudioListBox.selection_set(self.AudioListBox.nearest(event.y))
                    self.AudioListBox.activate(self.AudioListBox.nearest(event.y))
                    RightClickMenu.add_command(label='Remove from list', command=self.RemoveFromList)
                    RightClickMenu.add_command(label='Remove from playlist', command=self.remove_from_playlist)

            else:  # When there is no audio files in AudioListBox
                RightClickMenu.add_command(label='Open', command=self.OpenFiles)
                RightClickMenu.add_command(label='Open Playlist', command=self.GetPlaylist)

        try:
            RightClickMenu.tk_popup(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def RemoveFromList(self, event=None):
        '''Remove selected item from the list-box'''

        CurrentIndexs = self.AudioListBox.curselection()

        if CurrentIndexs:
            for idx, CurrentIndex in enumerate(CurrentIndexs):
                CurrentIndex -= idx

                if CurrentIndex < 0:
                    CurrentIndex = 0

                if CurrentIndex == self.CurrentPlayingIndex:
                    self.StopAudio()

                song_name = self.AudioListBox.get(CurrentIndex)
                self.AudioFiles.pop(song_name)
                self.AudioListBox.delete(CurrentIndex)

            if len(self.AudioFiles) == 1:
                self.AudioListBox.selection_set(0)

            else:
                self.AudioListBox.selection_set(CurrentIndex)

    def remove_from_playlist(self, event=None):
        '''Remove selected item from the list-box as well from the playlist file'''

        self.RemoveFromList()
        self.SavePlaylist()

    def UpDownDirection(self, event=None):
        '''When user presses up or down arrow'''

        direc = event.keysym

        if self.AudioFiles:
            CurrentIndex = self.AudioListBox.curselection()

            if CurrentIndex:
                CurrentIndex = CurrentIndex[0]

            else:
                CurrentIndex = self.SelectIndex

            if direc == 'Up':
                if CurrentIndex != 0:
                    CurrentIndex -= 1

            else:
                if CurrentIndex < len(self.AudioFiles) - 1:
                    CurrentIndex += 1

            self.AudioListBox.see(CurrentIndex)
            self.AudioListBox.selection_clear(0, 'end')

            if self.AudioListBox.itemcget(CurrentIndex, 'bg') != 'grey':
                self.AudioListBox.selection_set(CurrentIndex)

    def MultipleSelectionOneByOne(self, event=None):
        '''Select multiple items in list-box holding control key'''

        self.SelectIndex = self.AudioListBox.nearest(event.y)

        if self.SelectIndex in self.AudioListBox.curselection():
            self.AudioListBox.selection_clear(self.SelectIndex)

        else:
            self.AudioListBox.selection_set(self.SelectIndex)
            self.AudioListBox.activate(self.SelectIndex)

    def shift_multiple_selection(self, event=None):
        '''Select multiple items in list-box holding shift key'''

        from_ = self.SelectIndex
        to_ = self.AudioListBox.nearest(event.y)

        if from_ > to_:
            from_, to_ = to_, from_

        if not self.AudioListBox.curselection():
            self.AudioListBox.selection_clear(0, 'end')

        for idx in range(from_, to_ + 1):
            self.AudioListBox.selection_set(idx)

    def ResourcePath(self, FileName):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'included_files', FileName)


if __name__ == '__main__':
    Music_Player()
