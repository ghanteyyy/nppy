from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import About
import Include
import FileMenu
import EditMenu
import FormatMenu
import ViewMenu
import RightClick


class GPAD:
    def __init__(self, NewWindow=False):
        self.get_font = Include.GetFontDetails()

        if NewWindow:  # When user wants to make a new window
            self.master = Toplevel()

            if 'Number of Windows' not in self.get_font:  # Tracking the number of Toplevel Windows
                self.get_font['Number of Windows'] = 1

            else:
                self.get_font['Number of Windows'] += 1

            Include.SaveFontDetails(self.get_font)

        else:  # When programs starts for the first time
            self.master = Tk()

        self.font = Font(family=self.get_font['Font Family'], size=self.get_font['Font Size'])
        Include.ConfigFontStyle(self.get_font['Font Style'], self.font)

        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.edit_menu = Menu(self.menu, tearoff=0)
        self.format_menu = Menu(self.menu, tearoff=0)
        self.view_menu = Menu(self.menu, tearoff=0)
        self.help_menu = Menu(self.menu, tearoff=0)

        for label, menu in {'File': self.file_menu, 'Edit': self.edit_menu, 'Format': self.format_menu, 'View': self.view_menu, 'Help': self.help_menu}.items():
            self.menu.add_cascade(label=label, menu=menu)

        self.master.config(menu=self.menu)

        self.CanvasFrame = Frame(self.master)
        self.LineCanvas = Canvas(self.CanvasFrame, width=50)
        self.CanvasHSB = Scrollbar(self.CanvasFrame, orient='horizontal', command=self.LineCanvas.xview)
        self.LineCanvas.configure(xscrollcommand=self.CanvasHSB.set)
        self.CanvasHSB.pack(side='bottom', fill='x')
        self.LineCanvas.pack(side='left', fill='y')

        self.TextWidgetFrame = Frame(self.master, width=659, height=424)
        self.TextWidgetFrame.grid_propagate(False)
        self.TextWidget = Text(master=self.TextWidgetFrame, bd=0, undo=True, font=self.font, maxundo=-1, autoseparators=True)
        self.VSB = Scrollbar(self.TextWidgetFrame, orient='vertical', command=self.TextWidget.yview)
        self.HSB = Scrollbar(self.TextWidgetFrame, orient='horizontal', command=self.TextWidget.xview)
        self.TextWidget.configure(yscrollcommand=self.VSB.set, xscrollcommand=self.HSB.set)

        self.TextWidget.grid(row=0, column=0, sticky='nsew')
        self.VSB.grid(row=0, column=1, sticky='ns')
        self.HSB.grid(row=1, column=0, sticky='ew')

        self.TextWidgetFrame.grid_rowconfigure(0, weight=1)
        self.TextWidgetFrame.grid_columnconfigure(0, weight=1)
        self.TextWidget.focus_set()
        self.TextWidgetFrame.pack(side='top', fill='both', expand=True)

        self.LineColumnVar = StringVar()
        self.status_label_var = StringVar()
        self.LineColumnVar.set('Ln 1, Col 1')

        self.StatusBarFrame = Frame(self.TextWidgetFrame)
        self.StatusBarFrame.grid(row=2, column=0, sticky='e')

        self.StatusLabel = Label(self.StatusBarFrame, textvariable=self.status_label_var)
        self.StatusLabel.grid(row=0, column=0, sticky='w')
        self.LineColumn = Label(self.StatusBarFrame, textvariable=self.LineColumnVar)
        self.LineColumn.grid(row=0, column=1, ipadx=20)
        self.ZoomLabel = Label(self.StatusBarFrame, text='100%')
        self.ZoomLabel.grid(row=0, column=2, ipadx=10)
        self.TextFormatter = Label(self.StatusBarFrame, text='Windows (CRLF)')
        self.TextFormatter.grid(row=0, column=3, ipadx=14)
        self.encoding = Label(self.StatusBarFrame, text='UTF-8')
        self.encoding.grid(row=0, column=4, ipadx=10)

        self.AutoSaveVar = BooleanVar()
        self.fmc = FileMenu.File_Menu(self.master, self.TextWidget, self.status_label_var)
        self.FileMenuOptions = ['New', 'New Window ', 'Open... ', 'Save', 'SaveAs...', 'Auto Save', 'Exit']
        self.FileMenuCommands = [self.fmc.New, self.fmc.NewWindow, self.fmc.Open, self.fmc.Save, self.fmc.SaveAs, self.fmc.AutoSave, self.exit]
        self.FileMenuAccelerator = ['Ctrl+N', 'Ctrl+Shift+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Alt+S', 'Ctrl+Q']

        self.emc = EditMenu.Edit_Menu(self.master, self.TextWidget, self.status_label_var)
        self.EditMenuOptions = ['Undo', 'Cut', 'Copy', 'Paste', 'Delete', 'Search with Google', 'Find...', 'Replace...', 'Go To...', 'Select All', 'Time / Date', 'Strip Trailing Whitespace']
        self.EditMenuCommands = [self.emc.undo, self.emc.cut, self.emc.copy, self.emc.paste, self.emc.delete, self.emc.SearchWithGoogle, self.emc.FindWidget, self.emc.ReplaceWidget, self.emc.GoToWidget, self.emc.SelectAll, self.emc.GetDateTime, self.emc.StripWhitespaces]
        self.EditMenuAccelerator = ['Ctrl+Z', 'Ctrl+X', 'Ctrl+C', 'Ctrl+V', 'DEL', 'Ctrl+E', 'Ctrl+F', 'Ctrl+H', 'Ctr+G', 'Ctrl+A', 'F5', 'Alt+Enter']

        self.Fmc = FormatMenu.Format(self.master, self.TextWidget, self.font)
        self.FormatMenuOptions = ['Word Wrap', 'Font...']
        self.FormatMenuAccelerator = ['Ctrl+W', 'Ctrl+Shift+F']

        self.vmc = ViewMenu.View(self.master, self.TextWidget, self.TextWidgetFrame, self.CanvasFrame, self.LineCanvas, self.StatusBarFrame, self.ZoomLabel, self.font)
        self.ViewMenuOptions = ['Zoom', 'Status Bar', 'FullScreen', 'Show Line Numbers']
        self.ZoomCommands = [self.vmc.ZoomIn, self.vmc.ZoomOut, self.vmc.DefaultZoom]
        self.ViewMenuZoomAccelerator = {'Zoom In': '            Ctrl+Plus', 'Zoom Out': '        Ctrl+Minus', 'Restore Default Zoom': '                 Ctrl+0'}

        self.HelpMenuOptions = ['About']
        self.HelpMenuAccelerator = ['F12']
        self.HelpMenuCommands = [self.about]

        for index, value in enumerate(self.FileMenuOptions):
            if index == len(self.FileMenuOptions) - 1:
                self.file_menu.add_separator()

            elif value == 'Auto Save':
                self.file_menu.add_checkbutton(label=value.ljust(23), onvalue=1, offvalue=0, variable=self.AutoSaveVar, accelerator=self.FileMenuAccelerator[index], command=lambda: self.fmc.AutoSave(self.AutoSaveVar))
                continue

            self.file_menu.add_command(label=value.ljust(23), accelerator=self.FileMenuAccelerator[index], command=self.FileMenuCommands[index])

        for index, value in enumerate(self.EditMenuOptions):
            if index in [1, 5, 11]:
                self.edit_menu.add_separator()

            self.edit_menu.add_command(label=value.ljust(40), accelerator=self.EditMenuAccelerator[index], command=self.EditMenuCommands[index])

        for index, value in enumerate(self.FormatMenuOptions):
            if index == 1:
                self.format_menu.add_command(label=value.ljust(30), accelerator=self.FormatMenuAccelerator[index], command=self.Fmc.FontSelection)

            else:
                self.format_menu.add_checkbutton(label=value, onvalue=True, offvalue=False, variable=self.Fmc.WrapAroundVar, accelerator=self.FormatMenuAccelerator[index], command=self.Fmc.WrapAround)

        for index, value in enumerate(self.ViewMenuOptions):
            if index == 0:
                self.sub_view_menu = Menu(self.view_menu, tearoff=0)
                self.view_menu.add_cascade(label=value, menu=self.sub_view_menu)

                for index, values in enumerate(self.ViewMenuZoomAccelerator.items()):
                    self.sub_view_menu.add_command(label=values[0], accelerator=values[1], command=self.ZoomCommands[index])

            elif index == 1:
                self.view_menu.add_checkbutton(label=value, onvalue=1, offvalue=False, variable=self.vmc.ShowStatusBar, accelerator='Alt+S'.rjust(30), command=self.vmc.toggle_statusbar)

            elif index == 2:
                self.view_menu.add_checkbutton(label=value, onvalue=1, offvalue=False, variable=self.vmc.FullScreenVar, accelerator='F11'.rjust(28), command=self.vmc.set_full_screen)

            elif index == 3:
                self.view_menu.add_checkbutton(label=value, onvalue=1, offvalue=False, variable=self.vmc.LineNumberVar, accelerator='Alt+L'.rjust(30), command=self.vmc.ToggleLineNumber)

        for index, value in enumerate(self.HelpMenuOptions):
            self.help_menu.add_command(label=value.ljust(20), accelerator=self.HelpMenuAccelerator[index], command=self.HelpMenuCommands[index])

        self.Fmc.WrapAround()
        self.vmc.ToggleLineNumber()
        self.UpdateLineColumn()
        self.EnableDisableMenu()
        self.UpdateLabelText()

        self.TextWidget.bind('<Control-q>', self.exit)
        self.TextWidget.bind('<Button-3>', self.button_3)
        self.TextWidget.bind('<Delete>', self.emc.delete)
        self.TextWidget.bind('<Control-n>', self.fmc.New)
        self.TextWidget.bind('<Control-x>', self.emc.cut)
        self.TextWidget.bind('<Control-o>', self.fmc.Open)
        self.TextWidget.bind('<Control-s>', self.fmc.Save)
        self.TextWidget.bind('<Control-z>', self.emc.undo)
        self.TextWidget.bind('<Control-c>', self.emc.copy)
        self.TextWidget.bind('<BackSpace>', self.backspace)
        self.TextWidget.bind('<Control-v>', self.emc.paste)
        self.TextWidget.bind('<Key>', self.RemoveSelection)
        self.TextWidget.bind('<F5>', self.emc.GetDateTime)
        self.master.bind('<F12>', self.HelpMenuCommands[0])
        self.master.protocol('WM_DELETE_WINDOW', self.exit)
        self.TextWidget.bind('<Control-S>', self.fmc.SaveAs)
        self.TextWidget.bind('<Control-N>', self.fmc.NewWindow)
        self.TextWidget.bind('<Control-a>', self.emc.SelectAll)
        self.TextWidget.bind('<Control-N>', self.fmc.NewWindow)
        self.TextWidget.bind('<Control-plus>', self.vmc.ZoomIn)
        self.TextWidget.bind('<Control-g>', self.emc.GoToWidget)
        self.TextWidget.bind('<MouseWheel>', self.vmc.WheelZoom)
        self.TextWidget.bind('<Button-1>', self.SingleLeftClick)
        self.TextWidget.bind('<Control-f>', self.ShowFindWidget)
        self.TextWidget.bind('<Control-minus>', self.vmc.ZoomOut)
        self.TextWidget.bind('<Control-0>', self.vmc.DefaultZoom)
        self.TextWidget.bind('<Triple-Button-1>', self.TripleClick)
        self.TextWidget.bind('<Control-h>', self.ShowReplaceWidget)
        self.master.bind('<F11>', lambda e: self.view_menu.invoke(2))
        self.master.bind('<Alt-s>', lambda e: self.view_menu.invoke(1))
        self.TextWidget.bind('<Control-e>', self.emc.SearchWithGoogle)
        self.TextWidget.bind('<Double-Button-1>', self.DoubleLeftClick)
        self.TextWidget.bind('<Alt-Return>', self.ActivateStripWhiteSpace)
        self.TextWidget.bind('<Alt-l>', lambda e: self.view_menu.invoke(3))
        self.TextWidget.bind('<Control-F>', lambda e: self.Fmc.FontSelection())
        self.TextWidget.bind('<Control-w>', lambda e: self.format_menu.invoke(0))
        self.master.after(0, lambda: Include.initial_position(self.master, self.TextWidget))
        self.TextWidget.bind('<Control-Alt-s>', lambda e: self.fmc.AutoSave(self.AutoSaveVar))
        self.TextWidget.bind('<Configure>', lambda e: self.TextWidget.configure(scrollregion=self.TextWidget.bbox('end')))

        self.master.mainloop()

    def backspace(self, event=None):
        '''
        When backspace key is pressed
        '''

        self.status_label_var.set('')
        self.TextWidget.config(insertofftime=300, insertontime=600)

    def UpdateLabelText(self):
        '''
        Show the number of text selected, number of text copied or cut
        '''

        try:
            selected_text = self.TextWidget.get('sel.first', 'sel.last')
            self.status_label_var.set(f'{len(selected_text)} characters selected')

        except TclError:
            pass

        self.master.after(10, self.UpdateLabelText)

    def SingleLeftClick(self, event=None):
        '''
        Remove "found" tag and restore the blinking time to default
        '''

        self.status_label_var.set('')

        if 'triple_click' in self.TextWidget.tag_names():
            self.TextWidget.tag_delete('triple_click', '1.0', 'end')

        if 'found' in self.TextWidget.tag_names():
            self.TextWidget.tag_delete('found', '1.0', 'end')

        if self.TextWidget['insertofftime'] == 1000000:
            self.TextWidget.config(insertofftime=300, insertontime=600)

    def button_3(self, event=None):
        '''
        When user right clicks
        '''

        RightClick.RightClick(self.master, self.TextWidget, self.fmc, self.status_label_var).ShowPopUp(event=event)

    def RemoveSelection(self, event=None):
        '''
        Remove "found" and "triple_click" tags from the text_widget and reset
        the blinking time to default
        '''

        if event.keysym in ['Up', 'Down', 'Right', 'Left']:
            self.SingleLeftClick()

        if self.fmc.IsFileChanged():
            self.status_label_var.set('')

    def change_title(self, event=None):
        '''
        Insert * to the title of the window when user makes any change to the content
        '''

        title = self.master.title()

        if self.fmc.IsFileChanged():
            if not title.startswith('*'):
                self.master.title('*' + title)

        else:
            self.master.title(title.lstrip('*'))

    def UpdateLineColumn(self, event=None):
        '''
        Insert the line number and column number at the status bar
        '''

        line, column = tuple(self.TextWidget.index(INSERT).split('.'))
        self.LineColumnVar.set(f'Ln {line}, Col {int(column) + 1}')

        self.change_title()
        self.master.after(50, self.UpdateLineColumn)

    def EnableDisableMenu(self):
        '''
        Enable or disable some sub-menus in edit-menus
        '''

        text_from_text_widget = self.TextWidget.get('1.0', 'end-1c').strip()

        if self.fmc.IsFileChanged():  # Enable 'Undo' option when any change is detected to the text-widget
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
            selected_text = self.emc.GetSelectedText()  # Get the selected text

        except TclError:  # If there is no any text selected
            selected_text = None
            self.TextWidget.focus()

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

        self.master.after(100, self.EnableDisableMenu)

    def ShowFindWidget(self, event=None):
        '''
        Command when user clicks find sub-menu in Edit-Menu or when user
        presses Ctrl+F only if the respective sub-menu is activated
        '''

        if self.edit_menu.entrycget(9, 'state') == 'normal':
            self.emc.FindWidget()

    def ShowReplaceWidget(self, event=None):
        '''
        Command when user clicks replace sub-menu in Edit-Menu or when user
        presses Ctrl+H only if the respective sub-menu is activated
        '''

        if self.edit_menu.entrycget(11, 'state') == 'normal':
            self.emc.ReplaceWidget()

    def ActivateStripWhiteSpace(self, event=None):
        '''
        Commands for striping whitespaces from each line when user clicks
        strip-whitespaces sub-menu in Edit-Menu or when user presses
        Alt+Enter if the respective sub-menu is activated
        '''

        if self.edit_menu.entrycget(14, 'state') == 'normal':
            self.emc.strip_whitespaces()

        return 'break'

    def DoubleLeftClick(self, event=None):
        '''
        Make selection up-to the end of the line when user makes left double clicks
        '''

        self.TextWidget.tag_delete('triple_click', '1.0', 'end')
        cursor_pos = self.TextWidget.index('insert')
        line_end = self.TextWidget.index(f'{cursor_pos.split(".")[0]}.end')

        if cursor_pos == line_end:
            return 'break'

        self.TextWidget.config(insertofftime=1000000, insertontime=0)

    def TripleClick(self, event=None):
        '''
        When user triple clicks select all texts within that line
        '''

        contents = self.TextWidget.get('1.0', 'end').strip('\n')

        if contents:
            cursor_pos = self.TextWidget.index('insert').split('.')[0]
            self.TextWidget.tag_delete('sel', '1.0', 'end')
            self.TextWidget.tag_add('sel', f'{cursor_pos}.0', f'{cursor_pos}.end')
            self.TextWidget.tag_add('triple_click', f'{cursor_pos}.0', f'{cursor_pos}.end+1c')

            return 'break'

    def about(self, event=None):
        '''
        When user clicks about sub-menu in Help menu
        '''

        About.About(self.master)

    def exit(self, event=None):
        '''
        When user wants to exit the program
        '''

        if self.fmc.IsFileChanged():
            choice = messagebox.askyesnocancel('GPAD', 'Do you really want to quit without saving?')

            if choice is False:
                self.fmc.Save()

        else:
            choice = True

        if choice:
            exit = True
            MasterDestroy = False
            content = Include.GetFontDetails()

            if 'Zoomed' in content:
                content.pop('Zoomed')

            NumberOfWindows = content['Number of Windows']  # Getting number of Toplevel windows

            if self.master.winfo_class() == 'Tk':  # When user wants to close the root window
                if NumberOfWindows > 0:  # When some Toplevel windows is opened
                    exit = False
                    content['Master Withdrawn'] = True
                    self.master.withdraw()  # Withdrawing Tk window from the window

            elif self.master.winfo_class() == 'Toplevel':  # When user wants to close the Toplevel window
                NumberOfWindows -=1
                content['Number of Windows'] = NumberOfWindows

                if NumberOfWindows == 0 and content['Master Withdrawn']:  # If the window is the last Toplevel window
                    MasterDestroy = True

            Include.SaveFontDetails(content)

            if MasterDestroy:  # Ending the mainloop of Tk window if there is no any Toplevel window
                self.master.master.destroy()

            else:  # When user wants to close the Toplevel window opening another Toplevel window
                if exit:
                    self.master.destroy()


if __name__ == '__main__':
    GPAD()
