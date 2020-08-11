import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Scrollbar


class SSNI:
    def __init__(self):
        self.file_name = 'video_file.txt'

        self.master = Tk()
        self.master.withdraw()
        self.master.title('SSNI')
        self.master.iconbitmap(self.resource_path('included_files\\icon.ico'))

        self.first_left_frame = Frame(self.master)

        self.video_entry = Entry(self.first_left_frame, fg='grey', font=('Courier', 12), width=19, justify='center', highlightthickness=2, highlightbackground='grey')
        self.video_entry.insert(END, 'Video Name')
        self.video_entry.pack(pady=10, padx=10, ipady=3)

        self.add_button = Button(self.first_left_frame, text='ADD', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.add_remove_search_command(button_name='ADD'))
        self.add_button.pack(pady=5, ipady=3, ipadx=80)

        self.remove_button = Button(self.first_left_frame, text='REMOVE', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.add_remove_search_command(button_name='REMOVE'))
        self.remove_button.pack(pady=5, ipady=3, ipadx=70)

        self.search_button = Button(self.first_left_frame, text='SEARCH', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.add_remove_search_command(button_name='SEARCH'))
        self.search_button.pack(pady=5, ipady=3, ipadx=70)

        self.rename_window_button = Button(self.first_left_frame, text='RENAME', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=self.rename_window)
        self.rename_window_button.pack(pady=5, ipady=3, ipadx=69)

        self.first_left_frame.pack(padx=5, side=LEFT, ipady=2)

        self.text_area_frame = Frame(self.master)

        self.text_area = Text(self.text_area_frame, width=27, height=13, state=DISABLED, cursor='arrow')
        self.scrollbar = Scrollbar(self.text_area_frame, orient="vertical", command=self.text_area.yview)

        self.text_area.pack(side=LEFT, ipady=1)
        self.text_area_frame.pack(pady=5, padx=4, anchor='w')

        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', END)
        self.text_area_frame.pack(padx=5, pady=5, side=LEFT)

        self.rename_window_button.bind('<Return>', lambda e: self.rename_window())
        self.add_button.bind('<Return>', lambda e: self.add_remove_search_command(button_name='ADD'))
        self.remove_button.bind('<Return>', lambda e: self.add_remove_search_command(button_name='REMOVE'))
        self.search_button.bind('<Return>', lambda e: self.add_remove_search_command(button_name='SEARCH'))

        # Rename_window widgets
        self.rename_window_frame = Frame(self.master)

        self.old_name_entry = Entry(self.rename_window_frame, fg='grey', font=('Courier', 12), width=19, justify='center', highlightthickness=2, highlightbackground='grey')
        self.old_name_entry.insert(END, 'Old Name')

        self.new_name_entry = Entry(self.rename_window_frame, fg='grey', font=('Courier', 12), width=19, justify='center', highlightthickness=2, highlightbackground='grey')
        self.new_name_entry.insert(END, 'New Name')

        self.rename_button = Button(self.rename_window_frame, text='RENAME', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=self.rename_command)
        self.back_button = Button(self.rename_window_frame, text='BACK', bd=0, fg='blue', font=('Courier', 15, 'bold'), cursor='hand2', command=self.back_command, activeforeground='blue')

        self.master.bind('<Button-1>', self.key_bindings)
        self.back_button.bind('<Return>', self.back_command)
        self.video_entry.bind('<FocusIn>', self.key_bindings)
        self.old_name_entry.bind('<FocusIn>', self.key_bindings)
        self.new_name_entry.bind('<FocusIn>', self.key_bindings)
        self.rename_button.bind('<Return>', self.rename_command)

        self.master.after(0, self.center_window)
        self.master.after(0, self.insert_text_area)
        self.master.after(0, self.show_scrollbar)

        self.master.bind_class('Button', '<FocusIn>', lambda event, focus_out=True: self.key_bindings(event, focus_out))
        self.master.mainloop()

    def center_window(self):
        '''Set initial position of the window to the center of the screen'''

        self.master.update()
        self.master.resizable(0, 0)

        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

        self.master.deiconify()

    def key_bindings(self, event, focus_out=False):
        '''When user clicks in and out of the entry boxes'''

        widget = event.widget
        widgets = {self.video_entry: 'Video Name', self.old_name_entry: 'Old Name', self.new_name_entry: 'New Name'}

        if widget in widgets and widget.get().strip() == widgets[widget]:
            widget.delete(0, END)
            widget.config(fg='black')

            if widget == self.new_name_entry and not self.old_name_entry.get().strip():
                self.old_name_entry.delete(0, END)
                self.old_name_entry.config(fg='grey')
                self.old_name_entry.insert(END, widgets[self.old_name_entry])

        elif widget not in widgets or focus_out:
            for _widget in widgets:
                if not _widget.get().strip():
                    _widget.delete(0, END)
                    _widget.config(fg='grey')
                    _widget.insert(END, widgets[_widget])

        if widget in [self.master, self.rename_window_frame, self.first_left_frame]:
            self.master.focus()

    def rename_window(self):
        '''Rename window when user clicks rename button'''

        self.first_left_frame.pack_forget()
        self.text_area_frame.pack_forget()

        self.old_name_entry.pack(pady=10, padx=10, ipady=3)
        self.new_name_entry.pack(pady=10, padx=10, ipady=3)
        self.rename_button.pack(pady=15, ipady=3, ipadx=70)

        self.back_button.pack()

        self.rename_window_frame.pack(padx=5, side=LEFT, ipady=2)
        self.text_area_frame.pack(pady=5, padx=5, anchor='w')

    def back_command(self, event=None):
        '''Command when user clicks back button'''

        self.text_area_frame.pack_forget()
        self.rename_window_frame.pack_forget()

        self.first_left_frame.pack(padx=5, side=LEFT, ipady=2)
        self.text_area_frame.pack(pady=5, padx=5, anchor='w')

        self.back_button.pack_forget()

    def show_scrollbar(self):
        '''Show scrollbar when the character in the text is more than the height of the text widget'''

        if self.text_area.cget('height') < int(self.text_area.index('end-1c').split('.')[0]):
            self.scrollbar.pack(side=LEFT, fill='y')
            self.text_area.config(yscrollcommand=self.scrollbar.set)
            self.master.after(100, self.hide_scrollbar)

        else:
            self.master.after(100, self.show_scrollbar)

    def hide_scrollbar(self):
        '''Hide scrollbar when the character in the text is less than the height of the text widget'''

        if self.text_area.cget('height') >= int(self.text_area.index('end-1c').split('.')[0]):
            self.scrollbar.pack_forget()
            self.text_area.config(yscrollcommand=None)
            self.master.after(100, self.show_scrollbar)

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

    def add_remove_search_command(self, button_name):
        '''Commands when user clicks either ADD, REMOVE or SEARCH buttons'''

        contents = self.read_file()
        from_entry = self.video_entry.get().strip().title()

        if not from_entry or from_entry == 'Video Name':
            messagebox.showerror('Invalid Name', 'No Name given')

        elif button_name == 'ADD':
            if from_entry in contents:
                messagebox.showinfo('Already Exists', f'"{from_entry}" is already in file')

            else:
                contents.append(from_entry)
                messagebox.showinfo('Value Added', f'"{from_entry}" added in file')

        elif button_name == 'REMOVE':
            if from_entry in contents:
                contents.remove(from_entry)
                messagebox.showinfo('Value Removed', f'"{from_entry}" reomved from file')

            else:
                option = messagebox.askyesno('Add Value?', f'"{from_entry}" not in file. Do you want to add it?')

                if option:
                    contents.append(from_entry)

        elif button_name == 'SEARCH':
            if from_entry in contents:
                messagebox.showinfo('Exists', f'"{from_entry}" is in file')

            else:
                option = messagebox.askyesno('Add Value?', f'"{from_entry}" not in file. Do you want to add it?')

                if option:
                    contents.append(from_entry)

        self.video_entry.delete(0, END)
        self.video_entry.insert(END, 'Video Name')
        self.video_entry.config(fg='grey')

        self.insert_text_area(contents)
        self.master.focus()

    def rename_command(self, event=None):
        '''Commands when user clicks RENAME button'''

        contents = self.read_file()
        old_name = self.old_name_entry.get().strip()
        new_name = self.new_name_entry.get().strip().title()

        if old_name in ['', 'Old Name'] or new_name in ['', 'New Name']:
            messagebox.showerror('Invalid Video Name', 'The input video name is invlaid')

        elif old_name not in contents:
            messagebox.showerror('Not exists', 'Old Name Not found')

        elif new_name in contents:
            messagebox.showerror('Already Exists', 'New Name already exists in file. Try another!')

        else:
            old_name_index = contents.index(old_name)
            contents[old_name_index] = new_name

            self.insert_text_area(contents)

            for widget, text in {self.old_name_entry: 'Old Name', self.new_name_entry: 'New Name'}.items():
                widget.delete(0, END)
                widget.insert(END, text)
                widget.config(fg='grey')

            self.master.focus()
            messagebox.showinfo('Renamed', f'{old_name} renamed to {new_name}')

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS.

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    SSNI()
