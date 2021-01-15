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
        self.text_variable = Variable(value=values)
        self.listbox = Listbox(self.listbox_frame, listvariable=self.text_variable, width=listbox_size, height=6, selectmode=SINGLE, highlightthickness=0, exportselection=0, activestyle='none')
        self.scrollbar = Scrollbar(self.listbox_frame, orient='vertical', command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.label.pack(anchor='w')
        self.entry.pack(anchor='w')
        self.listbox_frame.pack(anchor='w')
        self.listbox.pack(side=LEFT)
        self.scrollbar.pack(side=LEFT, fill='y')


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
        self.sample_label = Label(self.sample_labelframe, text='AaBbYyZz', compound='center', image=self.pixel, width=200, height=40, takefocus=False)
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

        self.entry_listbox = {self.font_families_frame.entry: self.font_families_frame.listbox,
                              self.font_style_frame.entry: self.font_style_frame.listbox,
                              self.font_size_frame.entry: self.font_size_frame.listbox}

        self.non_duplicates_fonts()
        self.master.after(0, self.top_level.deiconify)
        self.top_level.bind('<Key>', self.up_down)
        self.top_level.bind('<Escape>', lambda e: self.top_level.destroy())
        self.top_level.after(250, lambda: select_font.set_selection(self.font_families_frame.entry, self.font_families_frame.entry_var))
        self.top_level.after(100, self.ok_cmd.config_sample_label)
        self.top_level.mainloop()

    def up_down(self, event):
        '''When user wants to select value using up or down arrows in select_font window'''

        arrow_key = event.keysym

        if arrow_key in ['Up', 'Down']:
            focused_widget = self.top_level.focus_get()

            if isinstance(focused_widget, Listbox):
                # When user selects listbox using keyboard with TAB key then focus is set to the respective listbox
                # Since we do not have listbox-entry pair like we have entry-listbox pair in self.entry_listbox which causes KeyError
                # when we try to get values using listbox as key
                # To fix this we need to check if the instance of focused_widget is Listbox
                # If yes, then we need to get respective entry_widget from focused_listbox using list comprehension
                # And setting focused_widget to that extracted entry_widget

                # You might be thinking why I have changed focused_widget from listbox to entry_widget. I did so because
                # when I designed this program I used entry_widget to know the respective listbox. But when user sets focus
                # to the listbox using TAB from keyboard then I need to write another function to map listbox-entry widget
                # which is redundant. In-order to fix this redundancy I used list comprehension to extract keys with respect to values
                # from self.entry_listbox and use it to get respective entry_widget.

                focused_widget = [key for key, value in self.entry_listbox.items() if value == focused_widget][0]

            focused_listbox = self.entry_listbox[focused_widget]
            values_length = len(focused_listbox.get(0, "end")) - 1
            focused_listbox_value_index = focused_listbox.curselection()[0]

            if arrow_key == 'Up':
                if focused_listbox_value_index > 0:
                    focused_listbox.selection_clear(focused_listbox_value_index)
                    focused_listbox_value_index -= 1

            else:
                if focused_listbox_value_index < values_length:
                    focused_listbox.selection_clear(focused_listbox_value_index)
                    focused_listbox_value_index += 1

            focused_listbox.selection_set(focused_listbox_value_index)
            focused_listbox.event_generate('<<ListboxSelect>>')

    def non_duplicates_fonts(self):
        '''Filter fonts starting with same name'''

        prev_family = ' '
        font_families = []

        for family in self.font_families:
            if not family.startswith(prev_family):
                font_families.append(family)
                prev_family = family

        self.font_families = font_families
