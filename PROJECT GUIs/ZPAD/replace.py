from tkinter import *
import tkinter.ttk as ttk
import include
import shortcut


class Replace:
    def __init__(self, master, text_widget):
        self.find_index = None
        self.word_indexes = []
        self.transparent_ico = include.resource_path('included_files\\transparent.ico')

        self.master = master
        self.text_widget = text_widget
        self.dummy_text_widget = Text(master)

        self.match_var, self.wrap_var = IntVar(), IntVar()
        self.wrap_var.set(1)

        self.replace_master = Toplevel()
        self.replace_master.grab_set()

        self.hide_show = include.hide_or_show_maximize_minimize(self.replace_master)  # Hiding minimize and maximize button
        self.replace_master.after(0, self.hide_show.hide_minimize_maximize)

        self.replace_master.withdraw()
        self.replace_master.after(0, self.replace_master.deiconify)
        self.replace_master.title('Replace')
        self.replace_master.iconbitmap(self.transparent_ico)
        self.pos_x, self.pos_y = self.master.winfo_x() + 55, self.master.winfo_y() + 170
        self.replace_master.geometry('{}x{}+{}+{}'.format(350, 155, self.pos_x, self.pos_y))
        self.replace_master.resizable(0, 0)

        self.find_what_frame = Frame(self.replace_master)

        self.find_what_label = ttk.Label(self.find_what_frame, text='Find what:')
        self.replace_find_what_entry = ttk.Entry(self.find_what_frame, width=31)
        self.find_what_label.grid(row=0, column=0)
        self.replace_find_what_entry.focus_set()
        self.replace_find_what_entry.grid(row=0, column=1, padx=18)
        self.find_what_frame.place(x=0, y=5)

        self.replace_with_frame = Frame(self.replace_master)
        self.replace_with_label = ttk.Label(self.replace_with_frame, text='Replace what:')
        self.replace_with_entry = ttk.Entry(self.replace_with_frame, width=31)
        self.replace_with_label.grid(row=0, column=0)
        self.replace_with_entry.grid(row=0, column=1, pady=5)
        self.replace_with_frame.place(x=0, y=30)

        self.buttons_frame = Frame(self.replace_master)
        self.style = ttk.Style()
        self.style.configure('my.TButton', font=('Helvetica', 8))
        self.find_next_button = ttk.Button(self.buttons_frame, text='Find Next', width=9, style='my.TButton', command=self.find_next)
        self.replace_button = ttk.Button(self.buttons_frame, text='Replace', width=9, style='my.TButton', command=self.replace)
        self.replace_all_button = ttk.Button(self.buttons_frame, text='Replace All', width=9, style='my.TButton', command=self.replace_all)
        self.cancel_button = ttk.Button(self.buttons_frame, text='Cancel', width=9, style='my.TButton', command=self.exit)
        self.find_next_button.grid(row=0, column=0, ipadx=3)
        self.replace_button.grid(row=1, column=0, ipadx=3, pady=5)
        self.replace_all_button.grid(row=2, column=0, ipadx=3)
        self.cancel_button.grid(row=3, column=0, ipadx=3, pady=5)
        self.buttons_frame.place(x=275, y=5)

        self.check_button_frame = Frame(self.replace_master)
        self.match_case_checkbutton = ttk.Checkbutton(self.check_button_frame, text='Match case', variable=self.match_var, takefocus=False)
        self.wrap_around_case_checkbutton = ttk.Checkbutton(self.check_button_frame, text='Wrap around', variable=self.wrap_var, takefocus=False)
        self.match_case_checkbutton.pack(anchor='w')
        self.wrap_around_case_checkbutton.pack(anchor='w', pady=5)
        self.check_button_frame.place(x=5, y=100)

        self.shortcut = shortcut.ShortCut(self.replace_master)
        self.find_next_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.find_next_button, 'F3'))
        self.find_next_button.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.replace_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.replace_button, 'Ctrl+Shift+H'))
        self.replace_button.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.replace_all_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.replace_all_button, 'Ctrl+Alt+Enter'))
        self.replace_all_button.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.cancel_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.cancel_button, 'Esc'))
        self.cancel_button.bind('<Leave>', lambda e: self.shortcut.destroy())

        self.insert_selected_text()
        self.replace_master.bind('<Control-Alt-Return>', self.replace_all)
        self.replace_master.bind('<Control-H>', self.replace)
        self.replace_master.bind('<Escape>', self.exit)
        self.replace_with_entry.bind('<Control-h>', self.entry_bind)
        self.replace_find_what_entry.bind('<Control-h>', self.entry_bind)
        self.find_next_button.bind('<Return>', self.find_next)
        self.replace_button.bind('<Return>', self.replace)
        self.replace_all_button.bind('<Return>', self.replace_all)
        self.cancel_button.bind('<Return>', self.exit)
        self.replace_master.protocol('WM_DELETE_WINDOW', self.exit)
        self.replace_master.mainloop()

    def entry_bind(self, event=None):
        '''When Ctrl+h is pressed while the focus is in Entry widgets, the last
           character in Entry widgets gets remove(its default behavior). So,
           to fix this problem return "break" is must, this tells tkinter
           not to go for further bindings.'''

        return 'break'

    def insert_selected_text(self, event=None):
        '''If user selects certain word and then gets the find-widget then
           inserting the selected word to the "Find what" entry widget to
           make more convenient.'''

        try:
            selected_text = self.text_widget.get('sel.first', 'sel.last').strip().strip('\n')
            self.text_widget.mark_set('insert', self.text_widget.index('sel.last'))

        except TclError:
            if 'found' in self.text_widget.tag_names():
                selected_text = self.text_widget.get('found.first', 'found.last').strip().strip('\n')
                self.text_widget.mark_set('insert', self.text_widget.index('found.last'))

            else:
                selected_text = None

        if selected_text:
            self.replace_with_entry.focus_set()
            self.replace_find_what_entry.delete(0, 'end')
            self.replace_find_what_entry.insert('end', selected_text)

    def add_tag(self, start_pos, end_pos):
        '''Add "found" tag to select the letters when match is replace by another word'''

        try:
            self.text_widget.tag_delete('found', '1.0', 'end')
            self.text_widget.tag_add('found', start_pos, end_pos)
            self.text_widget.tag_config('found', background='#347afa', foreground='white')
            self.text_widget.see(self.text_widget.index('found.last'))
            self.text_widget.config(insertofftime=1000000, insertontime=0)

        except TclError:
            self.text_widget.tag_delete('found', '1.0', 'end')

    def get_cursor_position(self):
        '''Getting the index of the word right after the position of the cursor'''

        line, column = tuple(self.text_widget.index(INSERT).split('.'))

        for index, pos in enumerate(self.word_indexes):
            ln, cl = tuple(pos.split('.'))

            if line == ln and (column == cl or int(cl) > int(column)):
                return index - 1

        return len(self.word_indexes) - 1

    def search_index(self, text_widget, target_text):
        '''Getting index of word which we need to find'''

        self.word_indexes = []

        start_pos = '1.0'

        while True:
            start_pos = text_widget.search(target_text, start_pos, END)  # Getting index

            if not start_pos:
                return

            end_pos = f'{start_pos}+{len(target_text)}c'
            self.word_indexes.append(start_pos)
            start_pos = end_pos

    def find_next(self, event=None):
        '''Commands when user clicks "Find Next" button in Replace window'''

        replace_what = self.replace_find_what_entry.get()
        match_case = self.match_var.get()
        wrap_around = self.wrap_var.get()

        if not replace_what:
            messagebox.showinfo('ZPAD', f'Could not found "{replace_what}"', parent=self.replace_master)
            return

        if match_case == 1:  # When user selects "Match Case" check-button we need the content as it is in text_widget
            self.search_index(self.text_widget, replace_what)

        else:
            # But when user does not select "Match Case" check-button we need all content in lowercase in dummy_text_widget
            # We do this because we don't care whether the text is uppercase or lowercase while searching
            self.dummy_text_widget.delete('1.0', END)
            self.dummy_text_widget.insert(END, self.text_widget.get('1.0', END).lower())
            self.search_index(self.dummy_text_widget, replace_what.lower())

        if not self.word_indexes:
            messagebox.showinfo('ZPAD', f'Could not found "{replace_what}"', parent=self.replace_master)
            return

        if self.find_index is None:
            self.find_index = self.get_cursor_position()

        if wrap_around == 1:
            try:  # Setting self.find_index to the starting position of the 'found' tag if it is in text_widget
                found_tag_index = self.text_widget.index('found.first')
                self.find_index = self.word_indexes.index(found_tag_index)

            except:  # If not found tag in text_widget then setting self.find_index to -1
                self.find_index = self.get_cursor_position()

            if len(self.word_indexes) == 1:
                self.find_index = -1

            elif self.find_index == len(self.word_indexes) - 1:
                self.find_index = -1

        self.find_index += 1

        if self.find_index >= len(self.word_indexes):
            messagebox.showinfo('ZPAD', f'Could not found "{replace_what}"', parent=self.replace_master)

        else:
            start_pos = self.word_indexes[self.find_index]
            end_pos = f'{start_pos}+{len(replace_what)}c'

            self.add_tag(start_pos, end_pos)

    def replace(self, event=None):
        '''When user clicks "Replace" button in Replace window'''

        self.find_next()  # Getting indexes of the text in replace

        old_text = self.replace_find_what_entry.get()
        new_text = self.replace_with_entry.get()

        if old_text not in self.text_widget.get('1.0', END):
            return

        try:
            tag_index = self.text_widget.index('found.first')
            tag_index = self.word_indexes.index(tag_index)
            start_pos = self.word_indexes[tag_index]

        except (ValueError, TclError):
            return

        end_pos = f'{start_pos}+{len(old_text)}c'

        self.text_widget.delete(start_pos, end_pos)
        self.text_widget.insert(start_pos, new_text)

        self.add_tag(start_pos, f'{start_pos}+{len(new_text)}c')

    def replace_all(self, event=None):
        '''When user clicks "Replace All" button in Replace window'''

        old_text = self.replace_find_what_entry.get()
        new_text = self.replace_with_entry.get()
        match_case = self.match_var.get()

        if not old_text or old_text not in self.text_widget.get('1.0', END):
            messagebox.showinfo('ZPAD', f'Could not found "{old_text}"', parent=self.replace_master)
            return

        contents = self.text_widget.get('1.0', 'end-1c')

        if match_case == 1:
            contents = contents.replace(old_text, new_text)

        else:
            contents = contents.lower().replace(old_text, new_text)

        self.text_widget.delete('1.0', END)
        self.text_widget.insert('1.0', contents)

    def exit(self, event=None):
        '''When user quits the find window'''

        self.find_index = None

        if 'found' in self.text_widget.tag_names():
            found_tag_index = self.text_widget.index('found.first')
            self.text_widget.mark_set('insert', found_tag_index)

        self.replace_master.destroy()
