import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter.ttk import Scrollbar
import pygame
import pyperclip


class SSNI:
    def __init__(self):
        self.after_id = None
        self.file_name = os.path.abspath(os.path.join('.', 'video_file.txt'))
        self.buttons_attributes = {'bd': 0, 'bg': 'green', 'fg': 'white', 'activebackground': 'green', 'activeforeground': 'white', 'cursor': 'hand2'}

        self.master = Tk()
        self.master.withdraw()
        self.master.title('SSNI')

        if sys.platform == 'win32':
            _width = 27
            buttons_ipady = 5
            _font = ('Courier', 12)
            back_active_bg = '#f0f0f0'
            self.master.iconbitmap(self.resource_path('icon.ico'))
            self.ErrorAudioFile = self.resource_path('WinErrSound.wav')

        else:
            _width = 21
            buttons_ipady = 3
            _font = ('Hack', 12)
            back_active_bg = '#d9d9d9'
            self.ErrorAudioFile = self.resource_path('LinuxErrSound.wav')
            self.IconImage = PhotoImage(file=self.resource_path('icon.png'))
            self.master.iconphoto(False, self.IconImage)

        pygame.init()
        pygame.mixer.music.load(self.ErrorAudioFile)

        self.BackImage = PhotoImage(file='included_files/back.png')
        self.buttons_attributes = {'bd': 0, 'width': _width, 'bg': 'green', 'fg': 'white',
                                   'activebackground': 'green', 'activeforeground': 'white',
                                   'cursor': 'hand2'}

        self.LeftFrame = Frame(self.master)
        self.LeftFrame.pack(side=LEFT)
        self.RightFrame = Frame(self.master)
        self.RightFrame.pack(side=RIGHT)

        self.FirstLeftFrame = Frame(self.LeftFrame)
        self.FirstLeftFrame.pack(side=LEFT)

        self.video_entry_style = ttk.Style()
        self.video_entry_style.configure('VE.TEntry', foreground='grey')
        self.video_entry = ttk.Entry(self.FirstLeftFrame, font=_font, width=19, justify='center', style='VE.TEntry')
        self.video_entry.insert(END, 'Video Name')
        self.video_entry.pack(pady=10, padx=10, ipady=3)

        self.add_button = Button(self.FirstLeftFrame, text='A D D', **self.buttons_attributes, command=lambda: self.add_remove_search_command(button_name='ADD'))
        self.add_button.pack(pady=5, ipady=buttons_ipady)
        self.remove_button = Button(self.FirstLeftFrame, text='R E M O V E', **self.buttons_attributes, command=lambda: self.add_remove_search_command(button_name='REMOVE'))
        self.remove_button.pack(pady=5, ipady=buttons_ipady)
        self.search_button = Button(self.FirstLeftFrame, text='S E A R C H', **self.buttons_attributes, command=lambda: self.add_remove_search_command(button_name='SEARCH'))
        self.search_button.pack(pady=5, ipady=buttons_ipady)
        self.rename_window_button = Button(self.FirstLeftFrame, text='R E N A M E', **self.buttons_attributes, command=self.ShowRenamingWidgets)
        self.rename_window_button.pack(pady=5, ipady=buttons_ipady)

        self.text_area = Text(self.RightFrame, width=27, height=13, state=DISABLED, cursor='arrow')
        self.scrollbar = Scrollbar(self.RightFrame, orient="vertical", command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.text_area.pack(side=LEFT, ipady=1)
        self.scrollbar.pack(side=RIGHT, fill='y')
        self.RightFrame.pack(pady=5, padx=4, anchor='w')

        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', END)
        self.RightFrame.pack(padx=5, pady=5, side=LEFT)

        self.SecondLeftFrame = Frame(self.LeftFrame)

        self.old_name_entry_style = ttk.Style()
        self.old_name_entry_style.configure('O.TEntry', foreground='grey')
        self.old_name_entry = ttk.Entry(self.SecondLeftFrame, font=_font, width=19, justify='center', style='O.TEntry')
        self.old_name_entry.insert(END, 'Old Name')
        self.old_name_entry.pack(padx=10, ipady=3)

        self.new_name_entry_style = ttk.Style()
        self.new_name_entry_style.configure('N.TEntry', foreground='grey')
        self.new_name_entry = ttk.Entry(self.SecondLeftFrame, font=_font, width=19, justify='center', style='N.TEntry')
        self.new_name_entry.insert(END, 'New Name')
        self.new_name_entry.pack(pady=10, padx=10, ipady=3)

        self.rename_button = Button(self.SecondLeftFrame, text='R E N A M E', **self.buttons_attributes, command=self.rename_command)
        self.rename_button.pack(ipady=buttons_ipady)
        self.back_button = Button(self.SecondLeftFrame, image=self.BackImage, bd=0, cursor='hand2', activebackground=back_active_bg, command=self.back_command)
        self.back_button.pack(ipady=buttons_ipady)

        self.master.bind('<Button-1>', self.key_bindings)
        self.back_button.bind('<Return>', self.back_command)
        self.video_entry.bind('<Button-3>', self.RightClick)
        self.video_entry.bind('<FocusIn>', self.key_bindings)
        self.old_name_entry.bind('<FocusIn>', self.key_bindings)
        self.new_name_entry.bind('<FocusIn>', self.key_bindings)
        self.rename_button.bind('<Return>', self.rename_command)

        self.master.after(0, self.center_window)
        self.master.after(0, self.insert_text_area)

        self.master.bind('<F5>', lambda e: self.insert_text_area())
        self.master.bind_class('Button', '<FocusIn>', lambda event, focus_out=True: self.key_bindings(event, focus_out))
        self.master.mainloop()

    def center_window(self):
        '''Set initial position of the window to the center of the screen'''

        self.master.update()
        self.master.resizable(0, 0)

        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.master.geometry(f'+{screen_width - width // 2}+{screen_height - height // 2}')

        self.widgets = {self.video_entry: ('Video Name', {self.video_entry_style: 'VE.TEntry'}), self.old_name_entry: ('Old Name', {self.old_name_entry_style: 'O.TEntry'}),
                        self.new_name_entry: ('New Name', {self.new_name_entry_style: 'N.TEntry'})}

        self.master.deiconify()

    def config_entry(self, widget, color, insert=True):
        '''Configure behavior of entries widget when user clicks in or out of them'''

        widget.delete(0, END)
        key = list(self.widgets[widget][1].keys())[0]
        key.configure(self.widgets[widget][1][key], foreground=color)

        if insert:
            widget.insert(END, self.widgets[widget][0])

    def key_bindings(self, event, focus_out=False):
        '''When user clicks in and out of the entry boxes'''

        widget = event.widget

        if widget in self.widgets and widget.get().strip() == self.widgets[widget][0]:
            self.config_entry(widget, 'black', False)

            if widget == self.new_name_entry and not self.old_name_entry.get().strip():
                self.config_entry(self.old_name_entry, 'grey')

            if widget == self.old_name_entry and not self.new_name_entry.get().strip():
                self.config_entry(self.new_name_entry, 'grey')

        elif widget not in self.widgets or focus_out:
            for _widget in self.widgets:
                if not _widget.get().strip():
                    self.config_entry(_widget, 'grey')

        if widget in [self.master, self.SecondLeftFrame, self.FirstLeftFrame, self.scrollbar]:
            self.master.focus()

    def ShowRenamingWidgets(self, event=None):
        '''Show the renaming widgets to rename old name with new name'''

        self.FirstLeftFrame.pack_forget()
        self.SecondLeftFrame.pack(side=LEFT)

    def back_command(self, event=None):
        '''When user clicks back button'''

        self.SecondLeftFrame.pack_forget()
        self.FirstLeftFrame.pack(side=LEFT)

    def read_file(self):
        '''Getting everything from file'''

        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                return [line.strip('\n') for line in f.readlines()]

        return []

    def write_to_file(self, contents):
        '''Writting new or renamed data to the file'''

        contents.sort(key=len)

        with open(self.file_name, 'w') as f:
            for content in contents:
                f.write(f'{content}\n')

        return contents

    def insert_text_area(self, contents=None):
        '''Insert contents of file in Text widget'''

        if contents is not None:
            contents = self.write_to_file(contents)

        else:
            contents = self.read_file()

        self.text_area.config(state=NORMAL)

        if contents:
            self.text_area.delete('1.0', END)
            self.text_area.config(fg='black')

            for index, content in enumerate(contents):
                if index == 0:
                    self.text_area.insert(END, content)

                else:
                    self.text_area.insert(END, '\n' + content)

        else:
            self.text_area.delete('1.0', END)
            self.text_area.config(fg='grey')
            self.text_area.insert('1.0', 'No data yet.')

        self.text_area.config(state=DISABLED)

        try:
            self.text_area.yview(self.line)
            self.line = None

        except (AttributeError, TclError):
            pass

    def add_remove_search_command(self, button_name):
        '''Commands when user clicks either ADD, REMOVE or SEARCH buttons'''

        success = False
        contents = self.read_file()
        from_entry = self.video_entry.get().strip()

        if from_entry == 'Video Name':
            pygame.mixer.music.play()

        elif button_name == 'ADD':
            if from_entry in contents:
                self.highlight(from_entry, '#e8cb10')
                self.config_entry(self.video_entry, 'grey')

            else:
                success = True

        elif button_name == 'REMOVE':
            if from_entry in contents:
                self.master.focus()
                contents.remove(from_entry)
                self.highlight(from_entry, 'red')
                self.config_entry(self.video_entry, 'grey')
                self.master.after(800, lambda: self.insert_text_area(contents))

            else:
                pygame.mixer.music.play()

        else:
            if from_entry in contents:
                self.master.focus()
                self.highlight(from_entry, '#3ccbde')
                self.config_entry(self.video_entry, 'grey')

            else:
                pygame.mixer.music.play()

        if success:
            contents.append(from_entry)
            self.insert_text_area(contents)
            self.highlight(from_entry, 'green')

            self.config_entry(self.video_entry, 'grey')
            self.master.focus()

    def rename_command(self, event=None):
        '''Commands when user clicks RENAME button'''

        contents = self.read_file()
        old_name = self.old_name_entry.get().strip()
        new_name = self.new_name_entry.get().strip()

        if old_name == 'Old Name' or new_name == 'New Name' or old_name not in contents or new_name in contents:
            pygame.mixer.music.play()

        else:
            old_name_index = contents.index(old_name)
            contents[old_name_index] = new_name

            self.insert_text_area(contents)

            for widget in [self.old_name_entry, self.new_name_entry]:
                self.config_entry(widget, 'grey')

            self.master.focus()
            self.highlight(new_name, '#45bf7c')

    def highlight(self, value, color):
        '''Fill color when value is added, removed and searched'''

        self.line = self.text_area.search(value, '1.0', 'end')
        self.text_area.tag_add('highlight', self.line, f'{self.line.split(".")[0]}.end+1c')
        self.text_area.tag_config('highlight', background=color, foreground='white')
        self.text_area.yview(self.line)

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.after_id = self.master.after(800, lambda: self.text_area.tag_delete('highlight'))

    def copy_cut(self, cut=False):
        '''Command for copying and cutting selected text of entry widget'''

        if self.video_entry.selection_present():
            text = self.video_entry.get()
            pyperclip.copy(text)  # Copying selected text to clipboard

            if cut:
                # When user clicks to the cut option of right-click
                # menu then deleting the text inside of the selection

                self.video_entry.delete('sel.first', 'sel.last')

    def paste(self):
        '''Command for pasting text from system clipboard to the position
           of cursor in entry widget'''

        clipboard = pyperclip.paste()

        if self.video_entry.select_present():
            self.video_entry.delete('sel.first', 'sel.last')  # Removing the selected text of entry widget

        cur_pos = self.video_entry.index(INSERT)
        self.video_entry.insert(cur_pos, clipboard)

    def RightClick(self, event=None):
        '''When user right clicks inside list-box'''

        RightClickMenu = Menu(self.master, tearoff=False)

        RightClickMenu.add_command(label='Copy', command=self.copy_cut)
        RightClickMenu.add_command(label='Cut', command=lambda: self.copy_cut(cut=True))
        RightClickMenu.add_command(label='Paste', command=self.paste)

        if not pyperclip.paste():
            # When there is no text in clipboard then
            # disabling paste options in right-click menu

            RightClickMenu.entryconfig(2, state='disabled')

        if self.video_entry.select_present() is False:
            # When there is no selection in entry widget then
            # disabling copy and cut options in right-click menu

            RightClickMenu.entryconfig(0, state='disabled')
            RightClickMenu.entryconfig(1, state='disabled')

            if self.master.focus_get() != self.video_entry:
                # When the cursor is over the entry widget and
                # user right clicks to entry widget then generating
                # left click event to set focus to entry widget
                # before showing pop-up menu

                self.video_entry.event_generate('<Button-1>')

        try:
            RightClickMenu.tk_popup(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

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
    SSNI()
