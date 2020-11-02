from tkinter import *
from tkinter.font import Font
import include
import file_menu
import edit_menu
import format_menu
import view_menu
import about
import right_click


class ZPAD:
    def __init__(self):
        self.get_font = include.get_font_details()

        self.master = Tk()
        self.font = Font(family=self.get_font['Font Family'], size=self.get_font['Font Size'])
        include.config_font_style(self.get_font['Font Style'], self.font)

        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.format_menu = Menu(self.menu, tearoff=0)
        self.view_menu = Menu(self.menu, tearoff=0)
        self.help_menu = Menu(self.menu, tearoff=0)

        for label, menu in {'File': self.file_menu, 'Edit': self.edit_menu, 'Format': self.format_menu, 'View': self.view_menu, 'Help': self.help_menu}.items():
            self.menu.add_cascade(label=label, menu=menu)

        self.master.config(menu=self.menu)

        self.canvas_frame = Frame(self.master)
        self.line_canvas = Canvas(self.canvas_frame, width=50)
        self.canvas_hsb = Scrollbar(self.canvas_frame, orient='horizontal', command=self.line_canvas.xview)
        self.line_canvas.configure(xscrollcommand=self.canvas_hsb.set)
        self.canvas_hsb.pack(side='bottom', fill='x')
        self.line_canvas.pack(side='left', fill='y')

        self.text_widget_frame = Frame(self.master, width=659, height=424)
        self.text_widget_frame.grid_propagate(False)
        self.text_widget = Text(master=self.text_widget_frame, bd=0, undo=True, font=self.font, maxundo=-1, autoseparators=True)
        self.vsb = Scrollbar(self.text_widget_frame, orient='vertical', command=self.text_widget.yview)
        self.hsb = Scrollbar(self.text_widget_frame, orient='horizontal', command=self.text_widget.xview)
        self.text_widget.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.text_widget.grid(row=0, column=0, sticky='nsew')
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb.grid(row=1, column=0, sticky='ew')

        self.text_widget_frame.grid_rowconfigure(0, weight=1)
        self.text_widget_frame.grid_columnconfigure(0, weight=1)
        self.text_widget.focus_set()
        self.text_widget_frame.pack(side='top', fill='both', expand=True)

        self.line_column_var = StringVar()
        self.status_label_var = StringVar()
        self.line_column_var.set('Ln 1, Col 1')

        self.status_bar_frame = Frame(self.text_widget_frame)
        self.status_bar_frame.grid(row=2, column=0, sticky='e')

        self.status_label = Label(self.status_bar_frame, textvariable=self.status_label_var)
        self.status_label.grid(row=0, column=0, sticky='w')
        self.line_column = Label(self.status_bar_frame, textvariable=self.line_column_var)
        self.line_column.grid(row=0, column=1, ipadx=20)
        self.zoom_label = Label(self.status_bar_frame, text='100%')
        self.zoom_label.grid(row=0, column=2, ipadx=10)
        self.text_formatter = Label(self.status_bar_frame, text='Windows (CRLF)')
        self.text_formatter.grid(row=0, column=3, ipadx=14)
        self.encoding = Label(self.status_bar_frame, text='UTF-8')
        self.encoding.grid(row=0, column=4, ipadx=10)

        self.fmc = file_menu.File_Menu(self.master, self.text_widget, self.status_label_var)
        self.file_menu_options = ['New', 'New Window ', 'Open... ', 'Save', 'SaveAs...', 'Exit']
        self.file_menu_commands = [self.fmc.new, self.fmc.new_window, self.fmc.open, self.fmc.save, self.fmc.save_as, self.fmc.exit]
        self.file_menu_acclerator = ['Ctrl+N', 'Ctrl+Shift+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']

        self.emc = edit_menu.Edit_Menu(self.master, self.text_widget, self.status_label_var)
        self.edit_menu_options = ['Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Search with Google', 'Find...', 'Replace...', 'Go To...', 'Select All', 'Time / Date', 'Strip Trailing Whitespace']
        self.edit_menu_commands = [self.emc.undo, self.emc.cut, self.emc.copy, self.emc.paste, self.emc.delete, self.emc.search_with_google, self.emc.find_widget, self.emc.replace_widget, self.emc.go_to_widget, self.emc.select_all, self.emc.get_date_time, self.emc.strip_whitespaces]
        self.edit_menu_accelerator = ['Ctrl+Z', 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'DEL', 'Ctrl+E', 'Ctrl+F', 'Ctrl+H', 'Ctr+G', 'Ctrl+A', 'F5', 'Alt+Enter']

        self.Fmc = format_menu.Format(self.master, self.text_widget, self.font)
        self.format_menu_options = ['Word Wrap', 'Font...']
        self.format_menu_accelerator = ['Ctrl+W', 'Ctrl+Shift+F']

        self.vmc = view_menu.View(self.master, self.text_widget, self.text_widget_frame, self.canvas_frame, self.line_canvas, self.status_bar_frame, self.zoom_label, self.font)
        self.view_menu_options = ['Zoom', 'Status Bar', 'FullScreen', 'Show Line Numbers']
        self.zoom_commands = [self.vmc.zoom_in, self.vmc.zoom_out, self.vmc.default_zoom]
        self.view_menu_zoom_accelerator = {'Zoom In': '            Ctrl+Plus', 'Zoom Out': '        Ctrl+Minus', 'Restore Default Zoom': '                 Ctrl+0'}

        self.help_menu_options = ['About']
        self.help_menu_accelerator = ['F12']
        self.help_menu_commands = [self.about]

        for index, value in enumerate(self.file_menu_options):
            if index in [5, 7]:
                self.file_menu.add_separator()

            self.file_menu.add_command(label=value.ljust(23), accelerator=self.file_menu_acclerator[index], command=self.file_menu_commands[index])

        for index, value in enumerate(self.edit_menu_options):
            if index in [1, 5, 11]:
                self.edit_menu.add_separator()

            self.edit_menu.add_command(label=value.ljust(40), accelerator=self.edit_menu_accelerator[index], command=self.edit_menu_commands[index])

        for index, value in enumerate(self.format_menu_options):
            if index == 1:
                self.format_menu.add_command(label=value.ljust(30), accelerator=self.format_menu_accelerator[index], command=self.Fmc.font_selection)

            else:
                self.format_menu.add_checkbutton(label=value, onvalue=True, offvalue=False, variable=self.Fmc.wrap_around_var, accelerator=self.format_menu_accelerator[index], command=self.Fmc.wrap_around)

        for index, value in enumerate(self.view_menu_options):
            if index == 0:
                self.sub_view_menu = Menu(self.view_menu, tearoff=0)
                self.view_menu.add_cascade(label=value, menu=self.sub_view_menu)

                for index, values in enumerate(self.view_menu_zoom_accelerator.items()):
                    self.sub_view_menu.add_command(label=values[0], accelerator=values[1], command=self.zoom_commands[index])

            elif index == 1:
                self.view_menu.add_checkbutton(label=value, onvalue=1, offvalue=False, variable=self.vmc.show_status_bar, accelerator='Alt+S'.rjust(30), command=self.vmc.toggle_statusbar)

            elif index == 2:
                self.view_menu.add_checkbutton(label=value, onvalue=1, offvalue=False, variable=self.vmc.fullscreen_var, accelerator='F11'.rjust(28), command=self.vmc.set_full_screen)

            elif index == 3:
                self.view_menu.add_checkbutton(label=value, onvalue=1, offvalue=False, variable=self.vmc.line_number_var, accelerator='Alt+L'.rjust(30), command=self.vmc.toggle_linenumber)

        for index, value in enumerate(self.help_menu_options):
            self.help_menu.add_command(label=value.ljust(20), accelerator=self.help_menu_accelerator[index], command=self.help_menu_commands[index])

        self.Fmc.wrap_around()
        self.vmc.toggle_linenumber()
        self.update_line_column()
        self.enable_disable_menu()
        self.update_label_text()

        self.text_widget.bind('<Button-3>', self.button_3)
        self.text_widget.bind('<Delete>', self.emc.delete)
        self.text_widget.bind('<Control-n>', self.fmc.new)
        self.text_widget.bind('<Control-x>', self.emc.cut)
        self.text_widget.bind('<Control-o>', self.fmc.open)
        self.text_widget.bind('<Control-s>', self.fmc.save)
        self.text_widget.bind('<Control-q>', self.fmc.exit)
        self.text_widget.bind('<Control-z>', self.emc.undo)
        self.text_widget.bind('<Control-c>', self.emc.copy)
        self.text_widget.bind('<Control-v>', self.emc.paste)
        self.text_widget.bind('<Key>', self.remove_selection)
        self.text_widget.bind('<F5>', self.emc.get_date_time)
        self.master.bind('<F12>', self.help_menu_commands[0])
        self.text_widget.bind('<Control-S>', self.fmc.save_as)
        self.master.protocol('WM_DELETE_WINDOW', self.fmc.exit)
        self.text_widget.bind('<Control-a>', self.emc.select_all)
        self.text_widget.bind('<Control-N>', self.fmc.new_window)
        self.text_widget.bind('<Control-plus>', self.vmc.zoom_in)
        self.text_widget.bind('<Button-1>', self.button_1_command)
        self.text_widget.bind('<Control-minus>', self.vmc.zoom_out)
        self.text_widget.bind('<Control-f>', self.show_find_widget)
        self.text_widget.bind('<Control-g>', self.emc.go_to_widget)
        self.text_widget.bind('<Control-0>', self.vmc.default_zoom)
        self.text_widget.bind('<Double-Button-1>', self.double_click)
        self.master.bind('<F11>', lambda e: self.view_menu.invoke(2))
        self.text_widget.bind('<Triple-Button-1>', self.triple_click)
        self.master.bind('<Alt-s>', lambda e: self.view_menu.invoke(1))
        self.text_widget.bind('<Control-h>', self.show_replace_widget)
        self.text_widget.bind('<Control-e>', self.emc.search_with_google)
        self.master.after(0, lambda: include.initial_position(self.master))
        self.text_widget.bind('<Alt-l>', lambda e: self.view_menu.invoke(3))
        self.text_widget.bind('<Alt-Return>', self.activate_strip_whitespace)
        self.text_widget.bind('<Control-F>', lambda e: self.Fmc.font_selection())
        self.text_widget.bind('<Control-w>', lambda e: self.format_menu.invoke(0))
        self.text_widget.bind('<BackSpace>', lambda e: self.status_label_var.set(''))
        self.text_widget.bind('<Configure>', lambda e: self.text_widget.configure(scrollregion=self.text_widget.bbox('end')))
        self.master.mainloop()

    def update_label_text(self):
        '''Show the number of text selected, number of text copied or cut'''

        try:
            selected_text = self.text_widget.get('sel.first', 'sel.last')
            self.status_label_var.set(f'{len(selected_text)} characters selected')

        except TclError:
            pass

        self.master.after(10, self.update_label_text)

    def button_1_command(self, event=None):
        '''Remove "found" tag and restore the blinking time to default'''

        self.status_label_var.set('')

        if 'triple_click' in self.text_widget.tag_names():
            self.text_widget.tag_delete('triple_click', '1.0', 'end')

        if 'found' in self.text_widget.tag_names():
            self.text_widget.tag_delete('found', '1.0', 'end')

        if self.text_widget['insertofftime'] == 1000000:
            self.text_widget.config(insertofftime=300, insertontime=600)

    def button_3(self, event=None):
        '''When user right clicks'''

        right_click.Right_Click(self.master, self.text_widget, self.fmc, self.status_label_var).show_popup(event=event)

    def remove_selection(self, event=None):
        '''Remove "found" and "triple_click" tags from the text_widget annd reset the blinking time to default'''

        if event.keysym in ['Up', 'Down', 'Right', 'Left']:
            self.button_1_command()

        if self.fmc.is_file_changed():
            self.status_label_var.set('')

    def change_title(self, event=None):
        '''Insert * to the title of the window when user makes any change to the content'''

        title = self.master.title()

        if self.fmc.is_file_changed():
            if not title.startswith('*'):
                self.master.title('*' + title)

        else:
            self.master.title(title.lstrip('*'))

    def update_line_column(self, event=None):
        '''Insert the line number and column number at the status bar'''

        line, column = tuple(self.text_widget.index(INSERT).split('.'))
        self.line_column_var.set(f'Ln {line}, Col {int(column) + 1}')

        self.change_title()
        self.master.after(50, self.update_line_column)

    def enable_disable_menu(self):
        '''Enable or disable some sub-menus in edit-menus'''

        text_from_text_widget = self.text_widget.get('1.0', 'end-1c').strip()

        if self.fmc.is_file_changed():  # Enable 'Undo' option when any change is detected to the text-widget
            if self.edit_menu.entrycget(0, 'state') == 'disabled':
                self.edit_menu.entryconfig(0, state=NORMAL)

        else:  # Disable 'Undo' option when change is not detected to the text-widget
            if self.edit_menu.entrycget(0, 'state') == 'normal':
                self.edit_menu.entryconfig(0, state=DISABLED)

        if text_from_text_widget:  # Enabling find and find next option if any text is found in text_widget
            if self.edit_menu.entrycget(8, 'state') == 'disabled':
                self.edit_menu.entryconfig(8, state=NORMAL)
                self.edit_menu.entryconfig(9, state=NORMAL)
                self.edit_menu.entryconfig(10, state=NORMAL)
                self.edit_menu.entryconfig(11, state=NORMAL)
                self.edit_menu.entryconfig(14, state=NORMAL)

        else:  # Else disabling find and find next option
            if self.edit_menu.entrycget(8, 'state') == 'normal':
                self.edit_menu.entryconfig(8, state=DISABLED)
                self.edit_menu.entryconfig(9, state=DISABLED)
                self.edit_menu.entryconfig(10, state=DISABLED)
                self.edit_menu.entryconfig(11, state=DISABLED)
                self.edit_menu.entryconfig(14, state=DISABLED)

        try:   # Disabling Paste menu if no text is found clipboard
            self.get_from_clipboard = self.master.clipboard_get()  # Getting text from clipboard

            if self.edit_menu.entrycget(4, 'state') == 'disabled' and self.get_from_clipboard:
                self.edit_menu.entryconfig(4, state=NORMAL)

        except:  # Enabling Paste menu if text is found clipboard
            if self.edit_menu.entrycget(4, 'state') == 'normal':
                self.edit_menu.entryconfig(4, state=DISABLED)

        try:
            selected_text = self.emc.get_selected_text()  # Get the selected text

        except TclError:  # If there is no any text selected
            selected_text = None
            self.text_widget.focus()

        if selected_text:  # Disabling Copy, Cut, Delete and Search with Google when some text is selected.
            if self.edit_menu.entrycget(2, 'state') == 'disabled':
                self.edit_menu.entryconfig(2, state=NORMAL)
                self.edit_menu.entryconfig(3, state=NORMAL)
                self.edit_menu.entryconfig(5, state=NORMAL)
                self.edit_menu.entryconfig(7, state=NORMAL)

        else:  # Enabling Copy, Cut, Delete and Search with google when some text is selected.
            if self.edit_menu.entrycget(2, 'state') == 'normal':
                self.edit_menu.entryconfig(2, state=DISABLED)
                self.edit_menu.entryconfig(3, state=DISABLED)
                self.edit_menu.entryconfig(5, state=DISABLED)
                self.edit_menu.entryconfig(7, state=DISABLED)

        self.master.after(100, self.enable_disable_menu)

    def show_find_widget(self, event=None):
        '''Command when user clicks find sub-menu in Edit-Menu or when user
           presses Ctrl+F only if the respective sub-menu is activated.'''

        if self.edit_menu.entrycget(9, 'state') == 'normal':
            self.emc.find_widget()

    def show_replace_widget(self, event=None):
        '''Command when user clicks replace sub-menu in Edit-Menu or when user
           presses Ctrl+H only if the respective sub-menu is activated.'''

        if self.edit_menu.entrycget(11, 'state') == 'normal':
            self.emc.replace_widget()

    def activate_strip_whitespace(self, event=None):
        '''Commands for striping whitespaces from each line when user clicks
           strip-whitespaces sub-menu in Edit-Menu or when user presses
           Alt+Enter if the respective sub-menu is activated'''

        if self.edit_menu.entrycget(14, 'state') == 'normal':
            self.emc.strip_whitespaces()

        return 'break'

    def double_click(self, event=None):
        '''Make selection up-to the end of the line when user makes left double
           clicks'''

        self.text_widget.tag_delete('triple_click', '1.0', 'end')
        cursor_pos = self.text_widget.index('insert')
        line_end = self.text_widget.index(f'{cursor_pos.split(".")[0]}.end')

        if cursor_pos == line_end:
            return 'break'

        self.text_widget.config(insertofftime=1000000, insertontime=0)

    def triple_click(self, event=None):
        '''When user triple clicks select all texts within that line'''

        contents = self.text_widget.get('1.0', 'end').strip('\n')

        if contents:
            cursor_pos = self.text_widget.index('insert').split('.')[0]
            self.text_widget.tag_delete('sel', '1.0', 'end')
            self.text_widget.tag_add('sel', f'{cursor_pos}.0', f'{cursor_pos}.end')
            self.text_widget.tag_add('triple_click', f'{cursor_pos}.0', f'{cursor_pos}.end+1c')

            return 'break'

    def about(self, event=None):
        '''When user clicks about sub-menu in Help menu'''

        about.About(self.master)


if __name__ == '__main__':
    ZPAD()
