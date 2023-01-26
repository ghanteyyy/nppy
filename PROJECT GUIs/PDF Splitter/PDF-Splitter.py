import os
import sys
from tkinter import *
import tkinter.ttk as ttk
from threading import Thread
from tkinter import scrolledtext, messagebox, filedialog
from splitter import SplitPDF


class _Entry:
    '''
    Create a ttk.Entry widget with temporary placeholder like in HTML
    '''

    def __init__(self, frame, width, entry_style_name, default_text='', entry_fg='grey'):
        self.IsDefault = True
        self.DEFAULT_TEXT = default_text
        self.entry_style_name = entry_style_name

        self.var = StringVar()
        self.var.set(default_text)

        self.EntryStyle = ttk.Style()
        self.EntryStyle.configure(f'{self.entry_style_name}.TEntry', foreground=entry_fg)
        self.Entry = ttk.Entry(frame, width=width, justify='center', textvariable=self.var, style=f'{self.entry_style_name}.TEntry')

        self.Entry.bind("<FocusIn>", self.focus_in)
        self.Entry.bind("<FocusOut>", self.focus_out)

    def focus_in(self, event=None):
        '''
        Remove temporary placeholder's text when user clicks to respective entry widget
        '''

        if self.IsDefault:
            self.var.set('')
            self.IsDefault = False
            self.EntryStyle.configure(f'{self.entry_style_name}.TEntry', foreground='black')

    def focus_out(self, event=None):
        '''
        Remove temporary placeholder's text when user clicks out of respective
        entry widget
        '''

        if self.IsDefault is False and not self.var.get().strip():
            self.IsDefault = True
            self.var.set(self.DEFAULT_TEXT)
            self.EntryStyle.configure(f'{self.entry_style_name}.TEntry', foreground='grey')


class _Top_Widgets:
    '''
    Create Entry widget and Button side-by-side at the beginning of the window
    '''

    def __init__(self, frame, style_name, entry_text=''):
        self.widget_frame = Frame(frame, bg='#bdccd4')
        self.widget_frame.pack(pady=(5, 0))

        self.Entry = _Entry(self.widget_frame, 100, style_name, entry_text)
        self.Entry.Entry.grid(row=0, column=0, ipady=6, padx=(5, 0))

        self.ButtonFrame = Frame(self.widget_frame, bg='white', highlightbackground='#29abe2', highlightthickness=2, bd=0, relief=FLAT)
        self.ButtonFrame.grid(row=0, column=1, padx=(5, 2), ipady=2)
        self.Button = Label(self.ButtonFrame, text='Browse', bg='white', width=15, cursor='hand2')
        self.Button.pack(ipady=4)


class _Mid_Widgets:
    '''
    Create Entry widget with '+' or 'x' button at the side of it
    '''

    def __init__(self, frame, row, cmd, var_text='Page Start - Page End', entry_fg='grey'):
        self.WholeFrame = Frame(frame, bg='white')
        self.ButtonFrame = Frame(self.WholeFrame, bg='white', highlightbackground='#00a99d', highlightthickness=2, bd=0, relief=FLAT)
        self.ButtonFrame.grid(row=row, column=0, ipady=2, pady=3)

        self.Entry = _Entry(self.ButtonFrame, 60, str(row), var_text, entry_fg)
        self.Entry.Entry.pack(side=LEFT, ipady=3, padx=(2, 0))

        self.AddButton = Button(self.ButtonFrame, text='+', bd=0, relief=FLAT, cursor='hand2', bg='purple', fg='white',
                                activebackground='purple', activeforeground='white', command=cmd)
        self.AddButton.pack(side=LEFT, padx=1, ipady=3, ipadx=5)

        self.Entry.Entry.bind('<Return>', cmd)


