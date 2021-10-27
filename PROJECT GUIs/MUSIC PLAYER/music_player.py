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

        self.files = dict()
        self.previous_volume = None
        self.current_playing_index = -1
        self.extensions = [('Music Files', '*.mp3')]
        self.file_path = self.resource_path('playlists.json')
        self.song_name = None  # Store currently playing song's name
        self.eof = False  # Trigger to check if the last songs is about to play
        self.rem_timer = None  # Stores an alarm to call change_time function in every 500 ms
        self.scale_timer = None  # Stores an alarm to call update_scale function in every 1000 ms
        self.showed_rem_time = False  # Trigger to check if remaining time has showed in total time button
        self.is_playing = None  # Trigger to check if the song is playing. None for has not started playing yet, True for playing and False for pause

        self.master = Tk()
        self.master.withdraw()
        self.master.iconbitmap(self.resource_path('icon.ico'))
        self.master.title('Music Player')

        self.play_image = PhotoImage(file=self.resource_path('Play.png'))
        self.stop_image = PhotoImage(file=self.resource_path('Stop.png'))
        self.next_image = PhotoImage(file=self.resource_path('Next.png'))
        self.mute_image = PhotoImage(file=self.resource_path('Mute.png'))
        self.pause_image = PhotoImage(file=self.resource_path('Pause.png'))
        self.unmute_image = PhotoImage(file=self.resource_path('Unmute.png'))
        self.previous_image = PhotoImage(file=self.resource_path('Previous.png'))

        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.master.config(menu=self.menu)

        self.file_menu.add_command(label='Open', accelerator='Ctrl + O', command=self.open_files)
        self.file_menu.add_command(label='Open Playlist', accelerator='Ctrl + P', command=self.get_playlist)
        self.file_menu.add_command(label='Save Playlist', accelerator='Ctrl + Shift + P', command=self.save_playlists)
        self.file_menu.add_command(label='Exit', accelerator='Ctrl + Q', command=self.master.destroy)

        self.variable = Variable()
        self.audio_list = Listbox(self.master, listvariable=self.variable, activestyle='none', height=10, width=100, bg='#f9f9fa', fg='purple', selectmode=MULTIPLE)
        self.audio_list.pack(fill='x')

        self.total_time_var = StringVar()
        self.total_time_var.set('--:--')
        self.escaped_time_var = StringVar()
        self.escaped_time_var.set('--:--')
        self.time_frame = Frame(self.master)
        self.escaped_time_label = Label(self.time_frame, textvariable=self.escaped_time_var, bd=0, takefocus=False)
        self.escaped_time_label.pack(side=LEFT)
        self.total_time_label = Label(self.time_frame, textvariable=self.total_time_var, bd=0)
        self.total_time_label.pack(side=RIGHT)
        self.time_frame.pack(fill='x')

        self.style = Style()
        self.seek_var = IntVar()
        self.seek_scale = ttk.Scale(self.master, from_=0, to=100, style='info.Horizontal.TScale', variable=self.seek_var, command=self.seek_song)
        self.seek_scale.pack(fill='x')

        self.volume_var = IntVar()
        self.volume_label_var = StringVar()
        self.volume_label_var.set('100%')
        self.volume_var.set(100)

        self.bottom_frame = Frame(self.master)
        self.bottom_frame.pack(side=BOTTOM, fill='x')
        self.buttons_attributes = {'bd': '0', 'bg': 'white', 'activebackground': 'white', 'takefocus': False}

        self.buttons_frame = Frame(self.bottom_frame)
        self.play_button = Button(self.buttons_frame, image=self.play_image, **self.buttons_attributes, command=self.play_or_pause_music)
        self.play_button.pack(side=LEFT)
        self.previous_button = Button(self.buttons_frame, image=self.previous_image, **self.buttons_attributes, command=lambda: self.prev_next_song(button_name='prev'))
        self.previous_button.pack(side=LEFT, padx=2, ipady=5)
        self.stop_button = Button(self.buttons_frame, image=self.stop_image, **self.buttons_attributes, command=self.stop)
        self.stop_button.pack(side=LEFT)
        self.next_button = Button(self.buttons_frame, image=self.next_image, **self.buttons_attributes, command=self.prev_next_song)
        self.next_button.pack(side=LEFT, padx=2)
        self.buttons_frame.pack(side=LEFT)

        self.volume_frame = Frame(self.bottom_frame)
        self.mute_unmute_button = Button(self.volume_frame, image=self.unmute_image, **self.buttons_attributes, command=self.mute_unmute_volume)
        self.mute_unmute_button.pack(side=LEFT)
        self.volume_slider = ttk.Scale(self.volume_frame, from_=0, to=100, variable=self.volume_var, style='success.Horizontal.TScale', takefocus=False, command=self.change_volume)
        self.volume_slider.pack(side=LEFT)
        self.volume_label = Label(self.volume_frame, textvariable=self.volume_label_var, width=4, font=font.Font(weight='bold'))
        self.volume_label.pack(side=LEFT)
        self.volume_frame.pack(side=RIGHT)

        self.initial_position()

        self.master.bind('<space>', self.space_bind)
        self.master.bind('<Return>', self.return_bind)
        self.master.bind('<Control-o>', self.open_files)
        self.master.bind('<Control-O>', self.open_files)
        self.master.bind('<m>', self.mute_unmute_volume)
        self.master.bind('<M>', self.mute_unmute_volume)
        self.master.bind('<Up>', self.up_down_direction)
        self.master.bind('<Down>', self.up_down_direction)
        self.master.bind('<Control-p>', self.get_playlist)
        self.master.bind('<Delete>', self.remove_from_list)
        self.master.bind('<Control-P>', self.save_playlists)
        self.audio_list.bind('<Button-3>', self.right_click)
        self.audio_list.bind('<Button-1>', self.single_click)
        self.audio_list.bind('<Double-Button-1>', self.double_click)
        self.master.bind('<Control-q>', lambda e: self.master.destroy())
        self.master.bind('<Control-Q>', lambda e: self.master.destroy())
        self.total_time_label.bind('<Button-1>', self.show_remaining_time)
        self.audio_list.bind('<Shift-Button-1>', self.shift_multiple_selection)
        self.master.bind('<n>', lambda event: self.prev_next_song(event, 'next'))
        self.master.bind('<N>', lambda event: self.prev_next_song(event, 'next'))
        self.master.bind('<p>', lambda event: self.prev_next_song(event, 'prev'))
        self.master.bind('<P>', lambda event: self.prev_next_song(event, 'prev'))
        self.audio_list.bind('<Control-Button-1>', self.multiple_selection_one_by_one)
        self.master.bind('<Control-a>', lambda e: self.audio_list.selection_set(0, 'end'))
        self.master.bind('<Control-A>', lambda e: self.audio_list.selection_set(0, 'end'))
        self.master.bind('<Control-Right>', lambda event: self.seek_song(event, 'forward'))
        self.master.bind('<Control-Left>', lambda event: self.seek_song(event, 'backward'))
        self.master.bind('<Left>', lambda event, change='decrease': self.change_volume(event, change))
        self.master.bind('<Right>', lambda event, change='increase': self.change_volume(event, change))
        self.audio_list.bind('<Left>', lambda event, change='decrease': self.change_volume(event, change))
        self.audio_list.bind('<Right>', lambda event, change='increase': self.change_volume(event, change))
        self.seek_scale.bind('<Button-1>', lambda event: self.SeekSingleClick(event, self.seek_scale, self.seek_song))
        self.volume_slider.bind('<Button-1>', lambda event: self.SeekSingleClick(event, self.volume_slider, self.change_volume, True))

        self.master.mainloop()

    def initial_position(self):
        '''Set window position to the center when program starts first time'''

        self.master.update()
        self.master.resizable(0, 0)

        width = self.master.winfo_width() // 2
        height = self.master.winfo_height() // 2
        screen_width = self.master.winfo_screenwidth() // 2
        screen_height = self.master.winfo_screenheight() // 2

        self.master.geometry(f'+{screen_width - width}+{screen_height - height}')
        self.master.deiconify()

    def clicked_at_empty_space(self, event=None):
        '''Check if user has clicked in empty space'''

        abs_coord_y = self.master.winfo_pointery() - self.master.winfo_rooty()

        last_index = len(self.audio_list.get(0, 'end')) - 1
        bbox = self.audio_list.bbox(last_index)

        if bbox:
            return abs_coord_y > bbox[1] + bbox[-1]

    def SeekSingleClick(self, event, widget, function, seek=False):
        '''Hijacking Single Left Click to work like Single Right Click
           to change the value of Scale to the position it is clicked

           Setting seek parameter to True activates audio_slider but
           not seek_scale when there is no audio in audio_list'''

        if self.previous_volume and seek:  # Unmuting sound when user clicks anywhere in volume slider
            self.mute_unmute_volume()

        if self.variable.get() or seek:
            widget.event_generate('<Button-3>', x=event.x, y=event.y)
            function()

        return 'break'

    def single_click(self, event=None):
        '''When user single left clicks'''

        if not self.files:
            # If there is no songs played yet but user left clicks
            # then make single left click event as double left click

            self.open_files()
            return 'break'

        if self.clicked_at_empty_space():
            return 'break'

        if self.audio_list.itemcget(self.audio_list.nearest(event.y), 'bg') == 'grey':
            self.audio_list.select_clear(0, 'end')
            self.select_index = self.audio_list.nearest(event.y)
            return 'break'

        self.audio_list.selection_clear(0, 'end')
        self.select_index = self.audio_list.nearest(event.y)

    def double_click(self, event=None):
        '''When user right clicks'''

        if self.clicked_at_empty_space():
            # When some files are opened and user double clicks
            # on the empty spaces then open file_dialog to open additional audio files
            self.open_files()

        else:
            # Play the selected song when user double clicks on it
            self.is_playing = None
            self.audio_list.selection_set(self.select_index)

            if self.current_playing_index > -1:
                self.audio_list.itemconfig(self.current_playing_index, bg='white', fg='purple')

            self.play_or_pause_music()

    def open_files(self, event=None, files=None):
        '''Open dialog box to select audio files'''

        if files is None:
            files = filedialog.askopenfilenames(filetypes=self.extensions, initialdir=os.getcwd(), defaultextension=self.extensions)

        if files:
            self.files.update({os.path.basename(f): f for f in files})
            self.variable.set(list(self.files.keys()))

            if self.current_playing_index == -1:
                self.select_index = 0

            if self.is_playing is None and not self.audio_list.curselection():
                self.audio_list.selection_set(0)

            if len(self.files) == 1:  # Play audio if user opens only 1 audio file
                self.play_or_pause_music()

        return 'break'

    def return_bind(self, event=None):
        '''When user press Enter key'''

        curr_sel = self.audio_list.curselection()

        if curr_sel:
            curr_sel = curr_sel[0]

            if self.song_name != self.audio_list.get(curr_sel):
                self.is_playing = None

                if self.current_playing_index > -1:
                    self.audio_list.itemconfig(self.current_playing_index, bg='white', fg='purple')

        self.play_or_pause_music()

    def space_bind(self, event=None):
        '''When user presses SPACE key'''

        curr_index = self.audio_list.curselection()

        if curr_index:
            curr_index = curr_index[0]

            if curr_index != self.current_playing_index:
                self.is_playing = None
                self.audio_list.itemconfig(self.current_playing_index, bg='white', fg='purple')

        self.play_or_pause_music()

    def play_or_pause_music(self, event=None):
        '''Play or pause audio when play or pause button is pressed'''

        try:
            if self.is_playing is None:  # When any audio is not played before
                curr_sel = self.audio_list.curselection()

                if curr_sel:
                    curr_sel = curr_sel[0]

                else:
                    curr_sel = 0

                self.current_playing_index = self.select_index = curr_sel
                self.audio_list.selection_set(self.current_playing_index)
                self.audio_list.itemconfig(self.current_playing_index, bg='grey', fg='white')
                self.audio_list.selection_clear(0, 'end')
                self.song_name = self.audio_list.get(self.current_playing_index)
                self.current_song_path = self.files[self.song_name]

                self.is_playing = True  # Here, True represents that the music is being played.
                img = self.pause_image
                pygame.mixer.music.load(self.current_song_path)  # Loading selected file for playing
                pygame.mixer.music.play()  # Start playing loaded file

                self.total_time = MP3(self.current_song_path).info.length  # Getting audio length
                self.seek_scale.config(to=int(self.total_time))
                self.seek_var.set(0)
                self.audio_list.see(self.current_playing_index)  # Scrolling to currently playing audio
                self.total_time_var.set(time.strftime('%H:%M:%S', time.gmtime(self.total_time)))
                self.audio_list.selection_clear(0, 'end')

                if self.current_playing_index != len(self.files) - 1:
                    self.eof = False  # Here, setting self.eof to False means last song is not being played yet

                if self.scale_timer:
                    self.master.after_cancel(self.scale_timer)

                self.update_scale()

            elif self.is_playing is True:  # Pausing audio when another audio is playing
                pygame.mixer.music.pause()
                img = self.play_image
                self.is_playing = False
                self.master.after_cancel(self.scale_timer)

            elif self.is_playing is False:  # Resume playing audio from where the audio is paused
                self.is_playing = True
                img = self.pause_image
                pygame.mixer.music.play(start=self.seek_var.get())
                self.update_scale()

            self.play_button.config(image=img)

        except pygame.error:
            self.is_playing = None
            messagebox.showinfo('ERR', 'Audio format not supported')

        except TclError:  # when user tries to play audio when no audio was added before
            pass

    def stop(self, event=None):
        '''Stop playing audio'''

        if self.is_playing:
            pygame.mixer.music.stop()

            if self.scale_timer is not None:
                self.master.after_cancel(self.scale_timer)

            self.seek_var.set(0)
            self.is_playing = None
            self.audio_list.itemconfig(self.current_playing_index, fg='purple', bg='white')
            self.current_playing_index -= 1
            self.total_time_var.set('--:--')
            self.escaped_time_var.set('--:--')
            self.audio_list.selection_clear(0, 'end')
            self.play_button.config(image=self.play_image)

    def update_scale(self, event=None):
        '''Continuously update escaping time and slider values
           until songs comes to end'''

        self.current_pos = pygame.mixer.music.get_pos() / 1000

        if self.seek_var.get() > int(self.current_pos):
            self.current_pos = self.seek_var.get() + 1

        self.escaped_time_var.set(time.strftime('%H:%M:%S', time.gmtime(self.current_pos)))
        self.seek_var.set(int(self.current_pos))

        if int(self.current_pos) == int(self.total_time):  # Checking if audio has complete playing
            self.master.after_cancel(self.scale_timer)
            self.is_playing = None

            self.seek_var.set(0)
            self.total_time_var.set('--:--')
            self.escaped_time_var.set('--:--')
            self.prev_next_song(button_name='next')

            if self.current_playing_index == len(self.files) - 1:  # Checking if the last completed audio was the second last.
                if self.eof:
                    self.is_playing = None
                    self.audio_list.see(0)
                    self.audio_list.selection_clear(0, 'end')
                    self.audio_list.selection_set(0)
                    self.play_button.config(image=self.play_image)

                    self.showed_rem_time = False
                    self.master.after_cancel(self.rem_timer)

                self.eof = True  # Here, if self.eof is set True then it means that the second last audio has just completed playing

        else:
            self.scale_timer = self.master.after(1000, self.update_scale)

    def seek_song(self, event=None, direc=None):
        '''Skip song as the user moves the slider'''

        if self.is_playing is not None:
            skipped_at = self.seek_var.get()

            if direc == 'forward':
                skipped_at += 5

                if skipped_at >= self.total_time:
                    self.prev_next_song()
                    return

            elif direc == 'backward':
                skipped_at -= 5

                if skipped_at <= 0:
                    skipped_at = 0

            self.seek_var.set(skipped_at)

            if self.is_playing:
                pygame.mixer.music.play(start=skipped_at)

            self.escaped_time_var.set(time.strftime('%H:%M:%S', time.gmtime(skipped_at)))

    def prev_next_song(self, event=None, button_name=None):
        '''Play previous and present audio present in list-box'''

        try:
            if self.current_playing_index > -1:
                from_list_box = self.variable.get()

                if button_name == 'prev':  # If previous buttons is clicked
                    if self.current_playing_index == 0:
                        return

                    self.audio_list.itemconfig(self.current_playing_index, bg='white', fg='purple')
                    self.current_playing_index -= 1

                else:  # If next button is clicked
                    if self.current_playing_index == len(from_list_box) - 1:
                        return

                    self.audio_list.itemconfig(self.current_playing_index, bg='white', fg='purple')
                    self.current_playing_index += 1

                self.audio_list.selection_clear(0, 'end')
                self.audio_list.see(self.current_playing_index)
                self.audio_list.selection_set(self.current_playing_index)
                self.is_playing = None
                self.play_or_pause_music()

        except TclError:
            pass

    def get_playlist(self, event=None):
        '''Get audio path stored in a file'''

        try:
            with open(self.file_path, 'r') as f:
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

            self.open_files(files=files)

    def save_playlists(self, event=None):
        '''Save audio path present in list-box'''

        if self.variable.get():
            with open(self.file_path, 'w') as f:
                contents = {'playlists': self.files}
                json.dump(contents, f, indent=4)
                messagebox.showinfo('Saved!', 'Playlist Saved !!')

        else:
            messagebox.showinfo('ERR', 'No audio found to save in Playlist')

    def show_remaining_time(self, event=None):
        '''Show remaining time of current playing audio'''

        if self.is_playing is not None and self.current_playing_index > -1:
            if self.showed_rem_time is False:  # If remaining time has not been shown
                self.showed_rem_time = True
                self.change_time()

            else:  # Remaining time has already been show
                self.showed_rem_time = False
                self.master.after_cancel(self.rem_timer)
                self.total_time_var.set(time.strftime('%H:%M:%S', time.gmtime(self.total_time)))

    def change_time(self):
        '''Calculate remaining time of currently playing song'''

        gmtime = time.gmtime(self.total_time - self.current_pos)
        self.total_time_var.set(time.strftime('-%H:%M:%S', gmtime))
        self.rem_timer = self.master.after(500, self.change_time)

    def mute_unmute_volume(self, event=None):
        '''Mute and Unmute volume'''

        if self.previous_volume is None:  # Volume is not muted before
            self.previous_volume = int(self.volume_label_var.get()[:-1])
            self.mute_unmute_button.config(image=self.mute_image)
            self.volume_slider.config(state='disabled')
            self.volume_label_var.set('0%')
            pygame.mixer.music.set_volume(0)
            self.volume_var.set(0)

        else:  # Volume is muted before
            self.volume_slider.config(state='normal')
            self.volume_var.set(self.previous_volume)
            pygame.mixer.music.set_volume(self.previous_volume / 100)
            self.volume_label_var.set(f'{self.previous_volume}%')
            self.mute_unmute_button.config(image=self.unmute_image)
            self.previous_volume = None

    def change_volume(self, event=None, change=None):
        '''Increase or decrease volume when user drags volume bar or
           when user presses right arrow or left arrow
            Here volume value is between 0-1'''

        curr_vol = self.volume_var.get()

        if change == 'increase':
            curr_vol += 5

            if curr_vol >= 100:
                curr_vol = 100

        elif change == 'decrease':
            curr_vol -= 5

            if curr_vol <= 0:
                curr_vol = 0

        self.volume_var.set(curr_vol)
        curr_vol /= 100
        pygame.mixer.music.set_volume(curr_vol)
        self.volume_label_var.set(f'{int(curr_vol * 100)}%')

        return 'break'

    def right_click(self, event=None):
        '''When user right clicks inside list-box'''

        curr_sel = self.audio_list.curselection()
        right_click_menu = Menu(self.master, tearoff=False)

        if len(curr_sel) > 1:  # If multiple selection is done
            right_click_menu.add_command(label='Remove from list', command=self.remove_from_list)
            right_click_menu.add_command(label='Remove from playlist', command=self.remove_from_playlist)

        else:
            if self.variable.get():
                if self.clicked_at_empty_space():
                    self.audio_list.selection_clear(0, 'end')
                    right_click_menu.add_command(label='Open', command=self.open_files)

                else:
                    self.audio_list.selection_clear(0, 'end')
                    self.audio_list.selection_set(self.audio_list.nearest(event.y))
                    self.audio_list.activate(self.audio_list.nearest(event.y))
                    right_click_menu.add_command(label='Remove from list', command=self.remove_from_list)
                    right_click_menu.add_command(label='Remove from playlist', command=self.remove_from_playlist)

            else:
                right_click_menu.add_command(label='Open', command=self.open_files)
                right_click_menu.add_command(label='Open Playlist', command=self.get_playlist)

        try:
            right_click_menu.tk_popup(event.x_root, event.y_root)

        finally:
            right_click_menu.grab_release()

    def remove_from_list(self, event=None):
        '''Remove selected item from the list-box'''

        curr_indexs = self.audio_list.curselection()

        if curr_indexs:
            for idx, curr_index in enumerate(curr_indexs):
                curr_index -= idx

                if curr_index < 0:
                    curr_index = 0

                if curr_index == self.current_playing_index:
                    self.stop()

                song_name = self.audio_list.get(curr_index)
                self.files.pop(song_name)
                self.audio_list.delete(curr_index)

            if len(self.files) == 1:
                self.audio_list.selection_set(0)

            else:
                self.audio_list.selection_set(curr_index)

    def remove_from_playlist(self, event=None):
        '''Remove selected item from the list-box as well from the playlist file'''

        self.remove_from_list()
        self.save_playlists()

    def up_down_direction(self, event=None):
        '''When user presses up or down arrow'''

        direc = event.keysym

        if self.files:
            curr_index = self.audio_list.curselection()

            if curr_index:
                curr_index = curr_index[0]

            else:
                curr_index = self.select_index

            if direc == 'Up':
                if curr_index != 0:
                    curr_index -= 1

            else:
                if curr_index < len(self.files) - 1:
                    curr_index += 1

            self.audio_list.see(curr_index)
            self.audio_list.selection_clear(0, 'end')

            if self.audio_list.itemcget(curr_index, 'bg') != 'grey':
                self.audio_list.selection_set(curr_index)

    def multiple_selection_one_by_one(self, event=None):
        '''Select multiple items in list-box holding control key'''

        self.select_index = self.audio_list.nearest(event.y)

        if self.select_index in self.audio_list.curselection():
            self.audio_list.selection_clear(self.select_index)

        else:
            self.audio_list.selection_set(self.select_index)
            self.audio_list.activate(self.select_index)

    def shift_multiple_selection(self, event=None):
        '''Select multiple items in list-box holding shift key'''

        from_ = self.select_index
        to_ = self.audio_list.nearest(event.y)

        if from_ > to_:
            from_, to_ = to_, from_

        if not self.audio_list.curselection():
            self.audio_list.selection_clear(0, 'end')

        for idx in range(from_, to_ + 1):
            self.audio_list.selection_set(idx)

    def resource_path(self, file_name):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'included_files', file_name)


if __name__ == '__main__':
    Music_Player()
