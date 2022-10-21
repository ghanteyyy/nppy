import os
import sys
import threading
from tkinter import *
import tkinter.ttk as ttk
from tkinter.font import Font
from tkinter import messagebox
from tkinter import filedialog
from tkinter import PhotoImage
from merger import Merger


class PdfMerger:
    def __init__(self):
        self.PDFs = dict()
        self.FrameNumber = 0
        self.IsEmpty = True
        self.extensions = ([('PDF', '*.pdf')])

        self.window = Tk()
        self.window.withdraw()
        self.window.title('PDF Merger')
        self.window.config(bg='#363636')

        self.AddImage = PhotoImage(file=self.ResourcePath('Add.png'))
        self.IconImage = PhotoImage(file=self.ResourcePath('icon.png'))
        self.MergeImage = PhotoImage(file=self.ResourcePath('Merge.png'))

        self.ListBoxFrame = Frame(self.window, bd=0, width=501, height=400, bg='#3c403d')
        self.ListBoxFrame.pack(padx=10, pady=10)
        self.ListBoxFrame.pack_propagate(False)
        self.PdfLists = Listbox(self.ListBoxFrame, width=1, height=1, fg='white', bg='#3c403d', bd=0, highlightbackground="#646464", highlightthickness=1, activestyle='none', font=Font(size=13, family='Lucida Console'))
        self.PdfLists.pack(side=LEFT, fill='both', expand=True)
        self.Scrollbar = ttk.Scrollbar(self.ListBoxFrame, orient='vertical', command=self.PdfLists.yview)

        self.AddMoreButton = Button(self.window, bg='#3c403d', activebackground='#3c403d', image=self.AddImage, bd=0, cursor='hand2', command=self.AddMorePDFs)
        self.AddMoreButton.place(in_=self.PdfLists, relx=0.86, rely=0.83)

        self.MergeButton = Button(self.window, bg='#363636', activebackground='#363636', image=self.MergeImage, bd=0, cursor='hand2', command=self.MergeButtonCommand)
        self.MergeButton.pack(pady=(0, 10), padx=10)

        self.ErrorLabel = Label(self.window, text='No PDFs yet', fg='white', bg='#3c403d', font=Font(size=20))
        self.GifLabel = Label(self.window, bg='#3c403d')

        self.GifFrames = [PhotoImage(file=self.ResourcePath('Merging.gif'),format = 'gif -index %i' %(i)) for i in range(31)]

        self.ShowScrollBar()
        self.window.after(0, self.InitialPosition)
        self.window.bind('<Control-a>', self.SelectAll)
        self.PdfLists.bind('<Button-3>', self.RightClick)
        self.window.bind('<Delete>', self.RightClickRemove)
        self.window.bind('<Control-o>', self.AddMorePDFs)
        self.PdfLists.bind('<Control-Button-1>', self.SetSelection)

        self.window.mainloop()

    def InitialPosition(self):
        '''
        Open the tkinter window at the center of the window
        '''

        self.window.update()
        self.window.iconphoto(False, self.IconImage)

        WindowWidth = self.window.winfo_width() // 2
        WindowHeight = self.window.winfo_height() // 2

        ScreenWidth = self.window.winfo_screenwidth() // 2
        ScreenHeight = self.window.winfo_screenheight() // 2

        x = ScreenWidth - WindowWidth
        y = ScreenHeight - WindowHeight

        self.window.geometry(f'+{x}+{y}')
        self.window.resizable(0, 0)

        if self.IsEmpty:
            self.ErrorLabel.place(in_=self.PdfLists, relx=0.4, rely=0.5)

        self.window.deiconify()

    def SetSelection(self, event):
        '''
        Select and deselect value in ListBox when
        holding control key and click to respective
        value.
        '''

        index = self.PdfLists.nearest(event.y)

        if index in self.PdfLists.curselection():
            self.PdfLists.selection_clear(index)

        else:
            self.PdfLists.selection_set(str(index))

    def SelectAll(self, event):
        '''
        Select all items in Listbox
        '''

        self.PdfLists.selection_set(0, END)

    def AddMorePDFs(self, event=None):
        '''
        Browse and add pdfs from the user preferred location
        '''

        files = filedialog.askopenfilenames(title='Select Files', defaultextension=self.extensions, filetypes=self.extensions)

        if files:
            if self.IsEmpty:
                # Remove Error Label
                self.IsEmpty = False
                self.ErrorLabel.place_forget()

            for file in files:  # Inserting pdfs name to the listbox
                basename = os.path.basename(file)

                if file not in self.PDFs.values():
                    self.PDFs.update({basename: file})
                    self.PdfLists.insert(END, basename)

    def MergeButtonCommand(self):
        '''
        Merge added pdfs when clicked merge button
        '''

        if len(self.PDFs) < 2:
            messagebox.showerror('ERR', 'Merging can only be done with 2 or more pdfs')

        else:
            output_path = filedialog.asksaveasfilename(title='Save', defaultextension=self.extensions, filetypes=self.extensions)

            if output_path:
                files = list(self.PDFs.values())

                self.Merger = Merger()

                self.MergeButton.config(state='disabled')
                self.AddMoreButton.config(state='disabled')

                self.GifLabel.place(in_=self.PdfLists, relx=0.32, rely=0.25)
                self.ShowGifAnimation()

                thread = threading.Thread(target=self.Merger.Merge, args=(output_path, files, self.PdfLists, self.window))
                thread.start()

    def RightClick(self, event):
        '''
        Show Right click menu when right clicked in ListBox
        '''

        x, y = self.window.winfo_pointerxy()
        RightClickMenu = Menu(self.window, tearoff=False)

        if self.PdfLists.selection_get():
            try:
                RightClickMenu.add_command(label='Remove', command=self.RightClickRemove)
                RightClickMenu.post(x, y)

            finally:
                RightClickMenu.grab_release()

    def RightClickRemove(self, event=None):
        '''
        Remove the selected item of listbox from
        right-click menu
        '''

        selections = reversed(self.PdfLists.curselection())

        for selection in selections:
            value = self.PdfLists.get(selection)
            self.PdfLists.delete(selection)
            self.PDFs.pop(value)

        if not self.PDFs:
            # Display Error label if there is no any PDFs
            self.IsEmpty = True
            self.ErrorLabel.place(in_=self.PdfLists, relx=0.4, rely=0.5)

    def ShowGifAnimation(self):
        '''
        Show buffering animation while pdfs being merged
        '''

        frame = self.GifFrames[self.FrameNumber]
        self.FrameNumber += 1

        if self.FrameNumber>30: #With this condition it will play gif infinitely
            self.FrameNumber = 0

        completed = self.Merger.IsFinished

        if completed:
            self.Merger.IsFinished = False
            self.GifLabel.place_forget()

            self.MergeButton.config(state='normal')
            self.AddMoreButton.config(state='normal')

            return

        self.GifLabel.configure(image=frame)
        self.AnimationTimer = self.window.after(20, self.ShowGifAnimation)

    def ShowScrollBar(self):
        '''
        Show ScrollBar when the contents of TreeView is
        more than the height of TreeView
        '''

        if  len(self.PdfLists.get(0, END)) > 22:
            self.Scrollbar.pack(side=RIGHT, padx=(2, 0), fill='y')
            self.PdfLists.config(yscrollcommand=self.Scrollbar.set)

            self.ScrollBarUpdateTimer = self.window.after(250, self.HideScrollBar)

        else:
            self.ScrollBarUpdateTimer = self.window.after(250, self.ShowScrollBar)

    def HideScrollBar(self):
        '''
        Hide ScrollBar when the contents of TreeView is
        less or equal than the height of TreeView
        '''

        if len(self.PdfLists.get(0, END)) <= 22:
            self.Scrollbar.pack_forget()
            self.ScrollBarUpdateTimer = self.window.after(250, self.ShowScrollBar)

        else:
            self.ScrollBarUpdateTimer = self.window.after(250, self.HideScrollBar)


    def ResourcePath(self, file_name):
        '''
        Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory
        '''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, 'assets', file_name)


if __name__ == '__main__':
    PdfMerger()
