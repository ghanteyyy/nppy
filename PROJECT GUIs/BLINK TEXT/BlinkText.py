import os
import sys
import string
from tkinter import *
import pyperclip


class BlinkText:
    '''Show and hide the given text such that it appears as blinking'''

    def __init__(self):
        self.KeyCombo = set()
        self.IsDefault = True
        self.DEFAULT_TEXT = 'TEXT'
        self.ModifiersKeys = ['Control', 'Shift', 'Alt']

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Blinking Text')

        self.IconPhoto = PhotoImage(file=self.resource_path('icon.png'))
        self.master.iconphoto(False, self.IconPhoto)

        self.frame = Frame(self.master, bg='#422a91')
        self.frame.pack(padx=16)

        self.BlinkTextEntryVar = StringVar()
        self.BlinkTextEntryVar.set(self.DEFAULT_TEXT)
        self.BlinkTextEntry = Entry(self.frame, width=15, font=('Courier', 15, 'bold'), fg='grey', justify='center', textvariable=self.BlinkTextEntryVar)
        self.BlinkTextEntry.grid(row=0, column=0, pady=10, ipady=2)

        self.BlinkLabelVar = StringVar()
        self.BlinkLabelVar.set('Blink')
        self.BlinkLabel = Label(self.master, text='Blink', fg='white', bg='#422a91', width=15, font=('Courier', 20), textvariable=self.BlinkLabelVar, wraplength=205)
        self.BlinkLabel.pack(pady=1, ipady=5)

        self.master.bind('<Button-1>', self.left_click)
        self.BlinkTextEntryVar.trace('w', self.change_text)
        self.BlinkTextEntry.bind('<FocusIn>', self.focus_in)
        self.BlinkTextEntry.bind('<FocusOut>', self.focus_out)
        self.BlinkTextEntry.bind('<Control-c>', self.CopyText)
        self.BlinkTextEntry.bind('<Control-v>', self.PasteText)
        self.BlinkTextEntry.bind('<KeyPress>', self.key_pressed)
        self.BlinkTextEntry.bind('<KeyRelease>', self.key_released)
        self.BlinkTextEntry.bind('<Control-BackSpace>', self.ControlBackSpace)
        self.BlinkTextEntry.bind('<Control-x>', lambda e: self.CopyText(cut=True))

        self.initial_position()
        self.master.config(bg='#422a91')

        self.master.mainloop()

    def initial_position(self):
        '''Centering window when program starts'''

        self.master.update()

        width, height = self.master.winfo_width() // 2, self.master.winfo_height() // 2
        screen_width, screen_height = self.master.winfo_screenwidth() // 2, self.master.winfo_screenheight() // 2

        self.master.geometry(f'+{screen_width - width}+{screen_height - height}')
        self.master.resizable(0, 0)
        self.master.deiconify()
        self.blink()

    def left_click(self, event=None):
        '''When user clicks to anywhere in the window'''

        widget = event.widget

        if isinstance(widget, Entry) is False:
            self.master.focus()

    def focus_in(self, event=None):
        '''Change focus when user clicks in of the entry widget'''

        if self.IsDefault:
            self.BlinkTextEntryVar.set('')
            self.IsDefault = False
            self.BlinkTextEntry.config(fg='black')

    def focus_out(self, event=None):
        '''Change focus when user clicks out of the entry widget'''

        get_from_entry = self.BlinkTextEntryVar.get().strip()

        if self.IsDefault is False and not get_from_entry:
            self.BlinkTextEntryVar.set(self.DEFAULT_TEXT)
            self.IsDefault = True
            self.BlinkTextEntry.config(fg='grey')

    def ControlBackSpace(self, event=None):
        '''When user presses control and backspace key at the same time'''

        get_from_entry = self.BlinkTextEntryVar.get().strip()

        if get_from_entry:
            get_from_entry = get_from_entry.split()[:-1]
            join_get_from_entry = ' '.join(get_from_entry)

            self.BlinkTextEntryVar.set(join_get_from_entry)

        return 'break'

    def key_pressed(self, event=None):
        '''When user presses any key'''

        key = event.keysym

        for modifiers in ['Control', 'Alt']:
            if modifiers in key:
                self.KeyCombo.add(key)

        get_from_entry = self.BlinkTextEntryVar.get().strip()

        if len(get_from_entry) == 22:  # When the text length of Entry widget is equal to 22
            if not self.KeyCombo:  # When user have not pressed control or Alt key
                if self.BlinkTextEntry.selection_present() and key in string.printable:
                    last_index = self.BlinkTextEntry.index('sel.last')
                    first_index = self.BlinkTextEntry.index('sel.first')
                    self.BlinkTextEntry.delete(first_index, last_index)

                elif key not in ['Left', 'Right', 'Delete', 'BackSpace']:  # When user have not pressed left or right
                    return 'break'

    def key_released(self, event=None):
        '''When user releases the pressed key'''

        key = event.keysym

        if key in self.KeyCombo:
            self.KeyCombo.remove(key)

    def blink(self):
        '''Change color of text between #422a91 and white every 100 milliseconds'''

        if self.BlinkLabel['fg'] == '#422a91':
            self.BlinkLabel['fg'] = 'white'

        else:
            self.BlinkLabel['fg'] = '#422a91'

        self.master.after(100, self.blink)

    def change_text(self, *args):
        '''When user makes any changes in Entry widget'''

        get_from_entry = self.BlinkTextEntryVar.get().strip()

        if get_from_entry:
            self.BlinkLabelVar.set(get_from_entry)

        else:
            self.BlinkLabelVar.set('Blink')

    def CopyText(self, event=None, cut=False):
        '''Copy text to the system clipboard rather than only in tkinter clipboard'''

        if self.BlinkTextEntry.selection_present():
            selected_text = self.BlinkTextEntry.selection_get()
            pyperclip.copy(selected_text)

            if cut:
                first_index = self.BlinkTextEntry.index('sel.first')
                last_index = self.BlinkTextEntry.index('sel.last')
                self.BlinkTextEntry.delete(first_index, last_index)

        return 'break '

    def PasteText(self, event=None):
        '''
        Paste clipboard text to the entry widget

        If the length of clipboard text and entry widget's text
        combined is more than 22 characters (I set the maximum
        characters of 22 to be in blink effect. Though more
        than 22 characters can be made but looks awful when in
        action) and also if there is selection in entry widget
        then the selected text gets removed and only part of the
        clipboard text that makes the length of text 22 gets inserted
        in entry widget.
        '''

        required_length = 0
        clipboard_text = pyperclip.paste().strip()
        entry_text = self.BlinkTextEntryVar.get().strip()

        if self.BlinkTextEntry.selection_present():  # Remove selected text in Entry widget
            first_index = self.BlinkTextEntry.index('sel.first')
            last_index = self.BlinkTextEntry.index('sel.last')

            required_length = len(self.BlinkTextEntry.selection_get())
            self.BlinkTextEntry.delete(first_index, last_index)

        if len(entry_text + clipboard_text) > 22:
            if required_length == 0:
                required_length = 22 - len(entry_text)

            insert_text = clipboard_text[:required_length]

        else:
            insert_text = clipboard_text

        self.BlinkTextEntry.insert('insert', insert_text)

        return 'break'

    def resource_path(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    BlinkText()
