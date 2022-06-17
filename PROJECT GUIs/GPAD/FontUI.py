import string
from tkinter import *
from tkinter import font
import tkinter.ttk as ttk
from tkinter import messagebox
import Include


class Widgets:
    '''Create a label, entry-widget and listbox'''

    def __init__(self, master, frame, label_text, values, entry_size, listbox_size):
        self.keys = []
        self.EntryIndex = 0

        self.master = master
        self.values = values
        self.LabelText = label_text
        self.LowerCaseValues = [v.lower() for v in values]

        self.frame = Frame(frame)
        self.frame.pack(side=LEFT, padx=5)

        self.Label = Label(self.frame, text=self.LabelText)

        self.EntryVar = StringVar()
        self.Entry = ttk.Entry(self.frame, textvariable=self.EntryVar, width=entry_size)

        self.ListBoxFrame = Frame(self.frame)
        self.TextVariable = Variable(value=values)
        self.ListBox = Listbox(self.ListBoxFrame, listvariable=self.TextVariable, width=listbox_size, height=6, selectmode=SINGLE, highlightthickness=0, exportselection=0, activestyle='none')
        self.ScrollBar = Scrollbar(self.ListBoxFrame, orient='vertical', command=self.ListBox.yview)
        self.ListBox.config(yscrollcommand=self.ScrollBar.set)

        self.Label.pack(anchor='w')
        self.Entry.pack(anchor='w')
        self.ListBoxFrame.pack(anchor='w')
        self.ListBox.pack(side=LEFT)
        self.ScrollBar.pack(side=LEFT, fill='y')

        self.ListBox.bind('<<ListboxSelect>>', self.ClickBind)

    def DownDirection(self, event=None):
        '''Move selection in downwards direction in listbox'''

        index = self.ListBox.curselection()[0]

        if index < len(self.values) - 1:
            index += 1

            self.ListBox.selection_clear(0, 'end')
            self.ListBox.selection_set(index)
            self.ListBox.see(index)

            self.EntryVar.set(self.values[index])
            self.Entry.selection_range(0, 'end')

        return 'break'

    def UpDirection(self, event=None):
        '''Move selection in upwards direction in listbox'''

        index = self.ListBox.curselection()[0]

        if index > 0:
            index -= 1

            self.ListBox.selection_clear(0, 'end')
            self.ListBox.selection_set(index)
            self.ListBox.see(index)

            self.EntryVar.set(self.values[index])
            self.Entry.selection_range(0, 'end')

        return 'break'

    def ClickBind(self, event=None):
        '''Insert value of selected text from the listbox in entry widget'''

        selection_index = self.ListBox.curselection()[0]
        data = self.ListBox.get(selection_index)

        self.EntryVar.set(data)
        self.master.after(10, lambda: SetSelection(self.Entry, self.EntryVar))

    def KeyPressed(self, event=None):
        '''When keys are pressed down'''

        key = event.keysym

        if key == 'space':
            key = ' '

        if key in string.printable:
            self.keys.append(key)

            if self.Entry.selection_present():
                self.sel = self.Entry.index('sel.first') + 1
                self.Entry.delete('sel.first', 'sel.last')

            else:
                self.sel = self.Entry.index('insert') + 1

            value = self.EntryVar.get() + key
            self.EntryVar.set(value)
            self.EntryIndex += 1

            self.Entry.icursor(self.EntryIndex)
            self.AutoComplete()

        return 'break'

    def KeyReleased(self, event=None):
        '''When the pressed keys are released'''

        key = event.keysym

        if key == ' ':
            key = 'space'

        if key in self.keys:
            self.keys.pop(self.keys.index(key))

        return 'break'

    def BackSpace(self, event=None):
        '''When backspace key is pressed'''

        value = self.EntryVar.get()[:-1]
        self.EntryVar.set(value)

        if self.EntryIndex != 0:
            if self.Entry.selection_present():
                self.Entry.delete('sel.first', 'sel.last')
                self.EntryIndex = len(self.EntryVar.get())

            else:
                self.EntryIndex -= 1

        return 'break'

    def TabCompletion(self, event=None):
        '''Select all text in entry widget of matched one.
           Also select the same value in listbox'''

        value = self.EntryVar.get()

        self.Entry.selection_range(0, 'end')
        self.Entry.icursor('end')

        index = self.values.index(value)
        self.ListBox.selection_clear(0, 'end')
        self.ListBox.selection_set(index)
        return 'break'

    def AutoComplete(self):
        '''Get matched fonts from the user entered font and if the whole
           font name is same as the first matched font then select the whole
           text in entry widget'''

        value = self.EntryVar.get().strip().lower()
        matched = [f for f in self.LowerCaseValues if f.startswith(value)]

        if matched:
            matched = matched[0]
            index = self.LowerCaseValues.index(matched)

            self.EntryVar.set(self.values[index])

            if self.Entry.index('insert') == len(matched):
                self.Entry.selection_range(0, 'end')
                self.ListBox.selection_clear(0, 'end')
                self.ListBox.selection_set(index)
                self.ListBox.see(index)

            else:
                self.ListBox.see(index)
                self.Entry.selection_range(self.sel, 'end')


