import string
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
import include


class Widgets:
    '''Create a label, entry-widget and listbox'''

    def __init__(self, master, frame, label_text, values, entry_size, listbox_size):
        self.keys = []
        self.entry_index = 0

        self.master = master
        self.values = values
        self.label_text = label_text
        self.lower_case_values = [v.lower() for v in values]

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

        self.listbox.bind('<<ListboxSelect>>', self.click_bind)

    def down_direction(self, event=None):
        '''Move selection in downwards direction in listbox'''

        index = self.listbox.curselection()[0]

        if index < len(self.values) - 1:
            index += 1

            self.listbox.selection_clear(0, 'end')
            self.listbox.selection_set(index)
            self.listbox.see(index)

            self.entry_var.set(self.values[index])
            self.entry.selection_range(0, 'end')

        return 'break'

    def up_direction(self, event=None):
        '''Move selection in upwards direction in listbox'''

        index = self.listbox.curselection()[0]

        if index > 0:
            index -= 1

            self.listbox.selection_clear(0, 'end')
            self.listbox.selection_set(index)
            self.listbox.see(index)

            self.entry_var.set(self.values[index])
            self.entry.selection_range(0, 'end')

        return 'break'

    def click_bind(self, event=None):
        '''Insert value of selected text from the listbox in entry widget'''

        selection_index = self.listbox.curselection()[0]
        data = self.listbox.get(selection_index)

        self.entry_var.set(data)
        self.master.after(10, lambda: set_selection(self.entry, self.entry_var))

    def key_pressed(self, event=None):
        '''When keys are pressed down'''

        key = event.keysym

        if key == 'space':
            key = ' '

        if key in string.printable:
            self.keys.append(key)

            if self.entry.selection_present():
                self.sel = self.entry.index('sel.first') + 1
                self.entry.delete('sel.first', 'sel.last')

            else:
                self.sel = self.entry.index('insert') + 1

            value = self.entry_var.get() + key
            self.entry_var.set(value)
            self.entry_index += 1

            self.entry.icursor(self.entry_index)
            self.auto_complete()

        return 'break'

    def key_released(self, event=None):
        '''When the pressed keys are relased'''

        key = event.keysym

        if key == ' ':
            key = 'space'

        if key in self.keys:
            self.keys.pop(self.keys.index(key))

        return 'break'

    def backspace(self, event=None):
        '''When backspace key is pressed'''

        value = self.entry_var.get()[:-1]
        self.entry_var.set(value)

        if self.entry_index != 0:
            if self.entry.selection_present():
                self.entry.delete('sel.first', 'sel.last')
                self.entry_index = len(self.entry_var.get())

            else:
                self.entry_index -= 1

        return 'break'

    def tab_completion(self, event=None):
        '''Select all text in entry widget of matched one.
           Also select the same value in listbox'''

        value = self.entry_var.get()

        self.entry.selection_range(0, 'end')
        self.entry.icursor('end')

        index = self.values.index(value)
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(index)
        return 'break'

    def auto_complete(self):
        '''Get matched fonts from the user entered font and if the whole
           font name is same as the first matched font then select the whole
           text in entry widget'''

        value = self.entry_var.get().strip().lower()
        matched = [f for f in self.lower_case_values if f.startswith(value)]

        if matched:
            matched = matched[0]
            index = self.lower_case_values.index(matched)

            self.entry_var.set(self.values[index])

            if self.entry.index('insert') == len(matched):
                self.entry.selection_range(0, 'end')
                self.listbox.selection_clear(0, 'end')
                self.listbox.selection_set(index)
                self.listbox.see(index)

            else:
                self.listbox.see(index)
                self.entry.selection_range(self.sel, 'end')