class PDFSplitter:
    '''
    Main Entry point of the Script
    '''

    def __init__(self):
        self.row = 0

        self.master = Tk()
        self.master.resizable(0, 0)
        self.master.withdraw()
        self.master.after(20, self.master.deiconify)
        self.master.config(bg='#bdccd4')
        self.master.title('PDF Splitter')
        self.IconPath = PhotoImage(file=self.ResourcePath('icon.png'))
        self.master.iconphoto(False, self.IconPath)

        self.Style = ttk.Style()
        self.Style.theme_use('clam')
        self.Style.map('TEntry', lightcolor=[('focus', 'blue')])

        # Creating Widgets that are located at the top section of the window
        self.TopFrame = Frame(self.master, bg='#bdccd4')
        self.TopFrame.pack()
        self.OriginalSourceEntry = _Top_Widgets(self.TopFrame, 'Original', 'Enter Original PDF path')
        self.OutputPathEntry = _Top_Widgets(self.TopFrame, 'Output', 'Enter output PDF path')

        # Creating Widgets that are located at the mid section of the window
        self.MidFrame = Frame(self.master)
        self.MidFrame.pack(padx=(5, 0), pady=(5, 0))

        self.MidInnerFrame1 = Frame(self.MidFrame)
        self.MidInnerFrame1.pack(side=LEFT)
        self.MidInnerFrame2 = Frame(self.MidFrame)
        self.MidInnerFrame2.pack(side=RIGHT)

        self.Prefix_Entry = _Entry(self.MidInnerFrame1, 50, 'Prefix', 'Enter Prefix Name')
        self.Prefix_Entry.Entry.pack(ipady=100)

        self.master.update()
        self.MidInnerFrame2_1 = Frame(self.MidInnerFrame2, bd=0, width=self.master.winfo_width() - self.MidInnerFrame1.winfo_width() - 8, height=self.MidInnerFrame1.winfo_height(), bg='white')
        self.MidInnerFrame2_1.propagate(False)
        self.MidInnerFrame2_1.pack(fill=BOTH)

        self.TextArea = scrolledtext.ScrolledText(self.MidInnerFrame2_1, cursor='arrow', state=DISABLED)
        self.TextArea.pack()
        self.master.update()
        self.TextArea.propagate(False)

        self.MidWidget = _Mid_Widgets(self.TextArea, 0, self.AddNextWidget)
        self.TextArea.window_create(END, window=self.MidWidget.WholeFrame)

        # Creating Widgets that are located at the bottom section of the window
        self.BottomFrame = Frame(self.master, bg='#bdccd4')
        self.BottomFrame.pack(fill='x', padx=(5,5), pady=(0, 5))

        self.GenerateButton = Button(self.BottomFrame, text='GENERATE PDF(s)', bd=0, bg='#f15a24', fg='white',
                                     activebackground='#f15a24', activeforeground='white', cursor='hand2',
                                     command=self.GenerateButtonCommand)
        self.GenerateButton.pack(fill='x', ipady=10, pady=(5, 5))

        self.OutputFrame = Frame(self.BottomFrame, bg='#bdccd4')
        self.OutputTextArea = scrolledtext.ScrolledText(self.OutputFrame, cursor='arrow', height=10, bg='#bdccd4', bd=0, state='disabled')
        self.OutputTextArea.pack(fill='x')

        self.ClearOutputButton = Button(self.OutputFrame, text='Clear Output', bd=0, fg='white', bg='#e07c02', activebackground='#e07c02', activeforeground='white', cursor='hand2', command=self.ClearOutput)
        self.ClearOutputButton.pack(fill='x', pady=(5, 3), ipady=10)

        # Bindings Widgets
        self.master.bind('<MouseWheel>', self.MouseWheelScroll)
        self.master.bind('<Button-1>', self.focus_on_everything)
        self.TextArea.bind('<Double-Button-1>', self.RestrictDefaultBindings)
        self.OutputPathEntry.Button.bind('<Button-1>', lambda e: self.GetPdfPath(self.OutputPathEntry, 'Output'))
        self.OriginalSourceEntry.Button.bind('<Button-1>', lambda e: self.GetPdfPath(self.OriginalSourceEntry, 'Original'))

        # self.test()  # Automates action of every widgets
        self.master.mainloop()

    def focus_on_everything(self, event=None):
        '''
        Focus to respective widget that is clicked to
        '''

        event.widget.focus()

    def RestrictDefaultBindings(self, event=None):
        '''
        Forbid the respective widget to fire its default bindings
        '''

        return 'break'

    def AddNextWidget(self, event=None):
        '''
        When user clicks to '+' or 'x' button located at the right-mid section widgets
        '''

        # Getting the current mouse pointer position
        abs_coord_x = self.master.winfo_pointerx() - self.master.winfo_vrootx()
        abs_coord_y = self.master.winfo_pointery() - self.master.winfo_vrooty()

        # Extracting the widget as per the mouse pointer position
        widget = self.master.winfo_containing(abs_coord_x, abs_coord_y)

        # Checking if the widget as per the mouse pointer position is '+' or 'x' button
        if event and event.keysym != 'Return' and widget.cget('bg') == 'red':
            parent = widget.winfo_parent()  # Getting the parent widget of the widget as per mouse pointer position.
            wid = self.master.nametowidget(parent)  # Converting got widget string to actual widget instance
            wid = wid.winfo_parent()  # Getting the parent widget of above converted widget to actual instance
            wid = self.master.nametowidget(wid)  # Again, converting above got widget string to actual widget instance
            wid.destroy()  # Finally, the widget that we get is the frame which holds Entry and 'x' buttons. Removing that frame.

        else:  # If the widget is not '+' or 'x' button then it is definitely a Entry widget
            entry_widgets = self.GetEntryWidgets()  # Getting all the entry widgets available in right-mid section
            last_entry_text = entry_widgets[-1].get().split('-')  # Grabbing last entry widget

            # When the text in the last widget is not in "number-number" format
            if len(last_entry_text) <= 1 or (len(last_entry_text) == 2 and (not last_entry_text[0].isdigit() or not last_entry_text[1].isdigit())):
                messagebox.showerror('ERR', 'Page Start or Page End not given')

            # When Page Start > Page End
            elif len(last_entry_text) == 2 and int(last_entry_text[0]) > int(last_entry_text[1]):
                messagebox.showerror('ERR', 'Page Start must be less than Page End')

            else:  # When the text in text widget is in "number-number" format and Page Star < Page End
                self.row += 1  # Increasing row by 1 to place widget in right-mid-section
                var_text = f'{int(last_entry_text[1]) + 1}-'  # Inserting Page Start text by increasing 1 thant the previous Page Start
                self.MidWidget.AddButton.config(text='x', bg='red', activebackground='red')  # Changing '+' button > 'x' button and its bg color
                self.MidWidget = _Mid_Widgets(self.TextArea, self.row, self.AddNextWidget, var_text=var_text, entry_fg='black')  # Creating right-mid-section widgets
                self.TextArea.window_create(END, window=self.MidWidget.WholeFrame)  # Inserting the created right-mid-section widget at the end of TextArea widget

                self.MidWidget.Entry.IsDefault = False  # Setting IsDefault to False so the Entry widget does not treat recently added text as default
                self.MidWidget.Entry.Entry.focus()      # Focusing to the recently created Entry widget
                self.MidWidget.Entry.Entry.icursor(len(var_text))  # Placing cursor positing at the Entry widget to the end of Entry widget

                self.master.update()  # Updating the whole window
                self.TextArea.see('end')  # Scrolling TextArea to the bottom

    def GetEntryWidgets(self):
        '''
        Get the list of entry widgets that are in the mid-section
        '''

        entry_widgets = []

        for child in self.TextArea.winfo_children():
            for frame_child in child.winfo_children():
                for another_child in frame_child.winfo_children():
                    if isinstance(another_child, ttk.Entry):
                        entry_widgets.append(another_child)

        return entry_widgets

    def MouseWheelScroll(self, event=None):
        '''
        Scroll right-mid-section part when user scrolls using mouse wheel
        '''

        original_widget = self.master.winfo_containing(self.master.winfo_pointerx(), self.master.winfo_pointery())
        wid = 'scrolledtext' in [w[1:] for w in original_widget.winfo_parent().split('.')]
        widget = self.master.nametowidget(original_widget).winfo_parent()
        widget = self.master.nametowidget(widget)

        if wid or widget == self.MidInnerFrame2_1:
            shift = (event.state & 0x1) != 0
            scroll = -1 if event.delta > 0 else 1

            if shift is False:
                self.TextArea.yview_scroll(scroll, "units")

    def GetPdfPath(self, entry, style_name):
        '''
        Get pdf path when user clicks to browse button
        '''

        self.master.update()
        extension = [('PDF', '*.pdf')]

        if style_name == 'Original':  # When user clicks first Browse button
            path = filedialog.askopenfilename(defaultextension=extension, filetypes=extension)

        else:  # When user clicks second Browse button
            path = filedialog.asksaveasfilename(title='Save', filetypes=extension, defaultextension=extension)

        if path:
            entry.Entry.IsDefault = False
            entry.Entry.EntryStyle.configure(f'{style_name}.TEntry', foreground='black')
            entry.Entry.var.set(path)

    def GenerateButtonCommand(self):
        '''
        When user clicks Generate PDFs button
        '''

        self.OutputTextArea.config(state='normal')
        self.OutputTextArea.delete('1.0', 'end')

        entries_widgets = self.GetEntryWidgets()
        prefix = self.Prefix_Entry.var.get().strip()
        save_to_path = self.OutputPathEntry.Entry.var.get().strip()
        save_to_path_dir = os.path.dirname(save_to_path)
        original_path = self.OriginalSourceEntry.Entry.var.get().strip()

        for entry in entries_widgets:
            nums = entry.get().strip().split('-')

            if len(nums) <= 1 or (len(nums) == 2 and (not nums[0].isdigit() or not nums[1].isdigit())):
                if not nums[0].isdigit() or not nums[1].isdigit():
                    messagebox.showerror('ERR', 'Some page numbers are not properly inserted')
                    return

        if self.OriginalSourceEntry.Entry.IsDefault:
            messagebox.showerror('ERR', 'Pdf path that has to be splitted not provided')

        elif self.OutputPathEntry.Entry.IsDefault:
            messagebox.showerror('ERR', 'Path to store splitted pdf(s) not provided')

        elif os.path.exists(original_path) is False:
            messagebox.showerror('ERR', 'Original PDF path not exists')

        elif os.path.exists(save_to_path_dir) is False:
            messagebox.showerror('ERR', 'Destination PDF path not exists')

        elif self.Prefix_Entry.IsDefault:
            messagebox.showerror('ERR', 'Prefix name was expected')

        else:
            root_path = ''
            create_sub_dirs = messagebox.askyesno('Confirm?', 'Do you want to create directory to splitted PDFs ?')

            if create_sub_dirs:
                root_path = os.path.join(save_to_path, 'PDF Splitter')

                if not os.path.exists(root_path):
                    os.mkdir(root_path)

            page_nums = []
            entry_widgets = self.GetEntryWidgets()

            for entry in entry_widgets:
                x, y = entry.get().split('-')
                page_nums.append((int(x), int(y)))

            splitter = SplitPDF(original_path, save_to_path, prefix, page_nums, self.OutputFrame, self.OutputTextArea, root_path)

            thread = Thread(target=splitter.split)
            thread.start()

    def ClearOutput(self):
        '''
        Clear Output log message when user clicks Clear Button
        '''

        self.OutputTextArea.config(state='normal')
        self.OutputTextArea.delete('1.0', 'end')
        self.OutputTextArea.config(state='disabled')

        self.OutputFrame.pack_forget()

    def test(self):
        '''
        This the test case to test if all the widget is working or not

        Change the paths and test_page_nums as per your environment
        '''

        to_path = r"C:\Users\6292s\Downloads\Test"
        original_path = r"C:\Users\6292s\Downloads\Documents\Math Note.pdf"

        test_page_nums = ['1-21', '22-42', '43-60', '61-99', '100-141', '142-161', '162-169', '169-186',
                          '187-197', '198-209', '210-238', '239-255', '256-271', '271-301', '302-327',
                          '328-339', '340-347', '347-357', '358-361', '362-372', '373-393', '394-409',
                          '410-419', '420-433', '434-443', '444-449']

        # Inserting path in top first Entry widget
        self.OriginalSourceEntry.Entry.Entry.focus()
        self.OriginalSourceEntry.Entry.IsDefault = False
        self.OriginalSourceEntry.Entry.EntryStyle.configure('Original.TEntry', foreground='black')
        self.OriginalSourceEntry.Entry.var.set(original_path)

        # Inserting path in top second Entry widget
        self.OutputPathEntry.Entry.Entry.focus()
        self.OutputPathEntry.Entry.IsDefault = False
        self.OutputPathEntry.Entry.EntryStyle.configure('Output.TEntry', foreground='black')
        self.OutputPathEntry.Entry.var.set(to_path)

        # Inserting path in Prefix Entry widget
        self.Prefix_Entry.Entry.focus()
        self.Prefix_Entry.IsDefault = False
        self.Prefix_Entry.EntryStyle.configure('Prefix.TEntry', foreground='black')
        self.Prefix_Entry.var.set('Exercise')

        for page_num in test_page_nums:
            self.MidWidget.Entry.Entry.focus()
            self.MidWidget.Entry.IsDefault = False
            self.MidWidget.Entry.EntryStyle.configure(f'{self.row}.TEntry', foreground='black')
            self.MidWidget.Entry.var.set(page_num)

            if page_num != test_page_nums[-1]:
                self.AddNextWidget()

        self.GenerateButtonCommand()

    def ResourcePath(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or
            file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or
            file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    PDFSplitter()
