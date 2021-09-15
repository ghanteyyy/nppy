from tkinter import *
import tkinter.ttk as ttk
import include
import shortcut


class Find:
    def __init__(self, master, text_widget):
        self.changed = False
        self.find_index = None
        self.word_indexes = []
        self.direction_var, self.match_case_var, self.wrap_around_var = IntVar(), IntVar(), IntVar()

        self.master = master
        self.text_widget = text_widget
        self.transparent_ico = include.resource_path('transparent.ico')

        self.find_master = Toplevel()
        self.find_master.transient(self.master)
        self.find_master.grab_set()
        self.dummy_text_widget = Text(self.find_master)

        self.find_master.withdraw()
        self.find_master.after(0, self.find_master.deiconify)
        self.find_master.title('Find')
        self.find_master.iconbitmap(self.transparent_ico)
        self.pos_x, self.pos_y = self.master.winfo_x() + 55, self.master.winfo_y() + 170
        self.find_master.geometry('{}x{}+{}+{}'.format(355, 123, self.pos_x, self.pos_y))
        self.find_master.resizable(0, 0)

        self.label_entry_frame = Frame(self.find_master)
        self.buttons_frame = Frame(self.find_master)

        self.find_what_label = ttk.Label(self.label_entry_frame, text='Find what:')
        self.find_what_entry = ttk.Entry(self.label_entry_frame, width=34)
        self.find_what_label.grid(row=0, column=0)
        self.find_what_entry.grid(row=0, column=1, padx=5)
        self.label_entry_frame.place(x=0, y=5)
        self.find_what_entry.focus_set()

        self.style = ttk.Style()
        self.style.configure('my.TButton', font=('Helvetica', 8))
        self.find_next_button = ttk.Button(self.buttons_frame, text='Find Next', width=9, style='my.TButton', command=self.find)
        self.cancel_button = ttk.Button(self.buttons_frame, text='Cancel', width=9, style='my.TButton', command=self.exit)
        self.find_next_button.grid(row=0, column=0, ipadx=3)
        self.cancel_button.grid(row=1, column=0, pady=5, ipadx=3)
        self.buttons_frame.place(x=280, y=5)

        self.direction_var.set(2)
        self.ttk_label_frame = LabelFrame(self.find_master, text="Direction", padx=5, pady=5)
        self.up_radio_buttons = ttk.Radiobutton(self.ttk_label_frame, text='Up', takefocus=False, value=1, variable=self.direction_var)
        self.down_radio_buttons = ttk.Radiobutton(self.ttk_label_frame, text='Down', takefocus=False, value=2, variable=self.direction_var)
        self.up_radio_buttons.pack(side=LEFT)
        self.down_radio_buttons.pack(side=LEFT)
        self.ttk_label_frame.place(x=165, y=30)

        self.check_button_frame = Frame(self.find_master)
        self.match_case_check_button = ttk.Checkbutton(self.check_button_frame, text='Match case', variable=self.match_case_var, takefocus=False)
        self.wrap_around_case_check_button = ttk.Checkbutton(self.check_button_frame, text='Wrap around', variable=self.wrap_around_var, takefocus=False)
        self.match_case_check_button.pack(anchor='w')
        self.wrap_around_case_check_button.pack(anchor='w', pady=5)
        self.check_button_frame.place(x=5, y=70)

        self.shortcut = shortcut.ShortCut(self.find_master)
        self.find_next_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.find_next_button, 'F3'))
        self.find_next_button.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.cancel_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.cancel_button, 'ESC'))
        self.cancel_button.bind('<Leave>', lambda e: self.shortcut.destroy())

        self.insert_selected_text()
        self.find_master.bind('<F3>', self.find)
        self.cancel_button.bind('<Return>', self.exit)
        self.find_next_button.bind('<Return>', self.find)
        self.find_master.protocol('WM_DELETE_WINDOW', self.exit)
        self.find_master.bind('<Escape>', self.exit)
        self.find_what_entry.bind('<Control-h>', self.entry_bind)
        self.find_master.mainloop()

    def entry_bind(self, event=None):
        '''When Ctrl+h is pressed while the focus is in Entry widgets, the last
           character in Entry widgets gets remove(its default behavior). So,
           to fix this problem return "break" is must, this tells tkinter
           not to go for further bindings.'''

        return 'break'

    def insert_selected_text(self, event=None):
        '''If user selects certain word and then gets the find-widget then inserting the selected
           word to the "Find what" entry widget to make more convenient.'''

        selected_text = None

        try:
            selected_text = self.text_widget.get('sel.first', 'sel.last').strip().strip('\n')
            self.text_widget.mark_set('insert', self.text_widget.index('sel.last'))

        except TclError:
            if 'found' in self.text_widget.tag_names():
                selected_text = self.text_widget.get('found.first', 'found.last').strip().strip('\n')
                self.text_widget.mark_set('insert', self.text_widget.index('found.last'))

        if selected_text:
            self.find_what_entry.delete(0, 'end')
            self.find_what_entry.insert('end', selected_text)

    def add_tag(self, start_pos, end_pos):
        '''Add "found" tag to select the letters when match is found'''

        try:  # Removing 'sel' tag if it contains any selection
            self.text_widget.get('sel.first', 'sel.last')
            self.text_widget.tag_remove('sel', 'sel.first', 'sel.last')

        except TclError:
            pass

        self.text_widget.tag_delete('found')
        self.text_widget.mark_set('insert', start_pos)
        self.text_widget.config(insertofftime=1000000, insertontime=0)
        self.text_widget.tag_add('found', start_pos, end_pos)
        self.text_widget.tag_config('found', background='#347afa', foreground='white')
        self.text_widget.see(self.text_widget.index('found.last'))

    def get_cursor_position(self):
        '''Getting the index of the word right after the position of the cursor'''

        line, column = tuple(self.text_widget.index(INSERT).split('.'))

        for index, pos in enumerate(self.word_indexes):
            ln, cl = tuple(pos.split('.'))

            if line == ln and (column == cl or int(cl) > int(column)):
                return index - 1

        return len(self.word_indexes)

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

    def find(self, event=None):
        '''Command when user clicks Find Next button in Find window'''

        find_what = self.find_what_entry.get()
        direction = self.direction_var.get()
        match_case = self.match_case_var.get()
        wrap_around = self.wrap_around_var.get()

        if not find_what:
            messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.find_master)
            self.find_what_entry.focus()
            return

        if match_case == 1:  # When 'Match Case' checkbutton is selected
            self.search_index(self.text_widget, find_what)
            self.find_index = self.get_cursor_position()

            try:  # If 'found' tag is in the text_widget
                # Setting self.find_index to the starting_index if the starting_index of the 'found' tag is in the self.word_indexes
                found_tag_index = self.text_widget.index('found.first')

                if found_tag_index in self.word_indexes:
                    self.find_index = self.word_indexes.index(found_tag_index)

            except TclError:  # If found tag is not in text_widget
                if direction == wrap_around == 1 and self.find_index == -1:  # When 'Up' and 'Wrap Around' checkbuttons are selected and the cursor is at the very beginning
                    self.find_index = len(self.word_indexes)

            self.changed = True

        else:  # When 'Match Case' checkbutton is not selected
            # When user does not select "Match Case" check-button then we need all text of text_widget in lowercase in dummy_text_widget
            # We do this because case-sensitive does not matter

            self.dummy_text_widget.delete('1.0', END)
            self.dummy_text_widget.insert(END, self.text_widget.get('1.0', END).lower())
            self.search_index(self.dummy_text_widget, find_what.lower())

            if self.changed:  # When 'Match Case' is previously selected
                self.changed = False

                if direction == 1:  # If the direction is 'UP'
                    self.text_widget.mark_set('insert', self.text_widget.index('found.first'))  # Changing the position of cursor to the starting of the selection
                    self.find_index = self.get_cursor_position() + 1

                else:  # If the direction is 'DOWN'
                    self.text_widget.mark_set('insert', self.text_widget.index('found.last'))  # Changing the position of cursor to the ending of the selection

                    self.find_index = self.get_cursor_position()

        if not self.word_indexes:
            messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.find_master)
            return

        if self.find_index is None:  # If finding is being done first time
            self.find_index = self.get_cursor_position()

        if wrap_around == 1:  # When 'Wrap Around' checkbutton is selected
            if direction == 1:  # When 'Up' checkbutton is selected
                if self.find_index == 0:  # Checking if self.find_index is 0
                    self.find_index = len(self.word_indexes)  # then setting the self.find_index to the end of the word_list

                self.find_index -= 1  # Decreasing the self.find_index by 1 each time so that the finding looks like it is going in UP direction.

            else:  # When 'Down' checkbutton is selected
                if self.find_index == len(self.word_indexes) - 1:  # Checking if self.find_index is the last index of the self.word_indexes
                    self.find_index = -1  # then setting the self.find_index to -1

                self.find_index += 1  # Increasing the self.find_index by 1 each time so that the finding looks like it is going in DOWN direction.

        else:  # When 'Wrap Around' checkbutton is not selected
            if direction == 1:  # When 'Up' checkbutton is selected
                if self.find_index <= 0:  # When self.find_index is equal to first index of the self.word_indexes
                    messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.find_master)
                    return

                self.find_index -= 1  # Decreasing the self.find_index by 1 each time so that the finding looks like it is going in UP direction.

            else:  # When 'Down' checkbutton is selected
                if self.find_index > len(self.word_indexes) - 2:  # When self.find_index is beyond the index of the self.word_indexes
                    messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.find_master)
                    return

                self.find_index += 1  # Increasing the self.find_index by 1 each time so that the finding looks like it is going in DOWN direction.

        try:
            start_pos = self.word_indexes[self.find_index]  # Getting the starting_position of the matched word from the self.word_indexes
            end_pos = f'{start_pos}+{len(find_what)}c'  # Setting the ending_position of the matched word

            self.add_tag(start_pos, end_pos)  # Selecting the matched word

        except IndexError:
            messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.find_master)

    def exit(self, event=None):
        '''When user quits the find window'''

        self.find_index = None

        if 'found' in self.text_widget.tag_names():
            found_tag_index = self.text_widget.index('found.first')
            self.text_widget.mark_set(INSERT, found_tag_index)

        self.find_master.destroy()
