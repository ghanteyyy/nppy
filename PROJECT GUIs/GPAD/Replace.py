from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import Include
import ShortCut


class Replace:
    def __init__(self, master, text_widget):
        self.FindIndex = None
        self.WordIndexes = []
        self.TransparentICO = Include.resource_path('transparent.ico')

        self.master = master
        self.TextWidget = text_widget
        self.DummyTextWidget = Text(master)

        self.MatchVar, self.WrapVar = IntVar(), IntVar()
        self.WrapVar.set(1)

        self.ReplaceWindow = Toplevel()
        self.ReplaceWindow.transient(self.master)
        self.ReplaceWindow.grab_set()

        self.ReplaceWindow.withdraw()
        self.ReplaceWindow.after(0, self.ReplaceWindow.deiconify)
        self.ReplaceWindow.title('Replace')
        self.ReplaceWindow.iconbitmap(self.TransparentICO)
        self.pos_x, self.pos_y = self.master.winfo_x() + 55, self.master.winfo_y() + 170
        self.ReplaceWindow.geometry('{}x{}+{}+{}'.format(350, 155, self.pos_x, self.pos_y))
        self.ReplaceWindow.resizable(0, 0)

        self.FindWhatFrame = Frame(self.ReplaceWindow)

        self.FindWhatLabel = ttk.Label(self.FindWhatFrame, text='Find what:')
        self.ReplaceFindWhatEntry = ttk.Entry(self.FindWhatFrame, width=31)
        self.FindWhatLabel.grid(row=0, column=0)
        self.ReplaceFindWhatEntry.focus_set()
        self.ReplaceFindWhatEntry.grid(row=0, column=1, padx=18)
        self.FindWhatFrame.place(x=0, y=5)

        self.ReplaceWithFrame = Frame(self.ReplaceWindow)
        self.ReplaceWithLabel = ttk.Label(self.ReplaceWithFrame, text='Replace what:')
        self.ReplaceWithEntry = ttk.Entry(self.ReplaceWithFrame, width=31)
        self.ReplaceWithLabel.grid(row=0, column=0)
        self.ReplaceWithEntry.grid(row=0, column=1, pady=5)
        self.ReplaceWithFrame.place(x=0, y=30)

        self.ButtonsFrame = Frame(self.ReplaceWindow)
        self.style = ttk.Style()
        self.style.configure('my.TButton', font=('Helvetica', 8))
        self.FindNextButton = ttk.Button(self.ButtonsFrame, text='Find Next', width=9, style='my.TButton', command=self.FindNext)
        self.ReplaceButton = ttk.Button(self.ButtonsFrame, text='Replace', width=9, style='my.TButton', command=self.Replace)
        self.ReplaceAllButton = ttk.Button(self.ButtonsFrame, text='Replace All', width=9, style='my.TButton', command=self.ReplaceAll)
        self.CancelButton = ttk.Button(self.ButtonsFrame, text='Cancel', width=9, style='my.TButton', command=self.exit)
        self.FindNextButton.grid(row=0, column=0, ipadx=3)
        self.ReplaceButton.grid(row=1, column=0, ipadx=3, pady=5)
        self.ReplaceAllButton.grid(row=2, column=0, ipadx=3)
        self.CancelButton.grid(row=3, column=0, ipadx=3, pady=5)
        self.ButtonsFrame.place(x=275, y=5)

        self.CheckButtonFrame = Frame(self.ReplaceWindow)
        self.MatchCaseCheckButton = ttk.Checkbutton(self.CheckButtonFrame, text='Match case', variable=self.MatchVar, takefocus=False)
        self.WrapAroundCaseCheckButton = ttk.Checkbutton(self.CheckButtonFrame, text='Wrap around', variable=self.WrapVar, takefocus=False)
        self.MatchCaseCheckButton.pack(anchor='w')
        self.WrapAroundCaseCheckButton.pack(anchor='w', pady=5)
        self.CheckButtonFrame.place(x=5, y=100)

        self.shortcut = ShortCut.ShortCut(self.ReplaceWindow)
        self.FindNextButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.FindNextButton, 'F3'))
        self.FindNextButton.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.ReplaceButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.ReplaceButton, 'Ctrl+Shift+H'))
        self.ReplaceButton.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.ReplaceAllButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.ReplaceAllButton, 'Ctrl+Alt+Enter'))
        self.ReplaceAllButton.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.CancelButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.CancelButton, 'Esc'))
        self.CancelButton.bind('<Leave>', lambda e: self.shortcut.destroy())

        self.InsertSelectedText()
        self.ReplaceWindow.bind('<Control-Alt-Return>', self.ReplaceAll)
        self.ReplaceWindow.bind('<Control-H>', self.Replace)
        self.ReplaceWindow.bind('<Escape>', self.exit)
        self.ReplaceWithEntry.bind('<Control-h>', self.entry_bind)
        self.ReplaceFindWhatEntry.bind('<Control-h>', self.entry_bind)
        self.FindNextButton.bind('<Return>', self.FindNext)
        self.ReplaceButton.bind('<Return>', self.Replace)
        self.ReplaceAllButton.bind('<Return>', self.ReplaceAll)
        self.CancelButton.bind('<Return>', self.exit)
        self.ReplaceWindow.protocol('WM_DELETE_WINDOW', self.exit)
        self.ReplaceWindow.mainloop()

    def entry_bind(self, event=None):
        '''When Ctrl+h is pressed while the focus is in Entry widgets, the last
           character in Entry widgets gets remove(its default behavior). So,
           to fix this problem return "break" is must, this tells tkinter
           not to go for further bindings.'''

        return 'break'

    def InsertSelectedText(self, event=None):
        '''If user selects certain word and then gets the find-widget then
           inserting the selected word to the "Find what" entry widget to
           make more convenient.'''

        try:
            selected_text = self.TextWidget.get('sel.first', 'sel.last').strip().strip('\n')
            self.TextWidget.mark_set('insert', self.TextWidget.index('sel.last'))

        except TclError:
            if 'found' in self.TextWidget.tag_names():
                selected_text = self.TextWidget.get('found.first', 'found.last').strip().strip('\n')
                self.TextWidget.mark_set('insert', self.TextWidget.index('found.last'))

            else:
                selected_text = None

        if selected_text:
            self.ReplaceWithEntry.focus_set()
            self.ReplaceFindWhatEntry.delete(0, 'end')
            self.ReplaceFindWhatEntry.insert('end', selected_text)

    def AddTag(self, start_pos, end_pos):
        '''Add "found" tag to select the letters when match is replace by another word'''

        try:
            self.TextWidget.tag_delete('found', '1.0', 'end')
            self.TextWidget.tag_add('found', start_pos, end_pos)
            self.TextWidget.tag_config('found', background='#347afa', foreground='white')
            self.TextWidget.see(self.TextWidget.index('found.last'))
            self.TextWidget.config(insertofftime=1000000, insertontime=0)

        except TclError:
            self.TextWidget.tag_delete('found', '1.0', 'end')

    def GetCurrentPosition(self):
        '''Getting the index of the word right after the position of the cursor'''

        line, column = tuple(self.TextWidget.index(INSERT).split('.'))

        for index, pos in enumerate(self.WordIndexes):
            ln, cl = tuple(pos.split('.'))

            if line == ln and (column == cl or int(cl) > int(column)):
                return index - 1

        return len(self.WordIndexes) - 1

    def SearchIndex(self, text_widget, target_text):
        '''Getting index of word which we need to find'''

        self.WordIndexes = []

        start_pos = '1.0'

        while True:
            start_pos = text_widget.search(target_text, start_pos, END)  # Getting index

            if not start_pos:
                return

            end_pos = f'{start_pos}+{len(target_text)}c'
            self.WordIndexes.append(start_pos)
            start_pos = end_pos

    def FindNext(self, event=None):
        '''Commands when user clicks "Find Next" button in Replace window'''

        replace_what = self.ReplaceFindWhatEntry.get()
        match_case = self.MatchVar.get()
        wrap_around = self.WrapVar.get()

        if not replace_what:
            messagebox.showinfo('GPAD', f'Could not found "{replace_what}"', parent=self.ReplaceWindow)
            return

        if match_case == 1:  # When user selects "Match Case" check-button we need the content as it is in text_widget
            self.SearchIndex(self.TextWidget, replace_what)

        else:
            # But when user does not select "Match Case" check-button we need all content in lowercase in dummy_text_widget
            # We do this because we don't care whether the text is uppercase or lowercase while searching
            self.DummyTextWidget.delete('1.0', END)
            self.DummyTextWidget.insert(END, self.TextWidget.get('1.0', END).lower())
            self.SearchIndex(self.DummyTextWidget, replace_what.lower())

        if not self.WordIndexes:
            messagebox.showinfo('GPAD', f'Could not found "{replace_what}"', parent=self.ReplaceWindow)
            return

        if self.FindIndex is None:
            self.FindIndex = self.GetCurrentPosition()

        if wrap_around == 1:
            try:  # Setting self.FindIndex to the starting position of the 'found' tag if it is in text_widget
                found_tag_index = self.TextWidget.index('found.first')
                self.FindIndex = self.WordIndexes.index(found_tag_index)

            except:  # If not found tag in text_widget then setting self.FindIndex to -1
                self.FindIndex = self.GetCurrentPosition()

            if len(self.WordIndexes) == 1:
                self.FindIndex = -1

            elif self.FindIndex == len(self.WordIndexes) - 1:
                self.FindIndex = -1

        self.FindIndex += 1

        if self.FindIndex >= len(self.WordIndexes):
            messagebox.showinfo('GPAD', f'Could not found "{replace_what}"', parent=self.ReplaceWindow)

        else:
            start_pos = self.WordIndexes[self.FindIndex]
            end_pos = f'{start_pos}+{len(replace_what)}c'

            self.AddTag(start_pos, end_pos)

    def Replace(self, event=None):
        '''When user clicks "Replace" button in Replace window'''

        self.FindNext()  # Getting indexes of the text in replace

        old_text = self.ReplaceFindWhatEntry.get()
        new_text = self.ReplaceWithEntry.get()

        if old_text not in self.TextWidget.get('1.0', END):
            return

        try:
            tag_index = self.TextWidget.index('found.first')
            tag_index = self.WordIndexes.index(tag_index)
            start_pos = self.WordIndexes[tag_index]

        except (ValueError, TclError):
            return

        end_pos = f'{start_pos}+{len(old_text)}c'

        self.TextWidget.delete(start_pos, end_pos)
        self.TextWidget.insert(start_pos, new_text)

        self.AddTag(start_pos, f'{start_pos}+{len(new_text)}c')

    def ReplaceAll(self, event=None):
        '''When user clicks "Replace All" button in Replace window'''

        old_text = self.ReplaceFindWhatEntry.get()
        new_text = self.ReplaceWithEntry.get()
        match_case = self.MatchVar.get()

        if not old_text or old_text not in self.TextWidget.get('1.0', END):
            messagebox.showinfo('GPAD', f'Could not found "{old_text}"', parent=self.ReplaceWindow)
            return

        contents = self.TextWidget.get('1.0', 'end-1c')

        if match_case == 1:
            contents = contents.replace(old_text, new_text)

        else:
            contents = contents.lower().replace(old_text, new_text)

        self.TextWidget.delete('1.0', END)
        self.TextWidget.insert('1.0', contents)

    def exit(self, event=None):
        '''When user quits the find window'''

        self.FindIndex = None

        try:
            found_tag_index = self.TextWidget.index('found.first')
            self.TextWidget.mark_set('insert', found_tag_index)

        except TclError:
            pass

        self.ReplaceWindow.destroy()
