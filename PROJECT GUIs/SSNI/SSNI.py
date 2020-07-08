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
        self.file_name = r'D:\My Project\Python\PROJECT GUIs\SSNI\video_file.txt'

        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.resizable(0, 0)
        self.master.title('SSNI')
        self.master.iconbitmap(self.resource_path('included_files\\icon.ico'))

        self.width, self.height = 246, 175
        self.w_width, self.w_height = 246, 312
        self.screen_width, self.screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        self.master.geometry(f'{self.width}x{self.height}+{self.screen_width // 2 - self.width // 2}+{self.screen_height // 2 - self.height // 2}')

        self.title_label = Label(self.master, text='SSNI', fg='white', bg='black', font=('Courier', 20))
        self.title_label.pack(fill='both')

        self.add_remove_search = Button(self.master, text='ADD | REMOVE | SEARCH', bg='red', fg='white', activebackground='red', activeforeground='white', cursor='hand2', command=self.add_remove_search_view_command)
        self.add_remove_search.pack(fill='both', ipady=10)

        self.rename_button = Button(self.master, text='RENAME', bg='red', fg='white', activebackground='red', activeforeground='white', cursor='hand2', command=self.rename_button_command)
        self.rename_button.pack(fill='both', ipady=10)

        self.view_button = Button(self.master, text='VIEW', bg='red', fg='white', activebackground='red', activeforeground='white', cursor='hand2', command=self.view_command)
        self.view_button.pack(fill='both', ipady=10)

        self.add_remove_search.bind('<Return>', lambda e: self.add_remove_search_view_command())
        self.rename_button.bind('<Return>', lambda e: self.rename_button_command())
        self.view_button.bind('<Return>', lambda e: self.view_command())

        self.master.mainloop()

    def widgets_bindings(self, event, vars, var_texts, widgets):
        '''When user clicks or select using tab from keyboard'''

        if event.widget == widgets[0]:
            if vars[0].get().strip() == var_texts[0]:
                vars[0].set('')
                widgets[0].config(fg='black')

        if len(vars) == 2 and not vars[1].get().strip():
            vars[1].set(var_texts[1])
            widgets[1].config(fg='grey')

    def master_bindings(self, event, vars, var_texts, frame, widgets):
        '''When user clicks to any frames or to the root window'''

        if event.widget in [frame, self.master, self.title_label]:
            for index, var in enumerate(vars):
                if not var.get().strip():
                    var.set(var_texts[index])
                    widgets[index].config(fg='grey')

            self.master.focus()

    def remove_widgets(self, widgets):
        '''Remove widgets for adding another see in: re_add_widgets function'''

        for widget in widgets:
            widget.place_forget()
            widget.pack_forget()

    def re_add_widgets(self, widgets):
        '''Add removed back to the window'''

        for widget in widgets:
            widget.pack(fill='both', ipady=10)

    def back_command(self, add_widgets=None, remove_widgets=None):
        '''When user clicks back command'''

        self.remove_widgets(remove_widgets)

        if add_widgets:
            self.re_add_widgets(add_widgets)

        else:
            self.re_add_widgets((self.add_remove_search, self.rename_button, self.view_button))
            self.master.geometry(f'{self.width}x{self.height}+{self.screen_width // 2 - self.width // 2}+{self.screen_height // 2 - self.height // 2}')

    def add_remove_search_view_command(self):
        '''When user clicks ADD | REMOVE | SEARCH | VIEW button'''

        self.master.geometry(f'{self.w_width}x{self.w_height}+{self.screen_width // 2 - self.w_width // 2}+{self.screen_height // 2 - self.w_height // 2}')
        self.remove_widgets((self.add_remove_search, self.rename_button, self.view_button))

        frame = Frame(self.master, highlightthickness=2, highlightbackground='silver')

        video_entry_var = StringVar()
        video_entry = Entry(frame, fg='grey', font=('Courier', 12), width=19, justify='center', highlightthickness=2, highlightbackground='grey', textvariable=video_entry_var)
        video_entry_var.set('Video Name')
        video_entry.pack(pady=10, padx=10, ipady=3)

        add_button = Button(frame, text='ADD', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.action_button_command('ADD', entry_var=video_entry_var, widgets=video_entry))
        add_button.pack(pady=5, ipady=3, ipadx=80)

        remove_button = Button(frame, text='REMOVE', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.action_button_command('REMOVE', entry_var=video_entry_var, widgets=video_entry))
        remove_button.pack(pady=5, ipady=3, ipadx=70)

        search_button = Button(frame, text='SEARCH', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.action_button_command('SEARCH', entry_var=video_entry_var, widgets=video_entry))
        search_button.pack(pady=5, ipady=3, ipadx=70)

        frame.pack(pady=10)

        back_button = Button(self.master, text='BACK', bd=0, fg='blue', font=('Courier', 15, 'bold'), cursor='hand2', command=lambda: self.back_command(remove_widgets=(video_entry, frame, back_button)))

        view_button = Button(frame, text='VIEW', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.view_command(remove_widgets=(frame, back_button)))
        view_button.pack(pady=5, ipady=3, ipadx=80)

        back_button.pack()

        back_button.bind('<Enter>', lambda e: back_button.config(fg='red'))
        back_button.bind('<Leave>', lambda e: back_button.config(fg='blue'))
        view_button.bind('<Return>', lambda e: self.view_command(remove_widgets=(frame, back_button)))
        back_button.bind('<Return>', lambda e: self.back_command(remove_widgets=(video_entry, frame, back_button)))
        add_button.bind('<Return>', lambda e: self.action_button_command('ADD', entry_var=video_entry_var, widgets=video_entry))
        search_button.bind('<Return>', lambda e: self.action_button_command('SEARCH', entry_var=video_entry_var, widgets=video_entry))
        remove_button.bind('<Return>', lambda e: self.action_button_command('REMOVE', entry_var=video_entry_var, widgets=video_entry))
        video_entry.bind('<FocusIn>', lambda event, vars=[video_entry_var], var_texts=['Video Name'], widgets=[video_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        video_entry.bind('<Button-1>', lambda event, vars=[video_entry_var], var_texts=['Video Name'], widgets=[video_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        self.master.bind('<Button-1>', lambda event, vars=[video_entry_var], var_texts=['Video Name'], frame=frame, widgets=[video_entry]: self.master_bindings(event, vars, var_texts, frame, widgets))
        video_entry.bind('<FocusOut>', lambda event, vars=[video_entry_var, video_entry_var], var_texts=['Video Name', 'Video Name'], widgets=[video_entry, video_entry]: self.widgets_bindings(event, vars, var_texts, widgets))

    def rename_button_command(self):
        '''When user clicks rename button'''

        self.master.geometry(f'{self.w_width}x{self.w_height}+{self.screen_width // 2 - self.w_width // 2}+{self.screen_height // 2 - self.w_height // 2}')
        self.remove_widgets((self.add_remove_search, self.rename_button, self.view_button))

        frame = Frame(self.master, highlightthickness=2, highlightbackground='silver')

        old_name_var = StringVar()
        old_name_entry = Entry(frame, fg='grey', font=('Courier', 12), width=20, justify='center', highlightthickness=2, highlightbackground='grey', textvariable=old_name_var)
        old_name_var.set('Old Name')
        old_name_entry.pack(pady=10, padx=10, ipady=3)

        new_name_var = StringVar()
        new_name_entry = Entry(frame, fg='grey', font=('Courier', 12), width=20, justify='center', highlightthickness=2, highlightbackground='grey', textvariable=new_name_var)
        new_name_var.set('New Name')
        new_name_entry.pack(pady=10, padx=10, ipady=3)

        action_button = Button(frame, text='RENAME', bg='green', fg='white', activebackground='green', activeforeground='white', cursor='hand2', command=lambda: self.action_button_command('REPLACE', widgets=[old_name_entry, new_name_entry], old_var=old_name_entry, new_var=new_name_var))
        action_button.pack(pady=15, ipady=3, ipadx=80)

        frame.pack(pady=25)

        back_button = Button(self.master, text='BACK', bd=0, fg='blue', font=('Courier', 15, 'bold'), cursor='hand2', command=lambda: self.back_command(remove_widgets=(frame, back_button)))
        back_button.pack()

        back_button.bind('<Enter>', lambda e: back_button.config(fg='red'))
        back_button.bind('<Leave>', lambda e: back_button.config(fg='blue'))
        back_button.bind('<Return>', lambda e: self.back_command(remove_widgets=(frame, back_button)))
        old_name_entry.bind('<Return>', lambda e: self.action_button_command('REPLACE', widgets=[old_name_entry, new_name_entry], old_var=old_name_var, new_var=new_name_var))
        new_name_entry.bind('<Return>', lambda e: self.action_button_command('REPLACE', widgets=[old_name_entry, new_name_entry], old_var=old_name_var, new_var=new_name_var))
        action_button.bind('<Return>', lambda e: self.action_button_command('REPLACE', widgets=[old_name_entry, new_name_entry], old_var=old_name_entry, new_var=new_name_var))
        old_name_entry.bind('<Button-1>', lambda event, vars=[old_name_var, new_name_var], var_texts=['Old Name', 'New Name'], widgets=[old_name_entry, new_name_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        new_name_entry.bind('<Button-1>', lambda event, vars=[new_name_var, old_name_var], var_texts=['New Name', 'Old Name'], widgets=[new_name_entry, old_name_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        old_name_entry.bind('<FocusIn>', lambda event, vars=[old_name_var, new_name_var], var_texts=['Old Name', 'New Name'], widgets=[old_name_entry, new_name_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        new_name_entry.bind('<FocusIn>', lambda event, vars=[new_name_var, old_name_var], var_texts=['New Name', 'Old Name'], widgets=[new_name_entry, old_name_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        new_name_entry.bind('<FocusOut>', lambda event, vars=[old_name_var, new_name_var], var_texts=['Old Name', 'New Name'], widgets=[old_name_entry, new_name_entry]: self.widgets_bindings(event, vars, var_texts, widgets))
        self.master.bind('<Button-1>', lambda event, vars=[old_name_var, new_name_var], var_texts=['Old Name', 'New Name'], frame=frame, widgets=[old_name_entry, new_name_entry]: self.master_bindings(event, vars, var_texts, frame, widgets))

    def view_command(self, remove_widgets=None):
        '''When user clicks view button'''

        self.master.geometry(f'{self.w_width}x{self.w_height}+{self.screen_width // 2 - self.w_width // 2}+{self.screen_height // 2 - self.w_height // 2}')

        if not remove_widgets:
            self.remove_widgets((self.add_remove_search, self.rename_button, self.view_button))

        else:
            self.remove_widgets(remove_widgets)

        self.sort_contents()

        with open(self.file_name, 'r') as f:
            contents = [content.strip('\n') for content in f.readlines()]

        self.text_area_frame = Frame(self.master, highlightthickness=2, highlightbackground='silver')
        self.text_area = Text(self.text_area_frame, width=27, height=14, state=DISABLED, cursor='arrow')
        self.scrollbar = Scrollbar(self.text_area_frame, orient="vertical", command=self.text_area.yview)

        self.text_area.pack(side=LEFT)
        self.text_area_frame.pack(pady=5, padx=4, anchor='w')
        self.show_scrollbar()

        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', END)

        for index, content in enumerate(contents):
            if index == 0:
                self.text_area.insert(END, content)

            else:
                self.text_area.insert(END, '\n' + content)

        self.text_area.config(state=DISABLED)

        back_button = Button(self.master, text='BACK', bd=0, fg='blue', font=('Courier', 15, 'bold'), cursor='hand2')

        if remove_widgets:
            back_button.config(command=lambda: self.back_command(add_widgets=remove_widgets, remove_widgets=(self.text_area_frame, back_button)))
            back_button.bind('<Return>', lambda e: self.back_command(add_widgets=remove_widgets, remove_widgets=(self.text_area_frame, back_button)))

        else:
            back_button.config(command=lambda: self.back_command(remove_widgets=(self.text_area_frame, back_button)))
            back_button.bind('<Return>', lambda e: self.back_command(remove_widgets=(self.text_area_frame, back_button)))

        back_button.pack()

        back_button.bind('<Enter>', lambda e: back_button.config(fg='red'))
        back_button.bind('<Leave>', lambda e: back_button.config(fg='blue'))

    def action_button_command(self, button_name, entry_var=None, widgets=None, old_var=None, new_var=None):
        '''When user clicks add, remove, search or rename button'''

        if entry_var:
            get_from_entry = entry_var.get().strip()

            if get_from_entry == 'Video Name':
                messagebox.showerror('Invalid Name', 'Enter a valid video')
                return

        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w'):
                pass

            contents = []

        else:
            with open(self.file_name, 'r') as f:
                contents = [line.strip('\n') for line in f.readlines()]

        if button_name == 'ADD':
            if get_from_entry in contents:
                messagebox.showinfo('Already Exists', f'"{get_from_entry}" is already in file')

            else:
                with open(self.file_name, 'a') as f:
                    f.write(f'{get_from_entry}\n')

                messagebox.showinfo('Value Added', f'"{get_from_entry}" added in file')

        elif button_name == 'REMOVE':
            try:
                if get_from_entry in contents:
                    with open(self.file_name, 'w') as f:
                        for content in contents:
                            if get_from_entry != content:
                                f.write(f'{content}\n')

                    messagebox.showinfo('Value Removed', f'"{get_from_entry}" reomved from file')

                else:
                    option = messagebox.askyesno('Add Value?', f'"{get_from_entry}" not in file. Do you want to add it?')

                    if option:
                        self.action_button_command('ADD', entry_var, widgets)

            except TypeError:
                messagebox.showinfo('Value Removed', f'{get_from_entry} reomved from file')

        elif button_name == 'SEARCH':
            if get_from_entry in contents:
                messagebox.showinfo('Exists', f'"{get_from_entry}" is in file')

            else:
                option = messagebox.askyesno('Add Value?', f'"{get_from_entry}" not in file. Do you want to add it?')

                if option:
                    self.action_button_command('ADD', entry_var, widgets)

        elif button_name == 'REPLACE':
            old_name = old_var.get().strip().title()
            new_name = new_var.get().strip().title()

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

                old_var.set('Old Name')
                new_var.set('New Name')

                for widget in widgets:
                    widget.config(fg='grey')

        else:
            messagebox.showerror('Invalid Name', 'Please Enter a valid video name')

        if button_name in ['ADD', 'REMOVE', 'SEARCH']:
            entry_var.set('Video Name')
            widgets.config(fg='grey')

            self.master.focus()

    def sort_contents(self):
        '''Sorting the contents of the file alphabetically'''

        with open(self.file_name, 'r') as f:
            contents = f.readlines()
            contents.sort()

        with open(self.file_name, 'w') as f:
            for content in contents:
                f.write(content)

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
