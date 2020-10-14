from tkinter import messagebox
import include


class Bindings:
    def __init__(self, master, frame):
        self.master = master
        self.click_bind_value = None
        self.listbox = frame.listbox
        self.entry_widget = frame.entry
        self.entry_var = frame.entry_var
        self.list_box_values = frame.values
        self.click_bind()

    def key_bind(self, *args):
        '''Filter the value in listbox as per given in entry widget'''

        try:
            var_get = self.entry_var.get()
            check_list = [value.lower() for value in self.list_box_values]
            starting_value = [fv for fv in check_list if fv.startswith(var_get.lower())]

            if len(starting_value) < 100:
                index = check_list.index(starting_value[0])
                self.listbox.yview(index)

                if var_get.lower() == starting_value[0].lower():
                    self.listbox.selection_set(index)

                else:
                    now = self.listbox.curselection()
                    self.listbox.selection_clear(now[0])

        except IndexError:
            pass

    def click_bind(self):
        '''Insert value of selected text from the listbox in entry widget'''

        now = self.listbox.curselection()

        if now != self.click_bind_value:
            self.click_bind_value = now

            if self.click_bind_value and self.listbox.get(self.click_bind_value[0]):
                value = self.listbox.get(self.click_bind_value[0])
                self.entry_var.set(value)
                self.master.after(10, lambda: set_selection(self.entry_widget, self.entry_var))

        self.master.after(10, self.click_bind)


class Commands:
    def __init__(self, master, font, sample_label, font_families_frame, font_style_frame, font_size_frame):
        self.top_level = master
        self.font = font
        self.font_families_frame = font_families_frame
        self.font_style_frame = font_style_frame
        self.font_size_frame = font_size_frame
        self.font_families = font_families_frame.values
        self.font_styles = font_style_frame.values
        self.font_sizes = font_size_frame.values
        self.sample_label = sample_label

        self.lower_font_style = [fs.lower() for fs in self.font_styles]
        self.lower_font_name = [fn.lower() for fn in self.font_families]

    def config_sample_label(self):
        '''Configure sample text as per the font_name, font_size and font_style
           from the entries widgets'''

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
        self.top_level.after(250, self.config_sample_label)

    def cmd(self, event=None):
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

        font_style_index = self.font_styles.index(font_style.title())
        font_style_listbox.selection_set(font_style_index)


def set_selection(entry_widget, var):
    # Selecting font_family in entry_widget

    entry_widget.select_range(0, len(var.get()) + 1)
    entry_widget.focus()
