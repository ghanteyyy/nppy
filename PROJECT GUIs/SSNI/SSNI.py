import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.ttk import Scrollbar


class SSNI:
    def __init__(self):
        self.after_id = None
        self.file_name = 'video_file.txt'

        self.master = Tk()
        self.master.withdraw()
        self.master.title('SSNI')
        self.master.iconbitmap(self.resource_path('included_files\\icon.ico'))

        self.first_left_frame = Frame(self.master)

        self.video_entry_style = ttk.Style()
        self.video_entry_style.configure('VE.TEntry', foreground='grey')
        self.video_entry = ttk.Entry(self.first_left_frame, font=('Courier', 12), width=19, justify='center', style='VE.TEntry')
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
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.text_area.pack(side=LEFT, ipady=1)
        self.scrollbar.pack(side=RIGHT, fill='y')
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

        self.old_name_entry_style = ttk.Style()
        self.old_name_entry_style.configure('O.TEntry', foreground='grey')
        self.old_name_entry = ttk.Entry(self.rename_window_frame, font=('Courier', 12), width=19, justify='center', style='O.TEntry')
        self.old_name_entry.insert(END, 'Old Name')

        self.new_name_entry_style = ttk.Style()
        self.new_name_entry_style.configure('N.TEntry', foreground='grey')
        self.new_name_entry = ttk.Entry(self.rename_window_frame, font=('Courier', 12), width=19, justify='center', style='N.TEntry')
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

        self.master.bind('<F5>', lambda e: self.insert_text_area())
        self.master.bind_class('Button', '<FocusIn>', lambda event, focus_out=True: self.key_bindings(event, focus_out))
        self.master.mainloop()

    def center_window(self):
        '''Set initial position of the window to the center of the screen'''

        self.master.update()
        self.master.resizable(0, 0)

        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2
        width, height = self.master.winfo_width(), self.master.winfo_height()
        self.master.geometry(f'{width}x{height}+{screen_width - width // 2}+{screen_height - height // 2}')

        self.widgets = {self.video_entry: ('Video Name', {self.video_entry_style: 'VE.TEntry'}), self.old_name_entry: ('Old Name', {self.old_name_entry_style: 'O.TEntry'}),
                        self.new_name_entry: ('New Name', {self.new_name_entry_style: 'N.TEntry'})}

        self.master.deiconify()

    def config_entry(self, widget, color, insert=False):
        '''Configure behaviour of entries widget when user clicks in or out of them'''

        widget.delete(0, END)
        key = list(self.widgets[widget][1].keys())[0]
        key.configure(self.widgets[widget][1][key], foreground=color)

        if insert:
            widget.insert(END, self.widgets[widget][0])

    def key_bindings(self, event, focus_out=False):
        '''When user clicks in and out of the entry boxes'''

        widget = event.widget

        if widget in self.widgets and widget.get().strip() == self.widgets[widget][0]:
            self.config_entry(widget, 'black')

            if widget == self.new_name_entry and not self.old_name_entry.get().strip():
                self.config_entry(self.old_name_entry, 'grey', True)

            if widget == self.old_name_entry and not self.new_name_entry.get().strip():
                self.config_entry(self.new_name_entry, 'grey', True)

        elif widget not in self.widgets or focus_out:
            for _widget in self.widgets:
                if not _widget.get().strip():
                    self.config_entry(_widget, 'grey', True)

        if widget in [self.master, self.rename_window_frame, self.first_left_frame]:
            self.master.focus()

    def rename_window(self):
        '''Rename window when user clicks rename button'''

        self.master.focus()
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

        success = False
        contents = self.read_file()
        from_entry = self.video_entry.get().strip()

        if not from_entry or from_entry == 'Video Name':
            messagebox.showerror('Invalid Name', 'No Name given')

        elif button_name == 'ADD':
            if from_entry in contents:
                self.highlight(from_entry, '#784da8')

            else:
                success = True

        elif button_name == 'REMOVE':
            if from_entry in contents:
                contents.remove(from_entry)
                self.highlight(from_entry, 'red')
                self.master.after(3000, lambda: self.insert_text_area(contents))

            else:
                option = messagebox.askyesno('Add Value?', f'"{from_entry}" not in file. Do you want to add it?')

                if option:
                    success = True

        else:
            if from_entry in contents:
                self.highlight(from_entry, '#784da8')

            else:
                option = messagebox.askyesno('Add Value?', f'"{from_entry}" not in file. Do you want to add it?')

                if option:
                    success = True

        if success:
            contents.append(from_entry)
            self.insert_text_area(contents)
            self.highlight(from_entry, 'green')

        self.config_entry(self.video_entry, 'grey', True)
        self.master.focus()

    def rename_command(self, event=None):
        '''Commands when user clicks RENAME button'''

        contents = self.read_file()
        old_name = self.old_name_entry.get().strip()
        new_name = self.new_name_entry.get().strip()

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

            for widget in [self.old_name_entry, self.new_name_entry]:
                self.config_entry(widget, 'grey', True)

            self.master.focus()
            self.highlight(new_name, '#ff006f')

    def highlight(self, value, color):
        '''Fill color when value is added, removed and searched'''

        line = self.text_area.search(value, '1.0', 'end')
        self.text_area.tag_add('highlight', line, f'{line.split(".")[0]}.end+1c')
        self.text_area.tag_config('highlight', background=color, foreground='white')
        self.text_area.see(f'{line}+2lines')

        if self.after_id:
            self.master.after_cancel(self.after_id)
            self.after_id = None

        self.after_id = self.master.after(3000, lambda: self.text_area.tag_delete('highlight'))

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