class UI:
    '''Main window for selecting fonts'''

    def __init__(self, master, _font):
        self.font = _font

        self.master = master
        self.transparent_ico = Include.resource_path('transparent.ico')

        self.FontWindow = Toplevel(self.master)
        self.FontWindow.transient(self.master)
        self.FontWindow.withdraw()
        self.FontWindow.title('Font')
        self.FontWindow.grab_set()
        self.FontWindow.iconbitmap(self.transparent_ico)
        self.FontWindow.resizable(0, 0)

        self.pos_x, self.pos_y = self.master.winfo_x() + 30, self.master.winfo_y() + 60
        self.FontWindow.geometry(f'415x245+{self.pos_x}+{self.pos_y}')

        self.FontFamilies = list(font.families(self.FontWindow))
        self.FontFamilies.sort()
        self.FontFamilies = self.FontFamilies[26:]
        self.NonDuplicatesFonts()
        self.LowerFontName = [f.lower() for f in self.FontFamilies]

        self.FontStyles = ['Regular', 'Italic', 'Bold', 'Bold Italic', 'Underline', 'Overstrike']
        self.LowerFontStyles = [s.lower() for s in self.FontStyles]
        self.FontSizes = [str(i) for i in range(9, 73)]

        self.ContainerFrame = Frame(self.FontWindow)
        self.ContainerFrame.pack(padx=5)

        self.FontFamiliesFrame = Widgets(self.FontWindow, self.ContainerFrame, 'Font:', self.FontFamilies, 29, 27)
        self.FontStyleFrame = Widgets(self.FontWindow, self.ContainerFrame, 'Font Style:', self.FontStyles, 21, 19)
        self.FontSizeFrame = Widgets(self.FontWindow, self.ContainerFrame, 'Size:', self.FontSizes, 9, 7)

        for frame in [self.FontFamiliesFrame, self.FontStyleFrame, self.FontSizeFrame]:
            frame.Entry.bind('<Up>', frame.UpDirection)
            frame.Entry.bind('<Tab>', frame.TabCompletion)
            frame.Entry.bind('<BackSpace>', frame.BackSpace)
            frame.Entry.bind('<Down>', frame.DownDirection)
            frame.Entry.bind('<KeyPress>', frame.KeyPressed)
            frame.Entry.bind('<KeyRelease>', frame.KeyReleased)
            frame.Entry.bind('<Escape>', lambda e: self.FontWindow.destroy())

        self.SampleLabelFrame = LabelFrame(self.FontWindow, text='Sample')
        self.pixel = PhotoImage(width=1, height=1)
        self.SampleLabel = Label(self.SampleLabelFrame, text='AaBbYyZz', compound='center', image=self.pixel, width=200, height=40, takefocus=False)
        self.SampleLabel.grid(row=0, column=0)
        self.SampleLabelFrame.pack()

        self.BottomFrame = Frame(self.FontWindow)
        self.OkButton = ttk.Button(self.BottomFrame, text='OK', command=self.ApplyAndSaveDetails)
        self.CancelButton = ttk.Button(self.BottomFrame, text='Cancel', command=self.FontWindow.destroy)
        self.OkButton.pack(side=LEFT)
        self.CancelButton.pack(side=LEFT, padx=5)
        self.BottomFrame.pack(side=RIGHT, pady=5)

        self.SetToDefault()

        self.FontFamiliesFrame.Entry.bind('<Return>', self.ApplyAndSaveDetails)
        self.FontStyleFrame.Entry.bind('<Return>', self.ApplyAndSaveDetails)
        self.FontStyleFrame.Entry.bind('<Return>', self.ApplyAndSaveDetails)

        self.entry_listbox = {self.FontFamiliesFrame.Entry: self.FontFamiliesFrame.ListBox,
                              self.FontStyleFrame.Entry: self.FontStyleFrame.ListBox,
                              self.FontSizeFrame.Entry: self.FontSizeFrame.ListBox}

        self.NonDuplicatesFonts()
        self.master.after(0, self.FontWindow.deiconify)

        self.FontWindow.bind('<Key>', self.UpDown)
        self.FontWindow.after(250, lambda: SetSelection(self.FontFamiliesFrame.Entry, self.FontFamiliesFrame.EntryVar))
        self.FontWindow.after(100, self.ConfigSampleLabel)
        self.FontWindow.mainloop()

    def UpDown(self, event):
        '''When user wants to select value using up or down arrows in select_font window'''

        arrow_key = event.keysym

        if arrow_key in ['Up', 'Down']:
            focused_widget = self.FontWindow.focus_get()

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

    def NonDuplicatesFonts(self):
        '''Filter fonts starting with same name'''

        prev_family = ' '
        font_families = []

        for family in self.FontFamilies:
            if not family.startswith(prev_family):
                font_families.append(family)
                prev_family = family

        self.FontFamilies = font_families

    def ConfigSampleLabel(self):
        '''Configure sample text as per the font_name, font_size and font_style
           from the entries widgets'''

        try:
            font_name = self.FontFamiliesFrame.Entry.get()
            font_style = self.FontStyleFrame.Entry.get().lower()
            font_size = int(self.FontSizeFrame.Entry.get())

            if font_style == 'regular':
                _font = (font_name, font_size, 'normal')

            else:
                _font = (font_name, font_size, font_style)

            if font_name.lower() not in self.LowerFontName or font_style not in self.LowerFontStyles:
                _font = ('Courier', 9, 'normal')

            self.SampleLabel.config(font=_font)
            self.FontWindow.after(250, self.ConfigSampleLabel)

        except ValueError:
            pass

    def ApplyAndSaveDetails(self, event=None):
        '''Set font_family, font_size and font_style to the text-widget and save
           them to the file so that same font details are used when the program
           runs next time.'''

        font_family = self.FontFamiliesFrame.EntryVar.get().strip()
        font_style = self.FontStyleFrame.EntryVar.get().strip().lower()
        font_size = self.FontSizeFrame.EntryVar.get().strip()

        if font_family.lower() not in self.LowerFontName:
            messagebox.showinfo('Font', 'There is no font with that name.\nChoose a font from the list of fonts.', parent=self.FontWindow)
            return

        elif font_style not in self.LowerFontStyles:
            messagebox.showinfo('Font', 'This font is not available in that style.\nChoose a style from the list of styles.', parent=self.FontWindow)
            return

        try:
            font_size = int(font_size)

        except ValueError:
            font_size = 9

        if font_style == 'regular':
            font_style = 'normal'

        Include.ConfigFontStyle(font_style, self.font)
        font_details = Include.GetFontDetails()

        if 'Zoomed' in font_details:
            self.font.configure(family=font_family, size=font_size + font_details['Zoomed'])

        else:
            self.font.configure(family=font_family, size=font_size)

        font_index = self.LowerFontName.index(font_family.lower())  # Getting index of the font_family in entry_widget

        font_details['Font Family'] = self.FontFamilies[font_index]
        font_details['Font Size'] = font_size
        font_details['Font Style'] = font_style

        Include.SaveFontDetails(font_details)  # Saving font_details in file
        self.FontWindow.destroy()

    def SetToDefault(self):
        '''Get font_family, font_size and font_styles from the file and set
           details to the text-widget when the program opens for the first
           time'''

        self.FontFamiliesFrame.EntryVar.set('')
        self.FontStyleFrame.EntryVar.set('')
        self.FontSizeFrame.EntryVar.set('')

        curr_font = Include.GetFontDetails()  # Getting font details
        font_family, font_size, font_style = curr_font['Font Family'], curr_font['Font Size'], curr_font['Font Style']

        if font_style == 'normal':
            font_style = 'Regular'

        self.FontFamiliesFrame.EntryVar.set(font_family)
        self.FontSizeFrame.EntryVar.set(font_size)
        self.FontStyleFrame.EntryVar.set(font_style.title())

        # List boxes
        font_family_listbox = self.FontFamiliesFrame.ListBox
        font_size_listbox = self.FontSizeFrame.ListBox
        font_style_listbox = self.FontStyleFrame.ListBox

        # Getting index of the font_family, font_size and font_style from the json file
        font_family_index = self.FontFamilies.index(font_family)
        font_family_listbox.yview(font_family_index)
        font_family_listbox.selection_set(font_family_index)

        if str(font_size) in self.FontSizes:
            font_size_index = self.FontSizes.index(str(font_size))
            font_size_listbox.yview(font_size_index)
            font_size_listbox.selection_set(font_size_index)

        font_style_index = self.FontStyles.index(font_style.title())
        font_style_listbox.selection_set(font_style_index)


def SetSelection(entry_widget, var):
    # Selecting font_family in entry_widget

    entry_widget.select_range(0, len(var.get()) + 1)
    entry_widget.focus()
