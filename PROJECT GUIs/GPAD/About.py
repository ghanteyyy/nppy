from tkinter import *
import tkinter.ttk as ttk
import Include
import Search


class About:
    def __init__(self, master):
        self.BuildNumber = '2.4.1'

        self.master = master
        self.AuthorAddress = 'http://github.com/ghanteyyy'
        self.SourceCodeAddress = 'https://github.com/ghanteyyy/nppy/tree/master/PROJECT GUIs/GPAD'

        self.AboutWindow = Toplevel(self.master)
        self.AboutWindow.transient(self.master)
        self.AboutWindow.grab_set()
        self.AboutWindow.withdraw()
        self.WindowInitialPosition()
        self.AboutWindow.after(0, self.AboutWindow.deiconify)
        self.AboutWindow.title('About')
        self.AboutWindow.iconbitmap(Include.resource_path('transparent.ico'))

        self.search = Search.Search(self.AboutWindow)
        self.DescriptionFrame = Frame(self.AboutWindow, bg='white')
        self.BuildLabel = Label(self.DescriptionFrame, text='Build:', bg='white')
        self.BuildNumberLabel = Label(self.DescriptionFrame, text=self.BuildNumber, bg='white')

        self.AuthorLabel = Label(self.DescriptionFrame, text='Author:', bg='white')
        self.AuthorNameButton = Button(self.DescriptionFrame, text='\t\tghanteyyy', bg='white', activebackground='white', activeforeground='black', fg='black', bd=0, command=self.GoToAuthorAddress)

        self.SourceCodeLabel = Label(self.DescriptionFrame, text='Source Code:', bg='white')
        self.SourceCodeButton = Button(self.DescriptionFrame, text='\t\tGPAD', bg='white', activebackground='white', activeforeground='black', fg='black', bd=0, command=self.GoToSourceCodeAddress)

        self.BuildLabel.grid(row=0, column=0, sticky='w')
        self.BuildNumberLabel.grid(row=0, column=1, sticky='e')
        self.AuthorLabel.grid(row=1, column=0, sticky='w')
        self.AuthorNameButton.grid(row=1, column=1, sticky='e')
        self.SourceCodeLabel.grid(row=2, column=0, sticky='w')
        self.SourceCodeButton.grid(row=2, column=1, sticky='e')
        self.DescriptionFrame.pack(pady=20)

        self.ShowLinkFrame = Frame(self.AboutWindow)
        self.LinkLabel = Label(self.ShowLinkFrame, bg='white')
        self.LinkLabel.grid(row=0, column=1)
        self.ShowLinkFrame.pack(side=LEFT)

        self.OkStyle = ttk.Style()
        self.OkStyle.configure('btn.TButton', background='white')
        self.OkFrame = Frame(self.AboutWindow, bg='white')
        self.OkButton = ttk.Button(self.OkFrame, text='Ok', style='btn.TButton', command=self.AboutWindow.destroy)
        self.OkButton.grid(row=0, column=0)
        self.OkFrame.pack(side=RIGHT)

        self.AuthorNameButton.bind('<Enter>', lambda e: self.Enter(self.AuthorNameButton, self.AuthorAddress))
        self.AuthorNameButton.bind('<Leave>', lambda e: self.Leave(self.AuthorNameButton))
        self.SourceCodeButton.bind('<Enter>', lambda e: self.Enter(self.SourceCodeButton, self.SourceCodeAddress))
        self.SourceCodeButton.bind('<Leave>', lambda e: self.Leave(self.SourceCodeButton))
        self.AuthorLabel.bind('<Enter>', lambda e: self.Enter(self.AuthorLabel, self.AuthorAddress))
        self.AuthorLabel.bind('<Leave>', lambda e: self.Leave(self.AuthorLabel))
        self.SourceCodeLabel.bind('<Enter>', lambda e: self.Enter(self.SourceCodeLabel, self.SourceCodeAddress))
        self.SourceCodeLabel.bind('<Leave>', lambda e: self.Leave(self.SourceCodeLabel))

        self.AuthorLabel.bind('<Button-1>', self.GoToAuthorAddress)
        self.SourceCodeLabel.bind('<Button-1>', self.GoToSourceCodeAddress)
        self.AboutWindow.bind('<Return>', lambda e: self.AboutWindow.destroy())
        self.AboutWindow.bind('<Escape>', lambda e: self.AboutWindow.destroy())
        self.AboutWindow.config(bg='white')
        self.AboutWindow.mainloop()

    def WindowInitialPosition(self):
        '''Set initial position of the about window'''

        width, height = 460, 130
        master_width, master_height = self.master.winfo_width() // 2, self.master.winfo_height() // 2
        offset_x, offset_y = self.master.winfo_x() + master_width - width // 2, self.master.winfo_y() + master_height - height // 2
        self.AboutWindow.geometry(f'{width}x{height}+{offset_x}+{offset_y}')
        self.AboutWindow.resizable(0, 0)

    def Enter(self, button, link):
        '''When the cursor enters the boundary of author-name and source-code link'''

        self.LinkLabel.config(text=link, fg='white', bg='grey')
        button.config(fg='red', activeforeground='red', cursor='hand2')

    def Leave(self, button):
        '''When the cursor leaves the boundary of author-name and source-code link'''

        self.LinkLabel.config(text='', bg='white')
        button.config(fg='black', activeforeground='black')

    def GoToAuthorAddress(self, event=None):
        '''Open author's Git-hub page '''

        self.AboutWindow.after(250, lambda: self.search.OpenLink(self.AuthorAddress))

    def GoToSourceCodeAddress(self, event=None):
        '''Open source-code Git-hub page '''

        self.AboutWindow.after(250, lambda: self.search.OpenLink(self.SourceCodeAddress))
