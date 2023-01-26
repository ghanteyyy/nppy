import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import pygame
import pyperclip


class _Entry:
    def __init__(self, frame, font, style_name, default_text):
        self.font = font
        self.frame = frame
        self.IsDefault = True
        self.style_name = style_name
        self.default_text = default_text

        self.var = StringVar()
        self.var.set(self.default_text)

        self.Style = ttk.Style()
        self.Style.configure(self.style_name, foreground='grey')

        self.Entry = ttk.Entry(self.frame, textvariable=self.var, font=self.font, width=19, justify='center', style=self.style_name)

        self.Entry.bind('<FocusIn>', self.FocusIn)
        self.Entry.bind('<FocusOut>', self.FocusOut)

    def FocusIn(self, event=None):
        '''
        When focus changes to Entry widget(s)
        '''

        if self.IsDefault and self.var.get().strip() == self.default_text:
            self.IsDefault = False
            self.var.set('')
            self.Style.configure(self.style_name, foreground='black')

    def FocusOut(self, event=None):
        '''
        When focus changes out of Entry widget(s)
        '''

        if self.IsDefault is False and not self.var.get().strip():
            self.IsDefault = True
            self.var.set(self.default_text)
            self.Style.configure(self.style_name, foreground='grey')

    def SetToDefault(self):
        '''
        Set the default values to respective ttk.Entry when user finish adding,
        deleting or renaming values
        '''

        self.IsDefault = True

        self.var.set(self.default_text)
        self.Style.configure(self.style_name, foreground='grey')


