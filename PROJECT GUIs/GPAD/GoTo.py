from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import Include
import ShortCut


class Go_To:
    def __init__(self, master, text_widget):
        self.TextWidget = text_widget

        self.GoToWindow = Toplevel(master)
        self.GoToWindow.transient(master)
        self.GoToWindow.grab_set()

        self.GoToWindow.withdraw()
        self.GoToWindow.after(0, self.GoToWindow.deiconify)
        self.GoToWindow.title('Go To Line')
        self.GoToWindow.iconbitmap(Include.resource_path('transparent.ico'))
        pos_x, pos_y = master.winfo_x() + 55, master.winfo_y() + 170
        self.GoToWindow.geometry('{}x{}+{}+{}'.format(250, 100, pos_x, pos_y))
        self.GoToWindow.focus_set()

        self.GoToLabelEntryFrame = Frame(self.GoToWindow)
        self.GoToLabel = ttk.Label(self.GoToLabelEntryFrame, text='Line Number:')
        self.GoToEntry = ttk.Entry(self.GoToLabelEntryFrame, width=37)
        self.GoToLabel.grid(row=0, column=0, sticky='w')
        self.GoToEntry.grid(row=1, column=0)
        self.GoToEntry.focus_set()
        self.GoToLabelEntryFrame.place(x=10, y=7)

        self.ButtonsFrame = Frame(self.GoToWindow)
        self.GoToButton = ttk.Button(self.ButtonsFrame, text='Go To', width=10, command=self.GoTo)
        self.CancelButton = ttk.Button(self.ButtonsFrame, text='Cancel', width=10, command=self.GoToWindow.destroy)
        self.GoToButton.grid(row=0, column=0, padx=8)
        self.CancelButton.grid(row=0, column=1)
        self.ButtonsFrame.place(x=80, y=65)

        self.shortcut = ShortCut.ShortCut(self.GoToWindow)
        self.GoToEntry.bind('<Control-h>', self.entry_bind)
        self.GoToButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.GoToButton, 'Enter', True))
        self.GoToButton.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.CancelButton.bind('<Enter>', lambda e: self.shortcut.ShowShortCut(self.CancelButton, 'Esc', True))
        self.CancelButton.bind('<Leave>', lambda e: self.shortcut.destroy())

        self.GoToWindow.bind('<Return>', self.GoTo)
        self.GoToWindow.bind('<Escape>', lambda e: self.GoToWindow.destroy())
        self.GoToWindow.mainloop()

    def entry_bind(self, event=None):
        '''
        When Ctrl+h is pressed while the focus is in Entry widgets, the last
        character in Entry widgets gets remove(its default behavior). So, to
        fix this problem return "break" is must, this tells tkinter not to go
        for further bindings
        '''

        return 'break'

    def GoTo(self, event=None):
        '''
        Move cursor to the given number of lines if available
        '''

        try:
            line_number = int(self.GoToEntry.get().strip())
            get_from_text = len(self.TextWidget.get('1.0', 'end-1c').split('\n'))

            if 1 <= line_number <= get_from_text:
                self.TextWidget.mark_set('insert', '{}.0'.format(line_number))
                self.TextWidget.see('insert')
                self.GoToWindow.destroy()

            else:
                messagebox.showinfo('GPAD - Goto Line', f'The line number must not be beyond or below the total number of lines [{get_from_text}].', parent=self.GoToWindow)

        except ValueError:
            messagebox.showinfo('GPAD - Goto Line', 'Line number must be in number', parent=self.GoToWindow)
