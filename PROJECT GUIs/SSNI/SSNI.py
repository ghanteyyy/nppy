import os
import sys

try:
    from tkinter import *
    from tkinter import messagebox
    from tkinter.ttk import Scrollbar

except (ImportError, ModuleNotFoundError):
    from Tkinter import *
    import tkMessageBox as messagebox
    from ttk import Scrollbar


class SSNI:
    def __init__(self):
        self.file_name = 'video_file.txt'

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.resizable(0, 0)
        self.master.title('SSNI')
        self.master.iconbitmap(self.resource_path('included_files\\icon.ico'))

        self.width, self.height = 475, 280
        self.screen_width, self.screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width // 2 - self.width // 2}+{self.screen_height // 2 - self.height // 2}')

        self.title_label = Label(self.master, text='SSNI', fg='white', bg='black', font=('Courier', 20))
        self.title_label.pack(fill='x')

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
        self.show_scrollbar()

        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', END)
        self.text_area_frame.pack(padx=5, pady=5, side=LEFT)

        self.master.after(0, self.insert_text_area)

        self.rename_window_button.bind('<Return>', lambda e: self.rename_window())
        self.add_button.bind('<Return>', lambda e: self.add_remove_search_command(button_name='ADD'))
        self.remove_button.bind('<Return>', lambda e: self.add_remove_search_command(button_name='REMOVE'))
        self.search_button.bind('<Return>', lambda e: self.add_remove_search_command(button_name='SEARCH'))
        self.video_entry.bind('<Button-1>', lambda event, widgets=[self.video_entry], texts=['Video Name']: self.widgets_bindings(event, widgets, texts))
        self.video_entry.bind('<FocusIn>', lambda event, widgets=[self.video_entry], texts=['Video Name']: self.widgets_bindings(event, widgets, texts))
        self.video_entry.bind('<FocusOut>', lambda event, widgets=[self.video_entry, self.video_entry], texts=['Video Name', 'Video Name']: self.widgets_bindings(event, widgets, texts))

        self.master.bind('<Button-1>', lambda event, widgets=[self.first_left_frame], entries=[self.video_entry], texts=['Video Name']: self.master_bindings(event, widgets, entries, texts))
        self.master.mainloop()

    def widgets_bindings(self, event, widgets, texts):
        '''When user clicks or select using tab from keyboard'''

        if event.widget == widgets[0] and widgets[0].get().strip() == texts[0]:
            widgets[0].delete(0, END)
            widgets[0].config(fg='black')

        if len(widgets) == 2 and not widgets[1].get().strip():
            widgets[1].delete(0, END)
            widgets[1].insert(END, texts[1])
            widgets[1].config(fg='grey')

    def master_bindings(self, event, widgets, enteries, texts):
        '''When user clicks to any frames or to the root window'''

        widgets.extend([self.title_label, self.text_area, self.scrollbar, self.master])

        if event.widget in widgets:
            for index, entry in enumerate(enteries):
                if not entry.get().strip():
                    entry.delete(0, END)
                    entry.insert(END, texts[index])
                    entry.config(fg='grey')

            self.master.focus()

    def rename_window(self):
        '''When user clicks rename button'''

        self.first_left_frame.pack_forget()
        self.text_area_frame.pack_forget()

        frame = Frame(self.master)

        self.old_name_entry = Entry(frame, fg='grey', font=('Courier', 12), width=19, justify='center', highlightthickness=2, highlightbackground='grey')
        self.old_name_entry.insert(END, 'Old Name')
        self.old_name_entry.pack(pady=10, padx=10, ipady=3)

        self.new_name_entry = Entry(frame, fg='grey', font=('Courier', 12), width=19, justify='center', highlightthickness=2, highlightbackground='grey')
        self.new_name_entry.insert(END, 'New Name')
        self.new_name_entry.pack(pady=10, padx=10, ipady=3)

        self.rename_button = Button(frame, text='RENAME', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=self.rename_command)
        self.rename_button.pack(pady=15, ipady=3, ipadx=70)

        back_button = Button(frame, text='BACK', bd=0, fg='blue', font=('Courier', 15, 'bold'), cursor='hand2', command=lambda: self.back_command(frame), activeforeground='blue')
        back_button.pack()

        frame.pack(padx=5, side=LEFT, ipady=2)
        self.text_area_frame.pack(pady=15, padx=5, anchor='w')

        self.old_name_entry.bind('<Button-1>', lambda event, widgets=[self.old_name_entry, self.new_name_entry], texts=['Old Name', 'New Name']: self.widgets_bindings(event, widgets, texts))
        self.new_name_entry.bind('<Button-1>', lambda event, widgets=[self.new_name_entry, self.old_name_entry], texts=['New Name', 'Old Name']: self.widgets_bindings(event, widgets, texts))
        self.old_name_entry.bind('<FocusIn>', lambda event, widgets=[self.old_name_entry, self.new_name_entry], texts=['Old Name', 'New Name']: self.widgets_bindings(event, widgets, texts))
        self.new_name_entry.bind('<FocusIn>', lambda event, widgets=[self.new_name_entry, self.old_name_entry], texts=['New Name', 'Old Name']: self.widgets_bindings(event, widgets, texts))
        self.new_name_entry.bind('<FocusOut>', lambda event, widgets=[self.old_name_entry, self.new_name_entry], texts=['Old Name', 'New Name']: self.widgets_bindings(event, widgets, texts))

        back_button.bind('<Return>', lambda e: self.back_command(frame))
        self.master.bind('<Button-1>', lambda event, widgets=[frame], entries=[self.old_name_entry, self.new_name_entry], texts=['Old Name', 'New Name']: self.master_bindings(event, widgets, entries, texts))

    def back_command(self, frame):
        '''Command for the back button'''

        self.text_area_frame.pack_forget()
        frame.pack_forget()

        self.first_left_frame.pack(padx=5, side=LEFT, ipady=2)
        self.text_area_frame.pack(pady=15, padx=5, anchor='w')

        self.video_entry.bind('<Button-1>', lambda event, widgets=[self.video_entry], texts=['Video Name']: self.widgets_bindings(event, widgets, texts))
        self.master.bind('<Button-1>', lambda event, widgets=[self.first_left_frame], entries=[self.video_entry], texts=['Video Name']: self.master_bindings(event, widgets, entries, texts))

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
        '''Reading all contents of the file'''

        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                return [line.strip('\n') for line in f.readlines()]

        else:
            with open(self.file_name, 'w'):
                pass

    def sort_file(self):
        '''Sorting contents of file according to length in ascending order'''

        contents = self.read_file()
        contents.sort(key=len)

        with open(self.file_name, 'w') as f:
            for content in contents:
                f.write(f'{content}\n')

    def insert_text_area(self):
        '''Insert text in Text widget'''

        contents = self.read_file()
        self.sort_file()
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
        '''Command for the ADD, REMOVE and SEARCH buttons'''

        contents = self.read_file()
        from_entry = self.video_entry.get().strip().title()

        if not from_entry or from_entry == 'Video Name':
            messagebox.showerror('Invalid Name', 'No Name given')

        elif button_name == 'ADD':
            if from_entry in contents:
                messagebox.showinfo('Already Exists', f'"{from_entry}" is already in file')

            else:
                with open(self.file_name, 'a') as f:
                    f.write(f'{from_entry}\n')

                messagebox.showinfo('Value Added', f'"{from_entry}" added in file')

        elif button_name == 'REMOVE':
            if from_entry in contents:
                with open(self.file_name, 'w') as f:
                    for content in contents:
                        if from_entry != content:
                            f.write(f'{content}\n')

                messagebox.showinfo('Value Removed', f'"{from_entry}" reomved from file')

            else:
                option = messagebox.askyesno('Add Value?', f'"{from_entry}" not in file. Do you want to add it?')

                if option:
                    self.action_button_command('ADD')

        elif button_name == 'SEARCH':
            if from_entry in contents:
                messagebox.showinfo('Exists', f'"{from_entry}" is in file')

            else:
                option = messagebox.askyesno('Add Value?', f'"{from_entry}" not in file. Do you want to add it?')

                if option:
                    self.action_button_command('ADD')

        self.sort_file()
        self.insert_text_area()

        self.video_entry.delete(0, END)
        self.video_entry.insert(END, 'Video Name')
        self.video_entry.config(fg='grey')

        self.master.focus()

    def rename_command(self):
        '''Commands for the RENAME button'''

        contents = self.read_file()
        old_name = self.old_name_entry.get().strip().title()
        new_name = self.new_name_entry.get().strip().title()

        if not old_name or not new_name or old_name == 'Old Name' or new_name == 'New Name':
            messagebox.showerror('Invalid Video Name', 'The input video name is invlaid')

        elif old_name not in contents:
            messagebox.showerror('Not exists', 'Old Name Not found')

        elif new_name in contents:
            messagebox.showerror('Already Exists', 'New Name already exists in file. Try another!')

        else:
            old_name_index = contents.index(old_name)
            contents[old_name_index] = new_name

            with open(self.file_name, 'w') as f:
                for content in contents:
                    f.write(f'{content}\n')

            self.insert_text_area()
            widgets = {self.old_name_entry: 'Old Name', self.new_name_entry: 'New Name'}

            for widget, text in widgets.items():
                widget.delete(0, END)
                widget.insert(END, text)
                widget.config(fg='grey')

            self.master.focus()
            messagebox.showinfo('Renamed', f'{old_name} renamed to {new_name}')

    def resource_path(self, relative_path):
        """ Get absolute path to resource from temporary directory

        In development:
            Gets path of photos that are used in this script like in icons and title_image from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of photos that are used in this script like in icons and title image from temporary directory"""

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path in _MEIPASS

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    SSNI()