class SSNI:
    def __init__(self):
        self.after_id = None
        self.AutoAddFile = os.path.abspath(os.path.join('.', 'AutoAdd.txt'))
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

        self.BackImage = PhotoImage(file=self.resource_path('back.png'))
        self.buttons_attributes = {'bd': 0, 'width': _width, 'bg': 'green', 'fg': 'white',
                                   'activebackground': 'green', 'activeforeground': 'white',
                                   'cursor': 'hand2'}

        self.LeftFrame = Frame(self.master)
        self.LeftFrame.pack(side=LEFT)
        self.RightFrame = Frame(self.master)
        self.RightFrame.pack(side=RIGHT, pady=5, anchor='w')

        self.FirstLeftFrame = Frame(self.LeftFrame)
        self.FirstLeftFrame.pack(side=LEFT)

        self.video_entry = _Entry(self.FirstLeftFrame, _font, 'VE.TEntry', 'Video Name')
        self.video_entry.Entry.pack(pady=10, padx=10, ipady=3)

        self.add_button = Button(self.FirstLeftFrame, text='A D D', **self.buttons_attributes, command=lambda: self.add_remove_search_command(button_name='ADD'))
        self.add_button.pack(pady=5, ipady=buttons_ipady)
        self.remove_button = Button(self.FirstLeftFrame, text='R E M O V E', **self.buttons_attributes, command=lambda: self.add_remove_search_command(button_name='REMOVE'))
        self.remove_button.pack(pady=5, ipady=buttons_ipady)
        self.search_button = Button(self.FirstLeftFrame, text='S E A R C H', **self.buttons_attributes, command=lambda: self.add_remove_search_command(button_name='SEARCH'))
        self.search_button.pack(pady=5, ipady=buttons_ipady)
        self.rename_window_button = Button(self.FirstLeftFrame, text='R E N A M E', **self.buttons_attributes, command=self.ShowRenamingWidgets)
        self.rename_window_button.pack(pady=5, ipady=buttons_ipady)
        self.auto_add_button = Button(self.FirstLeftFrame, text='A U T O   A D D', **self.buttons_attributes, command=self.AutoAdd)
        self.auto_add_button.pack(pady=5, ipady=buttons_ipady)

        self.ListBoxVariable = Variable()
        self.ListBox = Listbox(self.RightFrame, width=36, height=15, activestyle='none', listvariable=self.ListBoxVariable)
        self.scrollbar = ttk.Scrollbar(self.RightFrame, orient="vertical", command=self.ListBox.yview)
        self.ListBox.config(yscrollcommand=self.scrollbar.set)
        self.ListBox.pack(side=LEFT, ipady=1)
        self.scrollbar.pack(side=RIGHT, fill='y')

        self.SecondLeftFrame = Frame(self.LeftFrame)

        self.old_name_entry = _Entry(self.SecondLeftFrame,  _font, 'O.TEntry', 'Old Name')
        self.old_name_entry.Entry.pack(padx=10, ipady=3)

        self.new_name_entry = _Entry(self.SecondLeftFrame,  _font, 'N.TEntry', 'New Name')
        self.new_name_entry.Entry.pack(pady=10, padx=10, ipady=3)

        self.rename_button = Button(self.SecondLeftFrame, text='R E N A M E', **self.buttons_attributes, command=self.rename_command)
        self.rename_button.pack(ipady=buttons_ipady)
        self.back_button = Button(self.SecondLeftFrame, image=self.BackImage, bd=0, cursor='hand2', activebackground=back_active_bg, command=self.back_command)
        self.back_button.pack(ipady=buttons_ipady)

        self.master.bind('<F5>', self.InsertToListBox)
        self.ListBox.bind('<Button-3>', self.RightClick)
        self.master.bind('<Button-1>', self.key_bindings)
        self.back_button.bind('<Return>', self.back_command)
        self.rename_button.bind('<Return>', self.rename_command)
        self.video_entry.Entry.bind('<Button-3>', self.RightClick)
        self.master.bind_class('Button', '<FocusIn>', lambda event, focus_out=True: self.key_bindings(event, focus_out))

        self.master.after(0, self.center_window)
        self.master.after(0, self.InsertToListBox)

        self.master.mainloop()

    def center_window(self):
        '''
        Set initial position of the window to the center of the screen
        '''

        self.master.update()
        self.master.resizable(0, 0)

        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.master.geometry(f'+{screen_width - width // 2}+{screen_height - height // 2}')

        self.master.deiconify()

        if os.path.exists(self.AutoAddFile) is False:
            self.CreateAutoAddFile()

    def key_bindings(self, event, focus_out=False):
        '''
        When user clicks in and out of the entry boxes
        '''

        event.widget.focus()

    def ShowRenamingWidgets(self, event=None):
        '''
        Show the renaming widgets to rename old name with new name
        '''

        self.FirstLeftFrame.pack_forget()
        self.SecondLeftFrame.pack(side=LEFT)

    def back_command(self, event=None):
        '''
        When user clicks back button
        '''

        self.SecondLeftFrame.pack_forget()
        self.FirstLeftFrame.pack(side=LEFT)

    def read_file(self):
        '''
        Getting everything from file
        '''

        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                return [line.strip('\n') for line in f.readlines()]

        return []

    def write_to_file(self, contents):
        '''
        Writing new or renamed data to the file
        '''

        with open(self.file_name, 'w') as f:
            for content in contents:
                f.write(f'{content}\n')

    def InsertToListBox(self, event=None, contents=None, remove=False):
        '''
        Insert contents of file in Text widget
        '''

        if contents is None:
            contents = self.read_file()

        if contents:
            contents.sort(key=len)

            if self.ListBoxVariable.get() and self.ListBoxVariable.get()[0] == 'No data yet':
                self.ListBox.itemconfig(0, foreground='black')

            if remove is False:
                self.ListBoxVariable.set(contents)

            else:
                # When user removes any value then the deleted value gets selected by
                # red color first and then after 800ms, the value in the ListBox gets
                # deleted. When doing so the ListBox scrolls back to the top(its
                # default behavior). To avoid this default scrolling remove parameter
                # removes the respective value without scrolling to the top.

                index = self.ListBox.get(0, END).index(remove)
                self.ListBox.delete(index)

            self.write_to_file(contents)

        else:
            # When there is no value in text files

            self.ListBoxVariable.set(['No data yet'])
            self.ListBox.itemconfig(0, foreground='grey')

    def add_remove_search_command(self, button_name, from_listbox=None):
        '''
        Commands when user clicks either ADD, REMOVE or SEARCH buttons
        '''

        contents = self.read_file()

        if from_listbox is None:
            from_entry = self.video_entry.var.get().strip()

        else:
            from_entry = self.ListBox.selection_get()

        if from_entry == 'Video Name':
            pygame.mixer.music.play()

        elif button_name == 'ADD':
            if from_entry in contents:
                self.highlight(from_entry, '#e8cb10')

            else:
                contents.append(from_entry)

                self.InsertToListBox(contents=contents)
                self.highlight(from_entry, 'green')

        elif button_name == 'REMOVE':
            if from_entry in contents:
                self.ListBox.selection_clear(0, END)
                contents.remove(from_entry)

                self.highlight(from_entry, 'red')
                self.master.after(800, lambda: self.InsertToListBox(contents=contents, remove=from_entry))

            else:
                pygame.mixer.music.play()

        elif button_name == 'SEARCH':
            if from_entry in contents:
                self.highlight(from_entry, '#3ccbde')

            else:
                pygame.mixer.music.play()

        self.video_entry.SetToDefault()

    def rename_command(self, event=None):
        '''
        Commands when user clicks RENAME button
        '''

        contents = self.read_file()
        old_name = self.old_name_entry.var.get().strip()
        new_name = self.new_name_entry.var.get().strip()

        if old_name == 'Old Name' or new_name == 'New Name' or old_name not in contents or new_name in contents:
            pygame.mixer.music.play()

        else:
            old_name_index = contents.index(old_name)
            contents[old_name_index] = new_name

            self.InsertToListBox(contents=contents)

            for widget in [self.old_name_entry, self.new_name_entry]:
                widget.SetToDefault()

            self.master.focus()
            self.highlight(new_name, '#45bf7c')

    def CreateAutoAddFile(self):
        '''
        Create "AutoAdd.txt" file when needed
        '''

        with open(self.AutoAddFile, 'w'):
            pass

    def AutoAdd(self):
        '''
        When user clicks "Auto Add" button
        '''

        confirm = messagebox.askokcancel('Info', 'To add values automatically, you need to store those values in text file "AutoAdd.txt".\n\nNote: Each value must be in separate lines\n\nWant to Proceed?')

        if confirm:
            with open(self.AutoAddFile, 'r') as rf:
                lines = rf.readlines()

                for line in lines:
                    _line = line.strip('\n')

                    self.video_entry.Entry.focus()
                    self.video_entry.var.set(_line)

                    self.add_button.focus()
                    self.add_button.invoke()

                    idx = self.ListBox.get(0, END).index(_line)
                    self.SetListBoToDefault(idx)

            delete = messagebox.askyesno('Info ?', 'Auto-Add completed\n\nDo you want to clear the contents of Auto-Add.txt')

            if delete:
                with open(self.AutoAddFile, 'w'):
                    pass

    def highlight(self, value, color):
        '''
        Fill color when value is added, removed and searched
        '''

        index = self.ListBox.get(0, END).index(value)
        self.ListBox.see(index)

        self.ListBox.itemconfig(index, background=color, foreground='white')

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.after_id = self.master.after(800, lambda: self.SetListBoToDefault(index))

    def SetListBoToDefault(self, index):
        '''
        Set highlighted value in listbox to default
        '''

        self.ListBox.itemconfig(index, background='white', foreground='black')

    def copy_cut(self, cut=False, from_listbox=False):
        '''
        Command for copying and cutting selected text of entry widget
        '''

        if self.video_entry.Entry.selection_present():
            text = self.video_entry.var.get()

            if cut:
                # When user clicks to the cut option of right-click
                # menu then deleting the text inside of the selection

                self.video_entry.Entry.delete('sel.first', 'sel.last')

        elif from_listbox is True:
            text = self.ListBox.selection_get()

        pyperclip.copy(text)  # Copying selected text to clipboard

    def paste(self):
        '''
        Command for pasting text from system clipboard to the position of
        cursor in entry widget
        '''

        clipboard = pyperclip.paste()

        if self.video_entry.Entry.select_present():
            self.video_entry.Entry.delete('sel.first', 'sel.last')  # Removing the selected text of entry widget

        cur_pos = self.video_entry.Entry.index(INSERT)
        self.video_entry.Entry.insert(cur_pos, clipboard)

    def RightClick(self, event=None):
        '''
        When user right clicks inside list-box
        '''

        x, y = self.master.winfo_pointerxy()
        widget = self.master.winfo_containing(x, y)
        RightClickMenu = Menu(self.master, tearoff=False)

        if widget == self.video_entry.Entry:
            RightClickMenu.add_command(label='Copy', command=self.copy_cut)
            RightClickMenu.add_command(label='Cut', command=lambda: self.copy_cut(cut=True))
            RightClickMenu.add_command(label='Paste', command=self.paste)

            if not pyperclip.paste():
                # When there is no text in clipboard then disabling paste options in
                # right-click menu

                RightClickMenu.entryconfig(2, state='disabled')

            if widget.select_present() is False:
                # When there is no selection in entry widget then disabling copy and
                # cut options in right-click menu

                RightClickMenu.entryconfig(0, state='disabled')
                RightClickMenu.entryconfig(1, state='disabled')

                if self.master.focus_get() != widget:
                    # When the cursor is over the entry widget and user right clicks to
                    # entry widget then generating left click event to set focus to entry
                    # widget before showing pop-up menu

                    widget.event_generate('<Button-1>')

        elif widget == self.ListBox:
            _y = event.y
            nearest = self.ListBox.nearest(_y)  # Getting index nearest to the cursor
            bbox = self.ListBox.bbox(nearest)   # Getting the x, y, width and height of value of the obtained nearest index
            from_listbox = self.ListBoxVariable.get()

            if (from_listbox and from_listbox[0] == 'No data yet') or (nearest == 0 and _y > bbox[-1]):  # When there is no data in Listbox
                RightClickMenu.add_command(label='Load from file', command=self.InsertToListBox)

            else:
                self.ListBox.event_generate('<Button-1>')

                # Removing previous selection
                self.ListBox.select_clear(0, END)

                # Selecting the obtained nearest index
                self.ListBox.selection_set(nearest)

                RightClickMenu.add_command(label='Copy', command=lambda: self.copy_cut(from_listbox=True))
                RightClickMenu.add_command(label='Remove', command=lambda: self.add_remove_search_command('REMOVE', from_listbox=True))

        try:
            RightClickMenu.tk_popup(event.x_root, event.y_root)

        finally:
            RightClickMenu.grab_release()

    def resource_path(self, file_name):
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

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    SSNI()
