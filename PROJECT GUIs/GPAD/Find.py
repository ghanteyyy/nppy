from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import Include
import ShortCut


class Find:
    def __init__(self, master, text_widget):
        self.changed = False
        self.FindIndex = None
        self.WordIndexes = []
        self.DirectionVar, self.MatchCaseVar, self.WrapAroundVar = IntVar(), IntVar(), IntVar()

        self.master = master
        self.TextWidget = text_widget
        self.TransparentICO = Include.resource_path('transparent.ico')

        self.FindWindow = Toplevel()
        self.FindWindow.transient(self.master)
        self.FindWindow.grab_set()
        self.DummyTextWidget = Text(self.FindWindow)

        self.FindWindow.withdraw()
        self.FindWindow.after(0, self.FindWindow.deiconify)
        self.FindWindow.title('Find')
        self.FindWindow.iconbitmap(self.TransparentICO)
        self.pos_x, self.pos_y = self.master.winfo_x() + 55, self.master.winfo_y() + 170
        self.FindWindow.geometry('{}x{}+{}+{}'.format(355, 123, self.pos_x, self.pos_y))
        self.FindWindow.resizable(0, 0)

        self.LabelEntryFrame = Frame(self.FindWindow)
        self.ButtonsFrame = Frame(self.FindWindow)

        self.FindWhatLabel = ttk.Label(self.LabelEntryFrame, text='Find what:')
        self.FindWhatEntry = ttk.Entry(self.LabelEntryFrame, width=34)
        self.FindWhatLabel.grid(row=0, column=0)
        self.FindWhatEntry.grid(row=0, column=1, padx=5)
        self.LabelEntryFrame.place(x=0, y=5)
        self.FindWhatEntry.focus_set()

        self.style = ttk.Style()
        self.style.configure('my.TButton', font=('Helvetica', 8))
        self.FindNextButton = ttk.Button(self.ButtonsFrame, text='Find Next', width=9, style='my.TButton', command=self.Find)
        self.CancelButton = ttk.Button(self.ButtonsFrame, text='Cancel', width=9, style='my.TButton', command=self.exit)
        self.FindNextButton.grid(row=0, column=0, ipadx=3)
        self.CancelButton.grid(row=1, column=0, pady=5, ipadx=3)
        self.ButtonsFrame.place(x=280, y=5)

        self.DirectionVar.set(2)
        self.ttkLabelFrame = LabelFrame(self.FindWindow, text="Direction", padx=5, pady=5)
        self.UpRadioButton = ttk.Radiobutton(self.ttkLabelFrame, text='Up', takefocus=False, value=1, variable=self.DirectionVar)
        self.DownRadioButton = ttk.Radiobutton(self.ttkLabelFrame, text='Down', takefocus=False, value=2, variable=self.DirectionVar)
        self.UpRadioButton.pack(side=LEFT)
        self.DownRadioButton.pack(side=LEFT)
        self.ttkLabelFrame.place(x=165, y=30)

        self.CheckButtonFrame = Frame(self.FindWindow)
        self.MatchCaseCheckButton = ttk.Checkbutton(self.CheckButtonFrame, text='Match case', variable=self.MatchCaseVar, takefocus=False)
        self.WrapAroundCaseCheckButton = ttk.Checkbutton(self.CheckButtonFrame, text='Wrap around', variable=self.WrapAroundVar, takefocus=False)
        self.MatchCaseCheckButton.pack(anchor='w')
        self.WrapAroundCaseCheckButton.pack(anchor='w', pady=5)
        self.CheckButtonFrame.place(x=5, y=70)

        self.InsertSelectedText()
        self.shortcut = ShortCut.ShortCut(self.FindWindow)

        self.FindNextButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.FindNextButton, 'F3'))
        self.FindNextButton.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.CancelButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.CancelButton, 'ESC'))
        self.CancelButton.bind('<Leave>', lambda e: self.shortcut.destroy())

        self.FindWindow.bind('<F3>', self.Find)
        self.CancelButton.bind('<Return>', self.exit)
        self.FindNextButton.bind('<Return>', self.Find)
        self.FindWindow.protocol('WM_DELETE_WINDOW', self.exit)
        self.FindWindow.bind('<Escape>', self.exit)
        self.FindWhatEntry.bind('<Control-h>', self.entry_bind)
        self.FindWindow.mainloop()

    def entry_bind(self, event=None):
        '''
        When Ctrl+h is pressed while the focus is in Entry widgets, the last
        character in Entry widgets gets remove(its default behavior). So, to
        fix this problem return "break" is must, this tells tkinter not to go
        for further bindings
        '''

        return 'break'

    def InsertSelectedText(self, event=None):
        '''
        If user selects certain word and then gets the find-widget then inserting
        the selected word to the "Find what" entry widget to make more convenient
        '''

        selected_text = None

        try:
            selected_text = self.TextWidget.get('sel.first', 'sel.last').strip().strip('\n')
            self.TextWidget.mark_set('insert', self.TextWidget.index('sel.last'))

        except TclError:
            if 'found' in self.TextWidget.tag_names():
                selected_text = self.TextWidget.get('found.first', 'found.last').strip().strip('\n')
                self.TextWidget.mark_set('insert', self.TextWidget.index('found.last'))

        if selected_text:
            self.FindWhatEntry.delete(0, 'end')
            self.FindWhatEntry.insert('end', selected_text)

    def AddTag(self, start_pos, end_pos):
        '''
        Add "found" tag to select the letters when match is found
        '''

        try:  # Removing 'sel' tag if it contains any selection
            self.TextWidget.get('sel.first', 'sel.last')
            self.TextWidget.tag_remove('sel', 'sel.first', 'sel.last')

        except TclError:
            pass

        self.TextWidget.tag_delete('found')
        self.TextWidget.mark_set('insert', start_pos)
        self.TextWidget.config(insertofftime=1000000, insertontime=0)
        self.TextWidget.tag_add('found', start_pos, end_pos)
        self.TextWidget.tag_config('found', background='#347afa', foreground='white')
        self.TextWidget.see(self.TextWidget.index('found.last'))

    def GetCursorPosition(self):
        '''
        Getting the index of the word right after the position of the cursor
        '''

        line, column = tuple(self.TextWidget.index(INSERT).split('.'))

        for index, pos in enumerate(self.WordIndexes):
            ln, cl = tuple(pos.split('.'))

            if line == ln and (column == cl or int(cl) > int(column)):
                return index - 1

        return len(self.WordIndexes)

    def SearchIndex(self, text_widget, target_text):
        '''
        Getting index of word which we need to find
        '''

        start_pos = '1.0'
        self.WordIndexes = []

        while True:
            start_pos = text_widget.search(target_text, start_pos, END)  # Getting index

            if not start_pos:
                return

            end_pos = f'{start_pos}+{len(target_text)}c'
            self.WordIndexes.append(start_pos)
            start_pos = end_pos

    def Find(self, event=None):
        '''
        Command when user clicks Find Next button in Find window
        '''

        find_what = self.FindWhatEntry.get()
        direction = self.DirectionVar.get()
        match_case = self.MatchCaseVar.get()
        wrap_around = self.WrapAroundVar.get()

        if not find_what:
            messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.FindWindow)
            self.FindWhatEntry.focus()
            return

        if match_case == 1:  # When 'Match Case' checkbutton is selected
            self.SearchIndex(self.TextWidget, find_what)
            self.FindIndex = self.GetCursorPosition()

            try:  # If 'found' tag is in the text_widget
                # Setting self.FindIndex to the starting_index if the starting_index of the 'found' tag is in the self.WordIndexes
                found_tag_index = self.TextWidget.index('found.first')

                if found_tag_index in self.WordIndexes:
                    self.FindIndex = self.WordIndexes.index(found_tag_index)

            except TclError:  # If found tag is not in text_widget
                if direction == wrap_around == 1 and self.FindIndex == -1:  # When 'Up' and 'Wrap Around' check-buttons are selected and the cursor is at the very beginning
                    self.FindIndex = len(self.WordIndexes)

            self.changed = True

        else:  # When 'Match Case' checkbutton is not selected
            # When user does not select "Match Case" check-button then we need all text of text_widget in lowercase in dummy_text_widget
            # We do this because case-sensitive does not matter

            self.DummyTextWidget.delete('1.0', END)
            self.DummyTextWidget.insert(END, self.TextWidget.get('1.0', END).lower())
            self.SearchIndex(self.DummyTextWidget, find_what.lower())

            if self.changed:  # When 'Match Case' is previously selected
                self.changed = False

                if direction == 1:  # If the direction is 'UP'
                    self.TextWidget.mark_set('insert', self.TextWidget.index('found.first'))  # Changing the position of cursor to the starting of the selection
                    self.FindIndex = self.GetCursorPosition() + 1

                else:  # If the direction is 'DOWN'
                    self.TextWidget.mark_set('insert', self.TextWidget.index('found.last'))  # Changing the position of cursor to the ending of the selection

                    self.FindIndex = self.GetCursorPosition()

        if not self.WordIndexes:
            messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.FindWindow)
            return

        if self.FindIndex is None:  # If finding is being done first time
            self.FindIndex = self.GetCursorPosition()

        if wrap_around == 1:  # When 'Wrap Around' checkbutton is selected
            if direction == 1:  # When 'Up' checkbutton is selected
                if self.FindIndex == 0:  # Checking if self.FindIndex is 0
                    self.FindIndex = len(self.WordIndexes)  # then setting the self.FindIndex to the end of the word_list

                self.FindIndex -= 1  # Decreasing the self.FindIndex by 1 each time so that the finding looks like it is going in UP direction.

            else:  # When 'Down' checkbutton is selected
                if self.FindIndex == len(self.WordIndexes) - 1:  # Checking if self.FindIndex is the last index of the self.WordIndexes
                    self.FindIndex = -1  # then setting the self.FindIndex to -1

                self.FindIndex += 1  # Increasing the self.FindIndex by 1 each time so that the finding looks like it is going in DOWN direction.

        else:  # When 'Wrap Around' checkbutton is not selected
            if direction == 1:  # When 'Up' checkbutton is selected
                if self.FindIndex <= 0:  # When self.FindIndex is equal to first index of the self.WordIndexes
                    messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.FindWindow)
                    return

                self.FindIndex -= 1  # Decreasing the self.FindIndex by 1 each time so that the finding looks like it is going in UP direction.

            else:  # When 'Down' checkbutton is selected
                if self.FindIndex > len(self.WordIndexes) - 2:  # When self.FindIndex is beyond the index of the self.WordIndexes
                    messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.FindWindow)
                    return

                self.FindIndex += 1  # Increasing the self.FindIndex by 1 each time so that the finding looks like it is going in DOWN direction.

        try:
            start_pos = self.WordIndexes[self.FindIndex]  # Getting the starting_position of the matched word from the self.WordIndexes
            end_pos = f'{start_pos}+{len(find_what)}c'  # Setting the ending_position of the matched word

            self.AddTag(start_pos, end_pos)  # Selecting the matched word

        except IndexError:
            messagebox.showinfo('GPAD', f'Could not found "{find_what}"', parent=self.FindWindow)

    def exit(self, event=None):
        '''
        When user quits the find window
        '''

        self.FindIndex = None

        if 'found' in self.TextWidget.tag_names():
            found_tag_index = self.TextWidget.index('found.first')
            self.TextWidget.mark_set(INSERT, found_tag_index)

        self.FindWindow.destroy()
