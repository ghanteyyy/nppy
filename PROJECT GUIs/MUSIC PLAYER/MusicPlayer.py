import os
import re
import io
import sys
import time
import json
import bisect
import random
import datetime
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter import font, filedialog, messagebox
import pygame
import stagger
import customtkinter
from ttkbootstrap import Style
from PIL import Image, ImageTk
from mutagen.mp3 import MP3, HeaderNotFoundError


'''
To setup ttkbootstrap:
    1. Install ttkbootstrap using python -m pip install ttkbootstrap
    2. Create themes using python -m ttkcreator
    3. Specify your desired color and save the themes
    4. If you want to use my theme then copy user.py file to
            <python-installed-directory>\Lib\site-packages\ttkbootstrap\themes
'''


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.PrevID = ''
        self.TrackLine = 0
        self.RotateImageAngle = 10
        self.PrevSearchChar = None  # Store previous search string
        self.RepeatAudio = None  # Track the state of Repeat Button
        self.IsMuted = False  # Track if audio has been muted or not
        self.AudioName = None  # Store currently playing song's name
        self.IsLyricsAdded = None  # Tracks if user has added lyrics
        self.WindowNotMapped = False  # Track if window is minimized
        self.IsFindWidgetShown = False  # Track if FindWidget is shown
        self.SearchGlobalIndex = None  # Track the index of Search Value
        self.TotalAudioDuration = 0  # Store total time of inserted audio
        self.CurrentPlayingIndex = None  # Index of current playing audio
        self.IsAlbumPictureShown = False  # Track if album picture is shown
        self.childrens = []  # Stores children belonging to item of TreeView
        self.RotateImageTimer = None  # Store after timer label to rotate image
        self.EOF = False  # Trigger to check if the last songs is about to play
        self.SearchLocalIndex = None   # Track the search index of filtered items
        self.PlayRandom = False  # Track if Random Button has been pressed or not
        self.extensions = [('Music Files', '*.mp3')]  # Extensions for audio files
        self.AudioFiles = dict()  # Stores audio path that is currently opened by user
        self.IsDefaultImage = None  # Tracks if the current playing audio has album art
        self.RemTimer = None  # Stores an alarm to call change_time function in every 500 ms
        self.PreviousVolume = 100  # Store previous value of volume before muting and un-muting
        self.ScaleTimer = None  # Stores an alarm to call update_scale function in every 1000 ms
        self.ShowRemTime = False  # Trigger to check if remaining time has showed in total time button
        self.PlaylistPath = self.ResourcePath('playlists.json')  # File where list of audios are saved
        self.TagCount = 0  # Increase by 1 each time when user adds new audio for unique tags in TreeView
        self.PreviousScaleValue = 0  # Store previous position of AudioSlider to avoid dragging in same position
        self.isPlaying = None  # Trigger to check if the song is playing. None for has not started playing yet, True for playing and False for pause

        if sys.platform == 'win32':
            self.ErrorFile = self.ResourcePath('WinErrSound.wav')

        else:
            self.ErrorFile = self.ResourcePath('LinuxErrSound.wav')

        self.PlayError = pygame.mixer.Sound(self.ErrorFile)

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Music Player')
        self.master.iconbitmap(self.ResourcePath('icon.ico'))
        self.ButtonsAttributes = {'bd': '0', 'bg': 'white', 'activebackground': 'white', 'takefocus': False}

        self.AlbumArtImage = self.ResourcePath('albumart.png')
        self.ArtImage = PhotoImage(file=self.ResourcePath('art.png'))
        self.InfoImage = PhotoImage(file=self.ResourcePath('info.png'))
        self.PlayImage = PhotoImage(file=self.ResourcePath('Play.png'))
        self.NextImage = PhotoImage(file=self.ResourcePath('Next.png'))
        self.LrcImage = PhotoImage(file=self.ResourcePath('Lyrics.png'))
        self.UnmuteImage = PhotoImage(file=self.ResourcePath('Vol4.png'))
        self.PauseImage = PhotoImage(file=self.ResourcePath('Pause.png'))
        self.VolumeImage1 = PhotoImage(file=self.ResourcePath('Vol1.png'))
        self.VolumeImage2 = PhotoImage(file=self.ResourcePath('Vol2.png'))
        self.VolumeImage3 = PhotoImage(file=self.ResourcePath('Vol3.png'))
        self.VolumeImage4 = PhotoImage(file=self.ResourcePath('Vol4.png'))
        self.NoVolumeImage = PhotoImage(file=self.ResourcePath('Vol0.png'))
        self.SearchImage = PhotoImage(file=self.ResourcePath('Search.png'))
        self.StopAudioImage = PhotoImage(file=self.ResourcePath('Stop.png'))
        self.PreviousImage = PhotoImage(file=self.ResourcePath('Previous.png'))
        self.RepeatAllImage = PhotoImage(file=self.ResourcePath('RepeatAll.png'))
        self.SearchExitImage = PhotoImage(file=self.ResourcePath('SearchExit.png'))
        self.RandomActiveImage = PhotoImage(file=self.ResourcePath('RandomActive.png'))
        self.RepeatCurrentImage = PhotoImage(file=self.ResourcePath('RepeatCurrent.png'))
        self.RandomDisabledImage = PhotoImage(file=self.ResourcePath('RandomDisabled.png'))

        self.container = Frame(self.master)
        self.container.pack()

        self.Menu = Menu(self.container)
        self.FileMenu = Menu(self.Menu, tearoff=0)
        self.Menu.add_cascade(label='File', menu=self.FileMenu)
        self.master.config(menu=self.Menu)

        self.EmptySpace = ' ' * 10
        self.FileMenu.add_command(label='Open', accelerator=f'{self.EmptySpace}Ctrl + O' , command=self.OpenFiles)
        self.FileMenu.add_command(label='Open Playlist', accelerator=f'{self.EmptySpace}Ctrl + Shift + O', command=self.GetPlaylist)
        self.FileMenu.add_command(label='Find ...', accelerator=f'{self.EmptySpace}Ctrl + F' , command=self.ShowFindWidget)
        self.FileMenu.add_command(label='Save Playlist', accelerator=f'{self.EmptySpace}Ctrl + S', command=lambda: self.SavePlaylist(Event, True))
        self.FileMenu.add_command(label='Exit', accelerator=f'{self.EmptySpace}Ctrl + Q', command=self.master.destroy)

        self.AudioListFrame = Frame(self.container, width=621, height=239)
        self.AudioListFrame.pack()

        self.Columns = ['Title', 'Duration']

        self.style = Style('newtheme')
        self.TreeFrame = Frame(self.AudioListFrame)
        self.Tree = ttk.Treeview(self.TreeFrame, columns=self.Columns, show='headings', style='secondary.Treeview')
        self.Tree.pack(side=LEFT, fill=BOTH)
        self.TreeFrame.pack()

        # Attaching scrollbar to TreeView
        self.scrollbar = Scrollbar(self.TreeFrame, orient="vertical", command=self.Tree.yview)
        self.Tree.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT, fill='y')

        self.Tree.heading('Title', text='Title')
        self.Tree.column('Title', width=525)
        self.Tree.heading('Duration', text='Duration')
        self.Tree.column('Duration', width=60, anchor='center')

        self.TotalTimeVar = StringVar()
        self.TotalTimeVar.set('--:--')
        self.EscapedTimeVar = StringVar()
        self.EscapedTimeVar.set('--:--')

        self.TimeFrame = Frame(self.container)
        self.EscapedTimeLabel = Label(self.TimeFrame, textvariable=self.EscapedTimeVar, bd=0, takefocus=False)
        self.EscapedTimeLabel.pack(side=LEFT)
        self.TotalTimeLabel = Label(self.TimeFrame, textvariable=self.TotalTimeVar, bd=0)
        self.TotalTimeLabel.pack(side=RIGHT)
        self.TimeFrame.pack(fill='x')

        self.AudioSliderVar = DoubleVar()
        self.AudioSlider = customtkinter.CTkSlider(self.container, from_=0, to=100, variable=self.AudioSliderVar, command=self.SkipAudio)
        self.AudioSlider.pack(fill='x')

        self.VolumeSliderVar = IntVar()
        self.VolumeLabelVar = StringVar()
        self.VolumeLabelVar.set('100%')
        self.VolumeSliderVar.set(100)

        self.BottomFrame = Frame(self.container)
        self.BottomFrame.pack(side=BOTTOM, fill='x')

        self.ButtonsFrame = Frame(self.BottomFrame)
        self.ButtonsFrame.pack(side=LEFT)

        self.PlayButton = Button(self.ButtonsFrame, image=self.PlayImage, **self.ButtonsAttributes, command=self.PlayOrPauseAudio)
        self.PlayButton.pack(side=LEFT)
        self.PreviousButton = Button(self.ButtonsFrame, image=self.PreviousImage, **self.ButtonsAttributes, command=lambda: self.PreviousNextAudio(button_name='Prev'))
        self.PreviousButton.pack(side=LEFT, padx=2)
        self.StopAudioButton = Button(self.ButtonsFrame, image=self.StopAudioImage, **self.ButtonsAttributes, command=self.StopAudio)
        self.StopAudioButton.pack(side=LEFT)
        self.NextButton = Button(self.ButtonsFrame, image=self.NextImage, **self.ButtonsAttributes, command=lambda: self.PreviousNextAudio(button_name='Next', event=Event))
        self.NextButton.pack(side=LEFT, padx=2)
        self.ArtButton = Button(self.ButtonsFrame, image=self.ArtImage, **self.ButtonsAttributes, command=self.ShowAlbumPicture)
        self.ArtButton.pack(side=LEFT)
        self.LrcButton = Button(self.ButtonsFrame, image=self.LrcImage, **self.ButtonsAttributes, command=self.ShowLyricsCommand)
        self.LrcButton.pack(side=LEFT, padx=2)
        self.RepeatButton = Button(self.ButtonsFrame, image=self.RepeatAllImage, **self.ButtonsAttributes, command=self.ToggleRepeat)
        self.RepeatButton.pack(side=LEFT)
        self.RandomButton = Button(self.ButtonsFrame, image=self.RandomDisabledImage, **self.ButtonsAttributes, command=self.ToggleRandom)
        self.RandomButton.pack(side=LEFT, padx=2)
        self.SearchButton = Button(self.ButtonsFrame, image=self.SearchImage, **self.ButtonsAttributes, command=self.ShowFindWidget)
        self.SearchButton.pack(side=LEFT)

        self.VolumeFrame = Frame(self.BottomFrame)
        self.VolumeSliderFrame = Frame(self.VolumeFrame)
        self.MuteUnmuteButton = Button(self.VolumeFrame, image=self.VolumeImage4, **self.ButtonsAttributes, command=self.MuteUnmuteVolume)
        self.MuteUnmuteButton.pack(side=LEFT)
        self.VolumeSlider = customtkinter.CTkSlider(self.VolumeSliderFrame, width=80, from_=0, to=100, variable=self.VolumeSliderVar, command=self.ChangeVolume)
        self.VolumeSlider.pack(side=LEFT, padx=2)
        self.VolumeLabel = Label(self.VolumeSliderFrame, textvariable=self.VolumeLabelVar, width=4, font=font.Font(size=10, weight='bold'))
        self.VolumeLabel.pack(side=LEFT)
        self.VolumeFrame.pack(side=LEFT, padx=2)

        self.InfoFrame = Frame(self.BottomFrame)
        self.InfoFrame.pack(side=RIGHT)
        self.InfoButton = Button(self.InfoFrame, image=self.InfoImage, **self.ButtonsAttributes, command=self.ShowInfo)
        self.InfoButton.pack(padx=2)

        self.SearchStyle = ttk.Style()
        self.SearchEntryVar = StringVar()
        self.SearchEntryVar.trace("w", self.SearchAudio)
        self.SearchFrame = Frame(self.ButtonsFrame, bg='#e5e5e5')
        self.SearchStyle.configure('Search.TEntry')
        self.SearchEntry = ttk.Entry(self.SearchFrame, width=16, style='Search.TEntry', textvariable=self.SearchEntryVar)
        self.SearchEntry.pack(side=LEFT)
        self.ExitSearchButton = Button(self.SearchFrame, image=self.SearchExitImage, bg='#e5e5e5', bd=0, activebackground='#e5e5e5', cursor='hand2', command=self.DestroyFindWidget)
        self.ExitSearchButton.pack(side=RIGHT)

        self.LyricsFrame = Frame(self.AudioListFrame, bg='white', width=621, height=183)
        self.LyricsFrame.pack_propagate(0)
        self.LyricsBox = Text(self.LyricsFrame, cursor='arrow', width=1, height=1, autostyle=False, font=Font(size=15), bg='#e5e5e5', fg='#a1a9b5', wrap='word')
        self.LyricsBox.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.Tree.bind('<Delete>', self.RemoveFromList)
        self.master.bind('<0>', self.RewindCurrentAudio)
        self.master.bind('<MouseWheel>', self.MouseWheel)
        self.master.bind('<space>', self.SpaceBarBindings)
        self.master.bind_all('<Control-i>', self.ShowInfo)
        self.Tree.bind('<Button-1>', self.SingleLeftClick)
        self.AudioSlider.bind('<Button-3>', self.SkipAudio)
        self.master.bind_all('<Control-o>', self.OpenFiles)
        self.master.bind_all("<Button-3>", self.RightClick)
        self.SearchEntry.bind('<Up>', self.UpDownSearchItems)
        self.master.bind_all('<Control-O>', self.GetPlaylist)
        self.SearchEntry.bind('<Down>', self.UpDownSearchItems)
        self.VolumeFrame.bind('<Enter>', self.ShowVolumeSlider)
        self.VolumeFrame.bind('<Leave>', self.HideVolumeSlider)
        self.Tree.bind('<Motion>', self.RestrictResizingHeading)
        self.master.bind_all('<Control-f>', self.ShowFindWidget)
        self.master.bind_all('<Escape>', self.DestroyFindWidget)
        self.Tree.bind('<Shift-Delete>', self.RemoveFromPlaylist)
        self.SearchEntry.bind('<Return>', self.SearchEntryReturnBind)
        self.TotalTimeLabel.bind('<Button-1>', self.ShowRemainingTime)
        self.master.bind_all('<Double-Button-1>', self.DoubleLeftClick)
        self.master.bind("<Control-q>", lambda e: self.master.destroy())
        self.master.bind("<Control-s>", lambda event: self.SavePlaylist(event, True))
        self.Tree.bind('<Control-a>', lambda e: self.Tree.selection_set(self.childrens))
        self.master.bind_all('<Control-Left>', lambda event: self.SkipAudio(event, 'backward'))
        self.master.bind_all('<Control-Right>', lambda event: self.SkipAudio(event, 'forward'))
        self.master.bind_all('<Home>', lambda event, _dir="Top": self.ScrollTopDown(event, _dir))
        self.master.bind_all('<End>', lambda event, _dir="Down": self.ScrollTopDown(event, _dir))
        self.master.bind_all('<Left>', lambda event, change='decrease': self.ChangeVolume(event, change))
        self.master.bind_all('<Right>', lambda event, change='increase': self.ChangeVolume(event, change))
        self.master.bind_all('<Control-n>', lambda event: self.PreviousNextAudio(event, button_name='Next'))
        self.master.bind_all('<Control-p>', lambda event: self.PreviousNextAudio(event, button_name='Prev'))

        self.InitialPosition()
        self.StopWindowFlicking()

        self.master.mainloop()

    def RestrictResizingHeading(self, event):
        '''
        Restrict user to resize the columns of Treeview
        '''

        if self.Tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def StopWindowFlicking(self):
        '''
        When window is minimize and maximized continuously then black
        color gets appear on the window for fraction of seconds which
        looks like the window is flickering
        '''

        if self.master.winfo_ismapped() == 0:  # When window is minimized
            self.container.pack_forget()
            self.master.config(bg='#e5e5e5')
            self.WindowNotMapped = True

        if self.master.winfo_ismapped() == 1 and self.WindowNotMapped:  # When window is restored
            self.master.after(0, lambda: self.container.pack())
            self.WindowNotMapped = False

        self.master.after(5, self.StopWindowFlicking)

    def InitialPosition(self):
        '''
        Set window position to the center when program starts first time
        '''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')
        self.master.deiconify()

    def ClickedAtEmptySpace(self, event=None):
        '''Check if user has clicked in empty space'''

        return self.Tree.identify('item', event.x, event.y) == ''

    def SingleLeftClick(self, event):
        '''
        When user single left click inside Tree widget
        '''

        if self.Tree.identify_region(event.x, event.y) == 'heading':
            # Restrict single left clicking if the cursor is on Treeview's heading
            return

        if not self.AudioFiles:
            # If there is no audio played yet but user left clicks
            # then make single left click event as double left click

            self.OpenFiles()
            return 'break'

    def FormatEscapedTime(self, _time):
        '''
        Remove 00 from the hour part if found
        '''

        _time = _time.split(':')

        if _time[0] == '00':
            _time = ':'.join(_time[1:])

            return _time

    def DoubleLeftClick(self, event=None):
        '''
        When user double clicks anywhere in window
        '''

        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)

        if widget == self.Tree:
            if self.Tree.identify_region(event.x, event.y) == 'heading':
                self.DRY_1()

            elif self.ClickedAtEmptySpace(event):
                # When some files are opened and user double clicks
                # on the empty spaces then open file_dialog to open additional audio files
                self.OpenFiles()

            else:
                selection = self.Tree.selection()

                if selection:
                    index = self.childrens.index(selection[0])

                    if index == self.CurrentPlayingIndex:
                        self.AddRemoveSelection('Add')

                    else:
                        self.isPlaying = None

                    self.PlayOrPauseAudio()

        elif widget in [self.EscapedTimeLabel, self.VolumeLabel] or isinstance(widget, Frame):
            # When user clicks to the empty space or
            # to the EscapedTimeLabel or VolumeLabel
            self.DRY_1()

    def SpaceBarBindings(self, event=None):
        '''
        When user presses space-bar
        '''

        if self.master.focus_get() != self.SearchEntry:
            selections = self.Tree.selection()

            if self.childrens and selections and self.childrens.index(selections[0]) != self.CurrentPlayingIndex:
                self.isPlaying = None

            self.PlayOrPauseAudio()

    def MouseWheel(self, event):
        '''
        Change Volume or Skip Audio when ScrollWheel button
        '''

        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)

        if widget not in [self.Tree, self.AudioSlider, self.scrollbar]:
            self.ChangeVolume(event)

        elif widget == self.AudioSlider:  # Skip audio
            self.SkipAudio(event)

    def ShowVolumeSlider(self, event=None):
        '''
        Show the volume slider when user hovers to volume button
        '''

        self.VolumeSliderFrame.pack(side=LEFT)

    def HideVolumeSlider(self, event=None):
        '''
        Hide the volume slider when user hovers away from the volume button
        '''

        self.VolumeSliderFrame.pack_forget()

    def OpenFiles(self, event=None, files=None):
        '''
        Open dialog box to select audio files
        '''

        audio_name = ''
        ShowErrorMessage = False

        if self.isPlaying:
            audio_name = self.AudioName

        else:
            if self.Tree.selection():
                audio_name = self.Tree.item(self.Tree.focus())['values'][0]

        if files is None:
            files = filedialog.askopenfilenames(filetypes=self.extensions, defaultextension=self.extensions)

        if files:
            if self.ScaleTimer:
                # Stopping updating audio-slider and position of current playing audio
                # to resume audio when finishing adding the new audio to the TreeView
                self.master.after_cancel(self.ScaleTimer)

            for file in files:
                basename = os.path.basename(file)

                if basename not in self.AudioFiles:
                    try:
                        pygame.mixer.music.set_volume(0)
                        pygame.mixer.music.load(file)
                        pygame.mixer.music.play()

                        length = MP3(file).info.length
                        self.TotalAudioDuration += length

                        if isinstance(files, dict):
                            lrc = files[file]['Lyrics']

                        else:
                            lrc = ''

                        self.AudioFiles.update({basename: {'path': file,
                                                           'TagCount': self.TagCount,
                                                           'Lyrics': lrc}})
                        self.TagCount += 1

                    except (pygame.error, HeaderNotFoundError):
                        if ShowErrorMessage is False:
                            ShowErrorMessage = True
                            messagebox.showinfo('ERR', 'Some audio file(s) are not supported so ignoring them')

                    pygame.mixer.music.stop()

            if self.AudioFiles:
                self.Tree.delete(*self.Tree.get_children())  # Emptying TreeView contents

                for key, value in self.AudioFiles.items():  # Inserting data to TreeView
                    path = self.AudioFiles[key]['path']
                    tag = self.AudioFiles[key]['TagCount']
                    length = MP3(path).info.length

                    _time = time.strftime('%H:%M:%S', time.gmtime(length))
                    _time = self.FormatEscapedTime(_time)

                    self.Tree.insert('', END, values=(key, _time), tag=tag)

                self.childrens = self.Tree.get_children()
                self.LowerCasedAudioFiles = [f.lower() for f in self.AudioFiles.keys()]

                if self.IsMuted is False:  # Setting volume as the previously set by the user
                    pygame.mixer.music.set_volume(self.PreviousVolume / 100)

                if audio_name:
                    selIndex = self.childrens[list(self.AudioFiles.keys()).index(audio_name)]

                else:
                    selIndex = self.childrens[0]

                # Selecting audio and scrolling to the that selected audio
                self.Tree.focus_force()
                self.Tree.see(selIndex)
                self.Tree.focus(selIndex)
                self.Tree.selection_set(selIndex)

                if len(self.AudioFiles) == 1:  # Play audio if user opens only one audio file
                    self.PlayOrPauseAudio()

                elif self.isPlaying:  # Resuming audio after finishing opening audios
                    pygame.mixer.music.load(self.AudioFiles[self.AudioName]['path'])
                    pygame.mixer.music.play(start=self.CurrentPos)
                    self.UpdateScale()

                self.TotalAudioFiles = len(self.AudioFiles) - 1

        return 'break'

    def SortAudio(self, by):
        '''
        Sort audio list in Treeview alphabetically
        '''

        selected_text = ''
        sel = self.Tree.selection()

        if sel:
            selected_text = self.Tree.item(sel[-1])['values'][0]

        self.Tree.delete(*self.Tree.get_children())

        if by == 'name':
            self.AudioFiles = dict(sorted(self.AudioFiles.items(), key=lambda item: os.path.basename(item[0]).lower()))

        elif by == 'date':
            self.AudioFiles = dict(sorted(self.AudioFiles.items(), key=lambda item: os.path.getctime(item[1]['path'])))

        for key, value in self.AudioFiles.items():
            length = MP3(self.AudioFiles[key]['path']).info.length

            _time = time.strftime('%H:%M:%S', time.gmtime(length))
            _time = self.FormatEscapedTime(_time)

            self.Tree.insert('', END, values=(key, _time), tag=self.AudioFiles[key]['TagCount'])

        child = None
        self.childrens = self.Tree.get_children()

        for children in self.childrens:
            if self.Tree.item(children)['values'][0] == selected_text:
                child = children
                break

        if child:
            self.Tree.selection_set(child)
            self.Tree.see(child)

    def GetPlaylist(self, event=None):
        '''
        Get audio path stored in a file
        '''

        try:
            with open(self.PlaylistPath, 'r') as f:
                contents = json.load(f)

        except (json.decoder.JSONDecodeError, FileNotFoundError):
            contents = {}
            messagebox.showerror('ERR', 'Either playlists file is corrupt or does not exist')

        if contents:
            files = {k: {'Lyrics': v['Lyrics']} for k, v in contents.items() if os.path.exists(k)}  # Removing audios that does not exists
            self.OpenFiles(files=files)

        else:
            self.PlayError.play()

    def ScrollTopDown(self, event=None, _dir=None):
        '''
        Scroll to the top when "HOME" key is pressed or to the bottom when
        "END" key is pressed
        '''

        try:
            if _dir == "Top":
                index = self.childrens[0]

            else:
                index = self.childrens[self.TotalAudioFiles]

            self.Tree.see(index)
            self.Tree.selection_set(index)

        except (IndexError, AttributeError):
            self.PlayError.play()

    def AddRemoveSelection(self, status):
        '''
        Add or Remove selection when audio changes
        '''

        if self.AudioName:
            _tag = self.AudioFiles[self.AudioName]['TagCount']

        if status == 'Remove':
            if self.AudioName:  # Removing the previous selection if another audio has been played before
                self.Tree.tag_configure(_tag, background='#e5e5e5', foreground='#333333')

        else:
            if self.AudioName is None:
                self.PlayOrPauseAudio()

            else:
                self.Tree.tag_configure(_tag, background='#29465b')
                self.Tree.selection_remove(self.Tree.selection()[0])

    def PlayOrPauseAudio(self, event=None):
        '''
        Play or pause audio when play or pause button is pressed
        '''

        try:
            if self.AudioFiles:
                if self.isPlaying is None:  # Audio not playing yet
                    cursel = self.Tree.selection()
                    self.AddRemoveSelection('Remove')

                    if len(cursel) == 1:  # Play Audio if there is only one selection
                        cursel = cursel[0]
                        self.CurrentPlayingIndex = self.childrens.index(cursel)

                        if self.PrevID != cursel:  # Play Audio only if current playing audio is different than selected audio
                            self.PrevID = cursel
                            self.isPlaying = True
                            self.RotateImageAngle = 10
                            _image = self.PauseImage

                            self.AudioName = self.Tree.item(cursel)['values'][0]
                            self.CurrentAudioPath = self.AudioFiles[self.AudioName]['path']

                            self.TotalTime = MP3(self.CurrentAudioPath).info.length
                            self.AudioSlider.configure(to=int(self.TotalTime))
                            self.Tree.tag_configure(self.AudioFiles[self.AudioName]['TagCount'], foreground='silver')

                            _time = time.strftime('%H:%M:%S', time.gmtime(self.TotalTime))
                            _time = self.FormatEscapedTime(_time)

                            self.TotalTimeVar.set(_time)
                            self.EscapedTimeVar.set('00:00')
                            self.AudioSliderVar.set(0)

                            self.AddRemoveSelection('Add')
                            lrc_path = self.AudioFiles[self.AudioName]['Lyrics']

                            if lrc_path:
                                # Insert lyrics text to display lyrics
                                # of respective audios if exists
                                self.IsLyricsAdded = False
                                self.InsertLyricsText(lrc_path=lrc_path)

                            else:
                                if self.IsLyricsAdded is not None:
                                    self.IsLyricsAdded = None
                                    self.LyricsFrame.pack_forget()
                                    self.TreeFrame.pack()

                            self.StopImageRotation()
                            pygame.mixer.music.load(self.CurrentAudioPath)  # Loading selected file for playing
                            pygame.mixer.music.play()  # Start playing loaded file

                            if self.ScaleTimer:
                                self.master.after_cancel(self.ScaleTimer)

                            if self.IsDefaultImage:
                                # When user clicks Art button first and then clicks play button later
                                self.rotate_image()

                            self.ScaleTimer = self.master.after(250, self.UpdateScale)

                elif self.isPlaying is True:  # Audio is being played
                    self.isPlaying = False
                    _image = self.PlayImage

                    self.StopImageRotation()
                    pygame.mixer.music.pause()
                    self.master.after_cancel(self.ScaleTimer)

                elif self.isPlaying is False:  # Audio is paused
                    self.isPlaying = True
                    _image = self.PauseImage

                    pygame.mixer.music.set_pos(self.AudioSliderVar.get())
                    pygame.mixer.music.unpause()

                    if self.IsDefaultImage and self.RotateImageTimer is None:
                        # When user resumes audio while the animation is not shown yet
                        self.rotate_image()

                    self.ScaleTimer = self.master.after(250, self.UpdateScale)

                self.PlayButton.config(image=_image)

            else:
                self.PlayError.play()

        except (TclError, UnboundLocalError):
            pass

    def StopAudio(self, event=None):
        '''
        Stop playing audio
        '''

        if self.isPlaying is not None:  # If audio is playing or is paused
            pygame.mixer.music.stop()

            if self.ScaleTimer:
                self.master.after_cancel(self.ScaleTimer)

            self.PrevID = ''
            self.isPlaying = None
            self.AudioSliderVar.set(0)
            self.CurrentPlayingIndex = 0
            self.TotalTimeVar.set('--:--')
            self.EscapedTimeVar.set('--:--')
            self.Tree.see(self.childrens[0])
            self.AddRemoveSelection('Remove')
            self.Tree.selection_set(self.childrens[0])
            self.PlayButton.config(image=self.PlayImage)

            if self.IsAlbumPictureShown:
                self.IsAlbumPictureShown = False
                self.AlbumPictureFrame.pack_forget()
                self.TreeFrame.pack()

            if self.IsLyricsAdded is not None:
                self.IsLyricsAdded = None
                self.LyricsFrame.pack_forget()
                self.TreeFrame.pack()

            self.StopImageRotation()

        else:
            self.PlayError.play()

    def ToggleRepeat(self, event=None):
        '''
        When user clicks repeat button
        '''

        if self.RepeatAudio is None:  # Button has not clicked yet
            self.RepeatAudio = 'LoopAll'
            self.RepeatButton.config(relief='sunken')

        elif self.RepeatAudio == 'LoopAll':
            self.RepeatAudio = 'LoopCurrent'
            self.RepeatButton.config(image=self.RepeatCurrentImage)

        elif self.RepeatAudio == 'LoopCurrent':
            self.RepeatAudio = None
            self.RepeatButton.config(image=self.RepeatAllImage, relief='raised')

    def ToggleRandom(self, event=None):
        '''
        When user clicks random button
        '''

        if self.PlayRandom is False:
            self.PlayRandom = True
            self.RandomButton.config(image=self.RandomActiveImage)

        else:
            self.PlayRandom = False
            self.RandomButton.config(image=self.RandomDisabledImage)

    def UpdateScale(self, event=None):
        '''
        Continuously update escaping time and slider values until songs comes to end
        '''

        self.CurrentPos = pygame.mixer.music.get_pos() / 1000
        self.ShowSubtitle()

        if self.AudioSliderVar.get() > int(self.CurrentPos):
            # When user skips audio and the position of AudioSlider
            # becomes more than the previous AudioSlider position
            self.CurrentPos = self.AudioSliderVar.get() + 1

        _time = time.strftime('%H:%M:%S', time.gmtime(self.CurrentPos))
        _time = self.FormatEscapedTime(_time)

        self.EscapedTimeVar.set(_time)
        self.AudioSliderVar.set(int(self.CurrentPos))

        if int(self.CurrentPos) >= int(self.TotalTime):  # Checking if audio has complete playing
            self.master.after_cancel(self.ScaleTimer)

            self.AudioSliderVar.set(0)
            self.TotalTimeVar.set('--:--')
            self.EscapedTimeVar.set('--:--')

            if self.CurrentPlayingIndex == self.TotalAudioFiles:
                if self.RepeatAudio in ['LoopAll', 'LoopCurrent'] or self.PlayRandom:
                    self.EOF = False

                else:
                    self.EOF = True
                    self.StopAudio()

            if self.EOF:
                self.EOF = False
                self.ShowRemTime = False
                self.PlayButton.config(image=self.PlayImage)

                if self.RemTimer:
                    self.master.after_cancel(self.RemTimer)

            elif self.RepeatAudio == 'LoopCurrent':
                self.PrevID = ''
                self.isPlaying = None
                self.Tree.selection_set(self.childrens[self.CurrentPlayingIndex])
                self.PlayOrPauseAudio()

            elif self.RepeatAudio == 'LoopAll' and self.CurrentPlayingIndex == self.TotalAudioFiles:
                if self.PlayRandom is True:
                    self.PreviousNextAudio(button_name='next')

                else:
                    self.PrevID = ''
                    self.isPlaying = None
                    self.Tree.selection_set(self.childrens[0])
                    self.Tree.see(self.childrens[0])
                    self.PlayOrPauseAudio()

            else:
                self.PreviousNextAudio(button_name='next')

        else:
            self.ScaleTimer = self.master.after(1000, self.UpdateScale)

    def PreviousNextAudio(self, event=None, button_name=None):
        '''
        Play previous and present audio present in list-box
        '''

        try:
            if self.AudioFiles:
                if self.PlayRandom:
                    self.PrevID = ''
                    self.CurrentPlayingIndex = random.randint(0, self.TotalAudioFiles)

                elif button_name == 'Prev':
                    if self.RepeatAudio == 'LoopCurrent' and self.CurrentPlayingIndex == 0:
                        self.CurrentPlayingIndex = self.TotalAudioFiles + 1

                    elif self.CurrentPlayingIndex == 0:
                        return

                    self.CurrentPlayingIndex -= 1

                else:
                    if self.RepeatAudio == 'LoopCurrent' and self.CurrentPlayingIndex == self.TotalAudioFiles:
                        self.CurrentPlayingIndex = 0

                    elif self.CurrentPlayingIndex >= self.TotalAudioFiles:
                        return

                    self.CurrentPlayingIndex += 1

                self.isPlaying = None
                self.AddRemoveSelection('Remove')

                item = self.childrens[self.CurrentPlayingIndex]
                self.Tree.see(item)
                self.Tree.focus(item)
                self.Tree.selection_set(item)
                self.PlayOrPauseAudio()

                if self.IsAlbumPictureShown:
                    self.ShowAlbumPicture(force_show=True)

            else:
                self.PlayError.play()

        except TclError:
            pass

    def SkipAudio(self, event=None, direction=None):
        '''
        Skip song as the user moves the slider
        '''

        if self.isPlaying:
            SkipAt = self.AudioSliderVar.get()

            if direction == 'forward':
                SkipAt += 5

                if SkipAt >= self.TotalTime:
                    self.PreviousNextAudio()
                    return

            elif direction == 'backward':
                SkipAt -= 5

                if SkipAt <= 0:
                    SkipAt = 0

            if self.isPlaying:
                pygame.mixer.music.play(start=SkipAt)
                self.MuteUnmuteVolume(nochange=True)

            _time = time.strftime('%H:%M:%S', time.gmtime(SkipAt))
            _time = self.FormatEscapedTime(_time)

            self.AudioSliderVar.set(SkipAt)
            self.EscapedTimeVar.set(_time)

    def ChangeVolume(self, event=None, change=None):
        '''
        Increase or decrease volume when user drags volume bar or when user
        presses right arrow or left arrow
            Here volume value is between 0-1
        '''

        if self.master.focus_get() == self.SearchEntry and not event:
            self.master.tk_focusNext().focus()

        CurrentVolume = self.VolumeSliderVar.get()

        if change == 'increase':
            CurrentVolume += 5

            if CurrentVolume >= 100:
                CurrentVolume = 100

        elif change == 'decrease':
            CurrentVolume -= 5

            if CurrentVolume <= 0:
                CurrentVolume = 00

        if CurrentVolume == 0:
            self.IsMuted = False

        else:
            self.IsMuted = True
            self.PreviousVolume = CurrentVolume

        self.MuteUnmuteVolume()

        return 'break'

    def MuteUnmuteVolume(self, event=None, nochange=False):
        '''
        Mute and Unmute volume

        nochange parameter is to skip indented block of following first if
        statement to un-change volume when audio is skipped or changed
        '''

        if nochange is False:
            if self.IsMuted is False:  # Volume is not muted before
                self.IsMuted = True
                self.PreviousVolume = self.VolumeSliderVar.get()
                self.VolumeLabelVar.set('0%')
                pygame.mixer.music.set_volume(0)
                self.VolumeSliderVar.set(0)

            else:  # Volume is muted before
                self.IsMuted = False
                self.VolumeSliderVar.set(self.PreviousVolume)
                pygame.mixer.music.set_volume(self.PreviousVolume / 100)
                self.VolumeLabelVar.set(f'{self.PreviousVolume}%')

        SliderGet = self.VolumeSliderVar.get()

        if SliderGet == 0:
            self.MuteUnmuteButton.config(image=self.NoVolumeImage)

        elif SliderGet <= 25:
            self.MuteUnmuteButton.config(image=self.VolumeImage1)

        elif SliderGet <= 50:
            self.MuteUnmuteButton.config(image=self.VolumeImage2)

        elif SliderGet <=75:
            self.MuteUnmuteButton.config(image=self.VolumeImage3)

        else:
            self.MuteUnmuteButton.config(image=self.VolumeImage4)

    def ShowRemainingTime(self, event=None):
        '''
        Show remaining time of current playing audio
        '''

        if self.isPlaying is not None:
            if self.ShowRemTime is False:  # If remaining time has not been shown
                self.ShowRemTime = True
                self.ChangeTime()

            else:  # Remaining time has already been show
                self.ShowRemTime = False
                self.master.after_cancel(self.RemTimer)

                _time = time.strftime('%H:%M:%S', time.gmtime(self.TotalTime))
                _time = self.FormatEscapedTime(_time)

                self.TotalTimeVar.set(_time)

    def ChangeTime(self):
        '''
        Calculate remaining time of currently playing song
        '''

        gmtime = time.gmtime(self.TotalTime - self.CurrentPos)

        _time = time.strftime('%H:%M:%S', gmtime)
        _time = self.FormatEscapedTime(_time)

        self.TotalTimeVar.set(f'-{_time}')
        self.RemTimer = self.master.after(500, self.ChangeTime)

    def RightClick(self, event=None):
        '''
        When user right clicks inside list-box
        '''

        x, y = event.x , event.y  # Cursor position with respect to Tk window
        _x, _y = self.master.winfo_pointerxy()  # Cursor position with respect to monitor resolution

        CurrentSelection = self.Tree.selection()
        widget = self.master.winfo_containing(_x, _y)
        RightClickMenu = Menu(self.master, tearoff=False)

        if widget == self.Tree:
            region = self.Tree.identify_region(x, y)

            if CurrentSelection:
                if self.ClickedAtEmptySpace(event):
                    RightClickMenu.add_command(label='Open', command=self.OpenFiles)

                else:
                    if len(self.Tree.selection()) == 1:
                        self.Tree.event_generate("<Button-1>", x=x, y=y)
                        RightClickMenu.add_command(label='Add Lyrics', command=self.InsertLyrics)
                        RightClickMenu.add_command(label='Set Album Art', command=self.SetAlbumArt)

                    RightClickMenu.add_command(label='Remove from list', command=self.RemoveFromList)
                    RightClickMenu.add_command(label='Remove from playlist', command=self.RemoveFromPlaylist)

            else:
                if self.Tree.identify_element(x, y) == 'text':
                    self.Tree.event_generate('<Button-1>', x=x, y=y)
                    self.Tree.event_generate('<Button-3>', x=x, y=y)

                elif region == 'heading' or self.ClickedAtEmptySpace(event):
                    RightClickMenu.add_command(label='Open', command=self.OpenFiles)
                    RightClickMenu.add_command(label='Open Playlist', command=self.GetPlaylist)

            if self.Tree.selection() and region != 'heading':
                sub_menu = Menu(RightClickMenu, tearoff=0)
                sub_menu.add_command(label='By name', command=lambda: self.SortAudio('name'))
                sub_menu.add_command(label='By date', command=lambda: self.SortAudio('date'))

                RightClickMenu.add_cascade(label='Sort', menu=sub_menu)
                RightClickMenu.add_command(label='Remove Permanently (Caution!)', activeforeground='red', command=self.RemovePermanently)

        elif widget in [self.EscapedTimeLabel, self.VolumeLabel] or isinstance(widget, Frame):
            RightClickMenu.add_command(label='Open', command=self.OpenFiles)
            RightClickMenu.add_command(label='Open Playlist', command=self.GetPlaylist)

        try:
            RightClickMenu.post(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def RemoveFromList(self, event=None):
        '''
        Remove selected item from the list-box
        '''

        try:
            CurrentIndexes = self.Tree.selection()

            for iid in CurrentIndexes:
                if self.childrens.index(iid) == self.CurrentPlayingIndex and self.isPlaying is not None:
                    self.StopAudio()

                song_name = self.Tree.item(iid)['values'][0]
                pop_item = self.AudioFiles.pop(song_name)
                self.TotalAudioDuration -= MP3(pop_item['path']).info.length

            self.Tree.delete(*CurrentIndexes)
            self.LowerCasedAudioFiles = [f.lower() for f in self.AudioFiles.keys()]

            self.isPlaying = None
            self.AudioName = None
            self.CurrentPlayingIndex = None

            index = self.childrens.index(iid)
            self.childrens = self.Tree.get_children()
            self.Tree.focus(self.childrens[index])
            self.Tree.selection_set(self.childrens[index])
            self.TotalAudioFiles = len(self.AudioFiles) - 1

        except (IndexError, TclError):
            pass

    def RemoveFromPlaylist(self, event=None):
        '''
        Remove selected item from the list-box as well from the playlist file
        '''

        self.RemoveFromList()
        self.SavePlaylist()

    def RemovePermanently(self):
        '''
        Delete the selected files entirely from the device
        '''

        selections = self.Tree.selection()
        confirm = messagebox.askyesno('Really?', 'This action will permanently delete your selected file(s). You cannot undo this action.\n\nDo you still want to continue?')

        if confirm:
            for selection in selections:
                file = self.Tree.item(selection)['values'][0]

                if file in self.AudioFiles:
                    file_path = self.AudioFiles[file][0]
                    os.remove(file_path)

            self.RemoveFromPlaylist()

    def SavePlaylist(self, event=None, show_message=False):
        '''
        Save audio path present in list-box
        '''

        if self.AudioFiles:
            newAudioFiles = {v['path']: {'Lyrics': v['Lyrics']} for _, v in self.AudioFiles.items()}  # Saving Audios path without tagCount

            with open(self.PlaylistPath, 'w') as f:
                # contents = {'playlists': newAudioFiles}
                json.dump(newAudioFiles, f, indent=4)

                if show_message:
                    messagebox.showinfo('Saved!', 'Playlist Saved !!')

        else:
            self.PlayError.play()

    def ShowFindWidget(self, event=None):
        '''
        Show Find widget if not already shown
        '''

        if self.AudioFiles:
            if self.IsFindWidgetShown is False:
                self.IsFindWidgetShown = True
                self.SearchEntry.focus()
                self.SearchButton.pack_forget()
                self.SearchFrame.pack(side=LEFT)

            else:
                self.SearchEntry.focus()

        else:
            self.PlayError.play()

    def DestroyFindWidget(self, event=None):
        '''
        Destroy Find widget when pressed ESC or X button
        '''

        self.master.focus_force()
        self.SearchEntryVar.set('')
        self.IsFindWidgetShown = False
        self.SearchFrame.pack_forget()
        self.SearchButton.pack(side=LEFT)

    def SearchAudio(self, *args):
        '''
        Searching Audio
        '''

        try:
            value = self.SearchEntryVar.get().lower()

            if value:
                self.filteredFiles = [f for f in self.LowerCasedAudioFiles if f.startswith(value)]
                self.SearchLocalIndex = 0

                self.SearchGlobalIndex = self.LowerCasedAudioFiles.index(self.filteredFiles[self.SearchLocalIndex])
                item = self.childrens[self.SearchGlobalIndex]
                self.Tree.see(item)

        except (IndexError, AttributeError):
            pass

    def UpDownSearchItems(self, event=None):
        '''
        When user presses Up or Down arrow in SearchEntry box
        '''

        try:
            arrow = event.keysym

            if not self.SearchEntryVar.get():
                self.filteredFiles = []

            if arrow == 'Up':
                if self.SearchLocalIndex == 0:
                    self.SearchLocalIndex = len(self.filteredFiles)

                self.SearchLocalIndex -= 1

            elif arrow == 'Down':
                if self.SearchLocalIndex == len(self.filteredFiles) - 1:
                    self.SearchLocalIndex = -1

                if self.SearchLocalIndex != 0:
                    self.SearchLocalIndex += 1

            self.SearchGlobalIndex = self.LowerCasedAudioFiles.index(self.filteredFiles[self.SearchLocalIndex])

            item = self.childrens[self.SearchGlobalIndex]
            self.Tree.see(item)
            self.Tree.focus(item)
            self.Tree.selection_set(item)
            self.Tree.focus_force()

        except (TypeError, AttributeError, IndexError):
            # When no audio is opened though user wants to make a search
            self.PlayError.play()

    def SearchEntryReturnBind(self, event=None):
        '''
        When user hits Enter key when focused to SearchEntry box
        '''

        if self.SearchGlobalIndex:
            item = self.childrens[self.SearchGlobalIndex]
            self.Tree.focus(item)
            self.Tree.selection_set(item)

            if self.SearchGlobalIndex != self.CurrentPlayingIndex:
                self.isPlaying = None

            self.PlayOrPauseAudio()
            self.DestroyFindWidget()

    def DRY_1(self):
        '''
        Some conditions that are used for multiple times. So, to avoid
        repetition putting them in this method
        '''

        if self.isPlaying is not None:
            self.PlayOrPauseAudio()

        elif not self.AudioFiles:
            self.OpenFiles()

    def ShowInfo(self, event=None):
        '''
        Show basic audio information
        '''

        try:
            TotalFiles = len(self.AudioFiles)

            if TotalFiles >= 0:
                TotalTime = str(datetime.timedelta(seconds=int(self.TotalAudioDuration))).zfill(8).replace(':', ' : ')
                details = f"Total Audio: {TotalFiles}\nTotal Time: {TotalTime}"

            else:
                details = "Nothing to show"

        except AttributeError:
            details = "Nothing to show"

        messagebox.showinfo("Details", details)

    def ShowAlbumPicture(self, force_show=False):
        '''
        Show Album Picture instead of TreeView when clicked to art button

        When user plays next or previous audio then force_show when True changes
        the album picture when the previous album picture is shown already
        '''

        self.StopImageRotation()
        self.IsDefaultImage = True

        if self.IsLyricsAdded:
            self.IsLyricsAdded = False
            self.LyricsFrame.pack_forget()

        if self.IsAlbumPictureShown is False or force_show is True:
            image = ''
            self.IsAlbumPictureShown = True

            if self.isPlaying is not None:   # When audio is being played or is paused
                audioPath = self.AudioFiles[self.AudioName]['path']  # Getting the current playing or paused audio_path

                try:
                    mp3 = stagger.read_tag(audioPath)
                    by_data = mp3[stagger.id3.APIC][0].data   # Getting the image from the audio file
                    image = io.BytesIO(by_data)  # Storing the image to memory
                    size = (300, 300)

                except (stagger.errors.NoTagError, KeyError):
                    pass

            if image:
                self.IsDefaultImage = False

            else:
                # When audio do not have any audio_image then setting the default music image
                size = (175, 175)
                image = self.AlbumArtImage

            im = Image.open(image)
            im.thumbnail(size, Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(im)

            if force_show is False:
                self.TreeFrame.pack_forget()
                self.AlbumPictureFrame = Frame(self.AudioListFrame)
                self.AlbumPictureFrame.pack()
                self.AlbumPictureLabel = Label(self.AlbumPictureFrame, width=self.Tree.winfo_width() + 12, height=self.Tree.winfo_reqheight() - 4)
                self.AlbumPictureLabel.pack(side=BOTTOM)

            try:
                self.AlbumPictureLabel.config(image=image)
                self.AlbumPictureLabel.image = image

                if self.IsDefaultImage:
                    # Start animation only if there is no audio-image in audio
                    self.rotate_image()

            except AttributeError:
                # When user stops the audio without showing the album picture then the
                # self.AlbumPictureLabel does not exists as it has never been created
                # before which triggers AttributeError then ignoring this error
                pass

        else:
            self.IsAlbumPictureShown = False
            self.AlbumPictureFrame.pack_forget()
            self.TreeFrame.pack()

    def SetAlbumArt(self, event=None):
        '''
        Add image to album art of a selected audio
        '''

        try:
            image_path = filedialog.askopenfilenames(filetypes=[('Images', '.jpg .png .jpeg')])
            path_length = len(image_path)

            if path_length == 1:
                if self.isPlaying is not None:
                    # Quitting pygame to stop playing audio because stagger module needs
                    # the selected audio must not be used by any other applications/modules
                    pygame.mixer.music.stop()
                    pygame.quit()
                    self.master.after_cancel(self.ScaleTimer)

                image_path = image_path[0]

                # Getting the selected value
                sel = self.Tree.selection()[0]
                item = self.Tree.item(sel)['values'][0]
                audio_path = self.AudioFiles[item][0]

                # Saving image to audio as album art
                mp3 = stagger.read_tag(audio_path)
                mp3.picture = image_path
                mp3.write()

                if self.isPlaying is not None:
                    # When audio is being played or paused then resuming it
                    pygame.mixer.init()
                    pygame.mixer.music.load(self.AudioFiles[self.AudioName][0])
                    pygame.mixer.music.play(start=self.CurrentPos)

                    if self.isPlaying is False:
                        # If audio was paused before then restoring it state as paused
                        pygame.mixer.music.pause()

                    else:
                        # If audio was being played then resuming from the previous position
                        # Also restoring the previous volume value
                        pygame.mixer.music.set_volume(self.PreviousVolume / 100)
                        self.UpdateScale()

            elif path_length > 1:  # When user opens more than one images
                messagebox.showerror('ERR', 'Only one image file was expected')

        except stagger.errors.NoTagError:
            # Some audios do not support stagger module
            messagebox.showerror('ERR', 'Cannot add album art to the selected audio')

    def RewindCurrentAudio(self, event=None):
        '''
        Rewind the playing audio from the start when user presses 0
        '''

        if isinstance(event.widget, ttk.Entry):
            # Don't re-wind the audio when the
            # focus is in the search Entry widget
            return

        _child = None
        playing = self.isPlaying

        for child in self.Tree.get_children():  # Getting child of playing audio
            value = self.Tree.item(child)['values'][0]

            if value == self.AudioName:
                _child = child
                break

        if self.isPlaying is not None:  # When audio is either playing or is paused
            self.StopAudio()

            self.Tree.selection_set(_child)
            self.PlayOrPauseAudio()  # Playing the audio from the start

            if playing is False:
                # When the audio was previously paused
                # then maintaining the same state
                self.isPlaying = True
                self.PlayOrPauseAudio()

            self.master.focus_set()

    def ReadLyricsFile(self, lrc_path):
        '''
        Extracting lyrics from either lrc, srt or vtt file
        '''

        details = dict()

        with open(lrc_path) as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            # Extracting lyrics from .lrc file
            time_pattern = re.compile(r'\[.*?\]')
            _time = re.search(time_pattern, line)

            if _time:
                text = line[_time.end(0):].strip().strip('\n')
                _time = _time.group()[1:-1]

                if text:
                    _time = self.GetTotalSeconds(_time)
                    details[_time] = text

            else:  # Extracting lyrics from .srt or vtt file
                time_pattern = re.compile(r'\d+:\d+:\d+[\.,]\d+')
                _time = re.search(time_pattern, line)

                if _time:
                    _time = _time.group().replace(',', '.')
                    _time = self.GetTotalSeconds(_time)
                    details[_time] = lines[index + 1]

        return details

    def ShowSubtitle(self):
        '''
        Update Lyrics as the position of the audio
        '''

        if self.IsLyricsAdded:
            _time = datetime.timedelta(seconds=self.AudioSliderVar.get()).total_seconds() + 1

            closest = self.take_closest(list(self.LyricsDetails.keys()), _time)
            index = list(self.LyricsDetails.keys()).index(closest) + 1

            lineinfo = self.LyricsBox.dlineinfo(f'{self.TrackLine}.0')
            diff = lineinfo[1] - 23

            if diff > 0:
                self.LyricsBox.yview_scroll(lineinfo[1] - 23, 'pixels' )

            if 'config' in self.LyricsBox.tag_names():
                self.LyricsBox.tag_delete('config', f'{self.TrackLine}.0 linestart', f'{self.TrackLine}.0 lineend')

            self.TrackLine = index
            self.LyricsBox.tag_add('config', f'{self.TrackLine}.0 linestart', f'{self.TrackLine}.0 lineend')
            self.LyricsBox.tag_configure('config', font=Font(size=20, weight='bold'), foreground='black')

            self.LyricsBox.see(f'{self.TrackLine}.0')

    def ShowLyricsCommand(self, event=None):
        '''
        When user clicks lyrics button
        '''

        if self.AudioFiles:
            filetypes = [('Lyrics', '*.lrc *srt *vtt')]

            if self.IsLyricsAdded is None:  # If lyrics is not added before
                lrc_path = filedialog.askopenfilename(filetypes=filetypes, defaultextension=filetypes)

                if os.path.exists(lrc_path):  # Add only if the given path exists
                    self.InsertLyricsText(lrc_path)
                    self.ShowSubtitle()

                    self.IsLyricsAdded = False

            elif self.IsLyricsAdded is True:
                # When lyrics has been added before but user presses the
                # lyrics button then destroying(hiding) the lyrics texts
                self.IsLyricsAdded = False
                self.LyricsFrame.pack_forget()
                self.TreeFrame.pack()

            elif self.IsLyricsAdded is False:
                # When lyrics has been added but was destroyed by pressing
                # the lyrics button and again showing the same lyrics texts
                # when user wants it back
                self.TreeFrame.pack_forget()

                if self.IsAlbumPictureShown:
                    self.IsAlbumPictureShown = False
                    self.AlbumPictureFrame.pack_forget()

                self.IsLyricsAdded = True
                self.LyricsFrame.pack()

        else:
            self.PlayError.play()

    def GetTotalSeconds(self, _time):
        '''
        Convert string time into total seconds
        '''

        split = _time.split(':')
        format = ['%H', '%M', '%S.%f']

        if len(split) <= 2:
            formatter = ':'.join(format[1:])

        else:
            formatter = ':'.join(format)

        obj = datetime.datetime.strptime(_time, formatter)
        _time = obj.hour * 3600 + obj.minute * 60 + obj.second + obj.microsecond / 1000000
        _time = datetime.timedelta(seconds=_time).total_seconds()

        return _time

    def take_closest(self, myList, myNumber):
        '''
        Assumes myList is sorted. Returns closest value to myNumber. If two
        numbers are equally close, return the smallest number.
        '''

        pos = bisect.bisect_left(myList, myNumber)

        if pos == 0:
            return myList[0]

        if pos == len(myList):
            return myList[-1]

        before = myList[pos - 1]
        after = myList[pos]

        if after - myNumber < myNumber - before:
            return after

        else:
            return before

    def InsertLyrics(self, event=None, lrc_path=None):
        '''
        Save lyrics with the corresponding audio
        '''

        filetypes = [('Lyrics', '*.lrc *srt *vtt')]

        if lrc_path is None:
            lrc_path = filedialog.askopenfilename(filetypes=filetypes, defaultextension=filetypes)

        if lrc_path:
            values = self.AudioFiles[self.AudioName]
            values['Lyrics'] = lrc_path

            self.AudioFiles[self.AudioName] = values
            self.SavePlaylist()

    def InsertLyricsText(self, lrc_path):
        '''
        Add text to lyrics text box
        '''

        self.LyricsDetails = self.ReadLyricsFile(lrc_path)
        self.LyricsBox.tag_configure("center", justify='center')

        for value in self.LyricsDetails.values():
            self.LyricsBox.insert(END, value.strip('\n') + '\n')

        self.LyricsBox.tag_add("center", "1.0", "end")

    def rotate_image(self):
        '''
        Rotating image continuously like an animation
        '''

        size = (175, 175)

        if self.RotateImageAngle > 360:
            self.RotateImageAngle = 10

        if self.isPlaying is True:
            image = Image.open(self.AlbumArtImage)
            image_rot = image.rotate(-self.RotateImageAngle)

            image_rot.thumbnail(size, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image_rot)

            self.AlbumPictureLabel.config(image=photo_image)
            self.AlbumPictureLabel.image = photo_image

            self.RotateImageAngle += 10

        self.RotateImageTimer = self.master.after(10, self.rotate_image)

    def StopImageRotation(self):
        '''
        Cancel image rotation animation
        '''

        if self.RotateImageTimer is not None:
            self.master.after_cancel(self.RotateImageTimer)
            self.RotateImageTimer = None

    def ResourcePath(self, FileName):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', FileName)


if __name__ == '__main__':
    MusicPlayer()