class UI:
    '''Main window for selecting fonts'''

    def __init__(self, master, _font):
        self.font = _font

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
        self.lower_font_name = [f.lower() for f in self.font_families]

        self.font_styles = ['Regular', 'Italic', 'Bold', 'Bold Italic', 'Underline', 'Overstrike']
        self.lower_font_style = [s.lower() for s in self.font_styles]
        self.font_sizes = [str(i) for i in range(9, 73)]

        self.container_frame = Frame(self.top_level)
        self.container_frame.pack(padx=5)

        self.font_families_frame = Widgets(self.top_level, self.container_frame, 'Font:', self.font_families, 29, 27)
        self.font_style_frame = Widgets(self.top_level, self.container_frame, 'Font Style:', self.font_styles, 21, 19)
        self.font_size_frame = Widgets(self.top_level, self.container_frame, 'Size:', self.font_sizes, 9, 7)

        for frame in [self.font_families_frame, self.font_style_frame, self.font_size_frame]:
            frame.entry.bind('<Up>', frame.up_direction)
            frame.entry.bind('<Tab>', frame.tab_completion)
            frame.entry.bind('<BackSpace>', frame.backspace)
            frame.entry.bind('<Down>', frame.down_direction)
            frame.entry.bind('<KeyPress>', frame.key_pressed)
            frame.entry.bind('<KeyRelease>', frame.key_released)
            frame.entry.bind('<Escape>', lambda e: self.top_level.destroy())

        self.sample_labelframe = LabelFrame(self.top_level, text='Sample')
        self.pixel = PhotoImage(width=1, height=1)
        self.sample_label = Label(self.sample_labelframe, text='AaBbYyZz', compound='center', image=self.pixel, width=200, height=40, takefocus=False)
        self.sample_label.grid(row=0, column=0)
        self.sample_labelframe.pack()

        self.bottom_frame = Frame(self.top_level)
        self.ok_button = ttk.Button(self.bottom_frame, text='OK', command=self.apply_and_save_details)
        self.cancel_button = ttk.Button(self.bottom_frame, text='Cancel', command=self.top_level.destroy)
        self.ok_button.pack(side=LEFT)
        self.cancel_button.pack(side=LEFT, padx=5)
        self.bottom_frame.pack(side=RIGHT, pady=5)

        self.set_to_default()

        self.font_families_frame.entry.bind('<Return>', self.apply_and_save_details)
        self.font_style_frame.entry.bind('<Return>', self.apply_and_save_details)
        self.font_style_frame.entry.bind('<Return>', self.apply_and_save_details)

        self.entry_listbox = {self.font_families_frame.entry: self.font_families_frame.listbox,
                              self.font_style_frame.entry: self.font_style_frame.listbox,
                              self.font_size_frame.entry: self.font_size_frame.listbox}

        self.non_duplicates_fonts()
        self.master.after(0, self.top_level.deiconify)

        self.top_level.bind('<Key>', self.up_down)
        self.top_level.after(250, lambda: set_selection(self.font_families_frame.entry, self.font_families_frame.entry_var))
        self.top_level.after(100, self.config_sample_label)
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

    def config_sample_label(self):
        '''Configure sample text as per the font_name, font_size and font_style
           from the entries widgets'''

        try:
            font_name = self.font_families_frame.entry.get()
            font_style = self.font_style_frame.entry.get().lower()
            font_size = int(self.font_size_frame.entry.get())

            if font_style == 'regular':
                _font = (font_name, font_size, 'normal')

            else:
                _font = (font_name, font_size, font_style)

            if font_name.lower() not in self.lower_font_name or font_style not in self.lower_font_style:
                _font = ('Courier', 9, 'normal')

            self.sample_label.config(font=_font)
            self.top_level.after(250, self.config_sample_label)\

        except ValueError:
            pass

    def apply_and_save_details(self, event=None):
        '''Set font_family, font_size and font_style to the text-widget and save
           them to the file so that same font details are used when the program
           runs next time.'''

        font_family = self.font_families_frame.entry_var.get().strip()
        font_style = self.font_style_frame.entry_var.get().strip().lower()
        font_size = self.font_size_frame.entry_var.get().strip()

        if font_family.lower() not in self.lower_font_name:
            messagebox.showinfo('Font', 'There is no font with that name.\nChoose a font from the list of fonts.', parent=self.top_level)
            return

        elif font_style not in self.lower_font_style:
            messagebox.showinfo('Font', 'This font is not available in that style.\nChoose a style from the list of styles.', parent=self.top_level)
            return

        if not font_size.isdigit():
            font_size = 9

        if font_size.isdigit() and isinstance(font_size, str):
            font_size = int(font_size)

        if font_style == 'regular':
            font_style = 'normal'

        include.config_font_style(font_style, self.font)
        font_details = include.get_font_details()

        if 'Zoomed' in font_details:
            self.font.configure(family=font_family, size=font_size + font_details['Zoomed'])

        else:
            self.font.configure(family=font_family, size=font_size)

        font_index = self.lower_font_name.index(font_family.lower())  # Getting index of the font_family in entry_widget

        font_details['Font Family'] = self.font_families[font_index]
        font_details['Font Size'] = font_size
        font_details['Font Style'] = font_style

        include.save_font_details(font_details)  # Saving font_details in file
        self.top_level.destroy()

    def set_to_default(self):
        '''Get font_family, font_size and font_styles from the file and set
           details to the text-widget when the program opens for the first
           time'''

        self.font_families_frame.entry_var.set('')
        self.font_style_frame.entry_var.set('')
        self.font_size_frame.entry_var.set('')

        curr_font = include.get_font_details()  # Getting font details
        font_family, font_size, font_style = curr_font['Font Family'], curr_font['Font Size'], curr_font['Font Style']

        if font_style == 'normal':
            font_style = 'Regular'

        self.font_families_frame.entry_var.set(font_family)
        self.font_size_frame.entry_var.set(font_size)
        self.font_style_frame.entry_var.set(font_style)

        # List boxes
        font_family_listbox = self.font_families_frame.listbox
        font_size_listbox = self.font_size_frame.listbox
        font_style_listbox = self.font_style_frame.listbox

        # Getting index of the font_family, font_size and font_style from the json file
        font_family_index = self.font_families.index(font_family)
        font_family_listbox.yview(font_family_index)
        font_family_listbox.selection_set(font_family_index)

        if str(font_size) in self.font_sizes:
            font_size_index = self.font_sizes.index(str(font_size))
            font_size_listbox.yview(font_size_index)
            font_size_listbox.selection_set(font_size_index)

        font_style_index = self.font_styles.index(font_style)
        font_style_listbox.selection_set(font_style_index)


def set_selection(entry_widget, var):
    # Selecting font_family in entry_widget

    entry_widget.select_range(0, len(var.get()) + 1)
    entry_widget.focus()
