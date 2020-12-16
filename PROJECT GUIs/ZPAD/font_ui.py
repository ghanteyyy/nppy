from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
import include
import select_font


class Widgets:
    '''Create a label, entry-widget and listbox'''

    def __init__(self, master, frame, label_text, values, entry_size, listbox_size):
        self.master = master
        self.values = values
        self.label_text = label_text

        self.frame = Frame(frame)
        self.frame.pack(side=LEFT, padx=5)

        self.label = Label(self.frame, text=self.label_text)

        self.entry_var = StringVar()
        self.entry = ttk.Entry(self.frame, textvariable=self.entry_var, width=entry_size)

        self.listbox_frame = Frame(self.frame)
        self.listbox = Listbox(self.listbox_frame, width=listbox_size, height=6, selectmode=SINGLE, highlightthickness=0, exportselection=0, activestyle='none')
        self.scrollbar = Scrollbar(self.listbox_frame, orient='vertical', command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.insert()

        self.label.pack(anchor='w')
        self.entry.pack(anchor='w')
        self.listbox_frame.pack(anchor='w')
        self.listbox.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill='y')

    def insert(self):
        '''Insert respective value to the entry-widget and to the list-box'''

        if self.label_text == 'Font:':
            self.entry_var.set('Courier')

        else:
            self.entry_var.set(self.values[0])

        for index, value in enumerate(self.values):
            self.listbox.insert(index, value)


class UI:
    '''Main window for selecting fonts'''

    def __init__(self, master, _font):
        self.master = master
        self.transparent_ico = include.resource_path('included_files\\transparent.ico')

        self.top_level = Toplevel(self.master)
        self.top_level.transient(self.master)
        self.top_level.withdraw()
        self.top_level.title('Font')
        self.top_level.grab_set()
        self.top_level.iconbitmap(self.transparent_ico)
        self.top_level.resizable(0, 0)

        self.pos_x, self.pos_y = self.master.winfo_x() + 30, self.master.winfo_y() + 60
        self.top_level.geometry(f'415x245+{self.pos_x}+{self.pos_y}')

        self.font_families = list(font.families(self.top_level))
        self.font_families.sort()
        self.font_families = self.font_families[26:]
        self.non_duplicates_fonts()
        self.font_styles = ['Regular', 'Italic', 'Bold', 'Bold Italic', 'Underline', 'Overstrike']
        self.font_sizes = [str(i) for i in range(9, 73)]

        self.container_frame = Frame(self.top_level)
        self.container_frame.pack(padx=5)

        self.font_families_frame = Widgets(self.top_level, self.container_frame, 'Font:', self.font_families, 29, 27)
        self.font_style_frame = Widgets(self.top_level, self.container_frame, 'Font Style:', self.font_styles, 21, 19)
        self.font_size_frame = Widgets(self.top_level, self.container_frame, 'Size:', self.font_sizes, 9, 7)

        self.sample_labelframe = LabelFrame(self.top_level, text='Sample')
        self.pixel = PhotoImage(width=1, height=1)
        self.sample_label = Label(self.sample_labelframe, text='AaBbYyZz', compound='center', image=self.pixel, width=200, height=40)
        self.sample_label.grid(row=0, column=0)
        self.sample_labelframe.pack()

        self.ok_cmd = select_font.Commands(self.top_level, _font, self.sample_label, self.font_families_frame, self.font_style_frame, self.font_size_frame)

        self.bottom_frame = Frame(self.top_level)
        self.ok_button = ttk.Button(self.bottom_frame, text='OK', command=self.ok_cmd.cmd)
        self.cancel_button = ttk.Button(self.bottom_frame, text='Cancel', command=self.top_level.destroy)
        self.ok_button.pack(side=LEFT)
        self.cancel_button.pack(side=LEFT, padx=5)
        self.bottom_frame.pack(side=RIGHT, pady=5)

        self.ffsmuic = select_font.Bindings(self.top_level, self.font_style_frame)
        self.ffssmuic = select_font.Bindings(self.top_level, self.font_size_frame)
        self.fffmuic = select_font.Bindings(self.top_level, self.font_families_frame)

        self.ok_cmd.set_to_default()

        self.font_families_frame.entry.bind('<Return>', self.ok_cmd.cmd)
        self.font_style_frame.entry.bind('<Return>', self.ok_cmd.cmd)
        self.font_style_frame.entry.bind('<Return>', self.ok_cmd.cmd)

        self.font_families_frame.entry_var.trace('w', self.fffmuic.key_bind)
        self.font_style_frame.entry_var.trace('w', self.ffsmuic.key_bind)
        self.font_size_frame.entry_var.trace('w', self.ffssmuic.key_bind)

        self.non_duplicates_fonts()
        self.master.after(0, self.top_level.deiconify)
        self.top_level.bind('<Escape>', lambda e: self.top_level.destroy())
        self.top_level.after(250, lambda: select_font.set_selection(self.font_families_frame.entry, self.font_families_frame.entry_var))
        self.top_level.after(100, self.ok_cmd.config_sample_label)
        self.top_level.mainloop()

    def non_duplicates_fonts(self):
        '''Filter fonts starting with same name'''

        prev_family = ' '
        font_families = []

        for family in self.font_families:
            if not family.startswith(prev_family):
                font_families.append(family)
                prev_family = family

        self.font_families = font_families
