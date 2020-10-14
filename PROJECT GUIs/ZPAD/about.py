from tkinter import *
import tkinter.ttk as ttk
import include
import search


class About:
    def __init__(self, master):
        self.master = master
        self.author_page_link = 'http://github.com/ghanteyyy'
        self.source_code_link = 'http://github.com/ghanteyyy/Project GUIs/ZPAD'

        self.top_level = Toplevel(self.master)
        self.top_level.grab_set()
        self.top_level.withdraw()
        self.initial_position()
        self.top_level.after(0, self.top_level.deiconify)
        self.top_level.title('About')
        self.top_level.iconbitmap(include.resource_path('included_files\\transparent.ico'))

        self.search = search.Search(self.top_level)
        self.description_frame = Frame(self.top_level, bg='white')
        self.build_label = Label(self.description_frame, text='Build:', bg='white')
        self.build_number = Label(self.description_frame, text='1.0.0', bg='white')

        self.author_label = Label(self.description_frame, text='Author:', bg='white')
        self.author_name_button = Button(self.description_frame, text='\t\tghanteyyy', bg='white', activebackground='white', activeforeground='black', fg='black', bd=0, command=self.author_page)

        self.source_code_label = Label(self.description_frame, text='Source Code:', bg='white')
        self.source_code_button = Button(self.description_frame, text='\t\tZPAD', bg='white', activebackground='white', activeforeground='black', fg='black', bd=0, command=self.source_code_page)

        self.build_label.grid(row=0, column=0, sticky='w')
        self.build_number.grid(row=0, column=1, sticky='e')
        self.author_label.grid(row=1, column=0, sticky='w')
        self.author_name_button.grid(row=1, column=1, sticky='e')
        self.source_code_label.grid(row=2, column=0, sticky='w')
        self.source_code_button.grid(row=2, column=1, sticky='e')
        self.description_frame.pack(pady=20)

        self.show_link_frame = Frame(self.top_level)
        self.link_label = Label(self.show_link_frame, bg='white')
        self.link_label.grid(row=0, column=1)
        self.show_link_frame.pack(side=LEFT)

        self.ok_frame = Frame(self.top_level)
        self.ok_button = ttk.Button(self.ok_frame, text='Ok', command=self.top_level.destroy)
        self.ok_button.grid(row=0, column=0)
        self.ok_frame.pack(side=RIGHT)

        self.author_name_button.bind('<Enter>', lambda e: self.enter(self.author_name_button, self.author_page_link))
        self.author_name_button.bind('<Leave>', lambda e: self.leave(self.author_name_button))
        self.source_code_button.bind('<Enter>', lambda e: self.enter(self.source_code_button, self.source_code_link))
        self.source_code_button.bind('<Leave>', lambda e: self.leave(self.source_code_button))
        self.author_label.bind('<Enter>', lambda e: self.enter(self.author_label, self.author_page_link))
        self.author_label.bind('<Leave>', lambda e: self.leave(self.author_label))
        self.source_code_label.bind('<Enter>', lambda e: self.enter(self.source_code_label, self.source_code_link))
        self.source_code_label.bind('<Leave>', lambda e: self.leave(self.source_code_label))

        self.author_label.bind('<Button-1>', self.author_page)
        self.source_code_label.bind('<Button-1>', self.source_code_page)
        self.top_level.bind('<Return>', lambda e: self.top_level.destroy())
        self.top_level.bind('<Escape>', lambda e: self.top_level.destroy())
        self.top_level.config(bg='white')
        self.top_level.mainloop()

    def initial_position(self):
        '''Set initial position of the about window'''

        width, height = 400, 130
        master_width, master_height = self.master.winfo_width() // 2, self.master.winfo_height() // 2
        offset_x, offset_y = self.master.winfo_x() + master_width - width // 2, self.master.winfo_y() + master_height - height // 2
        self.top_level.geometry(f'{width}x{height}+{offset_x}+{offset_y}')
        self.top_level.resizable(0, 0)
        self.top_level.after(10, include.hide_or_show_maximize_minimize(self.top_level).hide_minimize_maximize)

    def enter(self, button, link):
        '''When the cursor enters the boundary of author-name and source-code link'''

        self.link_label.config(text=link, fg='white', bg='grey')
        button.config(fg='red', activeforeground='red', cursor='hand2')

    def leave(self, button):
        '''When the cursor leaves the boundary of author-name and source-code link'''

        self.link_label.config(text='', bg='white')
        button.config(fg='black', activeforeground='black')

    def author_page(self, event=None):
        '''Open author's Git-hub page '''

        self.top_level.after(250, lambda: self.search.open_link(self.author_page_link))

    def source_code_page(self, event=None):
        '''Open source-code Git-hub page '''

        self.top_level.after(250, lambda: self.search.open_link(self.source_code_link))
