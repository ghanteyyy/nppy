from tkinter import *
import tkinter.ttk as ttk
import include
import shortcut


class Go_To:
    def __init__(self, master, text_widget):
        self.text_widget = text_widget
        self.go_to_master = Toplevel(master)
        self.go_to_master.transient(master)
        self.go_to_master.grab_set()

        self.go_to_master.withdraw()
        self.go_to_master.after(0, self.go_to_master.deiconify)
        self.go_to_master.title('Go To Line')
        self.go_to_master.iconbitmap(include.resource_path('included_files\\transparent.ico'))
        pos_x, pos_y = master.winfo_x() + 55, master.winfo_y() + 170
        self.go_to_master.geometry('{}x{}+{}+{}'.format(250, 100, pos_x, pos_y))
        self.go_to_master.focus_set()

        self.go_to_label_entry_frame = Frame(self.go_to_master)
        self.go_to_label = ttk.Label(self.go_to_label_entry_frame, text='Line Number:')
        self.go_to_entry = ttk.Entry(self.go_to_label_entry_frame, width=37)
        self.go_to_label.grid(row=0, column=0, sticky='w')
        self.go_to_entry.grid(row=1, column=0)
        self.go_to_entry.focus_set()
        self.go_to_label_entry_frame.place(x=10, y=7)

        self.buttons_frame = Frame(self.go_to_master)
        self.go_to_button = ttk.Button(self.buttons_frame, text='Go To', width=10, command=self.go_to)
        self.cancel_button = ttk.Button(self.buttons_frame, text='Cancel', width=10, command=self.go_to_master.destroy)
        self.go_to_button.grid(row=0, column=0, padx=8)
        self.cancel_button.grid(row=0, column=1)
        self.buttons_frame.place(x=80, y=65)

        self.shortcut = shortcut.ShortCut(self.go_to_master)
        self.go_to_entry.bind('<Control-h>', self.entry_bind)
        self.go_to_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.go_to_button, 'Enter', True))
        self.go_to_button.bind('<Leave>', lambda e: self.shortcut.destroy())
        self.cancel_button.bind('<Enter>', lambda e: self.shortcut.show_shortcut(self.cancel_button, 'Esc', True))
        self.cancel_button.bind('<Leave>', lambda e: self.shortcut.destroy())

        self.go_to_master.bind('<Return>', self.go_to)
        self.go_to_master.bind('<Escape>', lambda e: self.go_to_master.destroy())
        self.go_to_master.mainloop()

    def entry_bind(self, event=None):
        '''When Ctrl+h is pressed while the focus is in Entry widgets, the last
           character in Entry widgets gets remove(its default behavior). So,
           to fix this problem return "break" is must, this tells tkinter
           not to go for further bindings.'''

        return 'break'

    def go_to(self, event=None):
        '''Move cursor to the given number of lines if available'''

        try:
            line_number = int(self.go_to_entry.get().strip())
            get_from_text = len(self.text_widget.get('1.0', 'end-1c').split('\n'))

            if 1 <= line_number <= get_from_text:
                self.text_widget.mark_set('insert', '{}.0'.format(line_number))
                self.text_widget.see('insert')
                self.go_to_master.destroy()

            else:
                messagebox.showinfo('ZPAD - Goto Line', f'The line number must not be beyond or below the total number of lines [{get_from_text}].', parent=self.go_to_master)

        except ValueError:
            messagebox.showinfo('ZPAD - Goto Line', 'Line number must be in number', parent=self.go_to_master)
