import os
import sys
import string
import random
import pyperclip

try:  # Python 3
    from tkinter import *
    from tkinter import messagebox

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *
    import tkMessageBox as messagebox


class Password_Generator:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.resizable(0, 0)
        self.master.title('Password GENERATOR')
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))
        self.master.geometry(f'362x529+{self.master.winfo_screenwidth() // 2 - 362 // 2}+{self.master.winfo_screenheight() // 2 - 529 // 2}')

        self.font = ('Calibri', 12)
        self.title = Label(self.master, text='Password GENERATOR', font=('Calibri', 20))
        self.title.pack(pady=5)

        self.image_obj = PhotoImage(file=self.resource_path('included_files/title_image.png'))

        self.image_label = Label(self.master, image=self.image_obj)
        self.image_label.pack(pady=5)

        # Input box to enter the length of password
        self.number_box_var = StringVar()
        self.number_box = Entry(self.master, width=25, fg='grey', font=('Calibri', 12), justify='center', textvariable=self.number_box_var)
        self.number_box_var.set('Number of Character')
        self.number_box.pack(pady=5, ipady=2)

        self.check_box_frame = Frame(self.master)
        self.check_box_items = ['UPPERCASE', 'LOWERCASE', 'NUMBERS', 'SPECIAL CHARACTERS', 'ALL']   # Options for generating password

        # Variables to hold the selected option
        self.upper_var, self.lower_var, self.num_var, self.special_var, self.all_var = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        self.vars = [self.upper_var, self.lower_var, self.num_var, self.special_var, self.all_var]

        for index, value in enumerate(self.check_box_items):  # Creating Checkbuttons according to name stored in "check_box_items" and variables to hold selected options stored in "var"
            self.check_box = Checkbutton(self.check_box_frame, text=value, anchor='w', bd=0, variable=self.vars[index], font=self.font)
            self.check_box.grid(row=index, column=0, sticky='w')

        self.check_box_frame.pack(pady=5)

        # Buttons to generate random password
        self.generate_password_button = Button(self.master, text='Generate Password', bg='Green', fg='white', activeforeground='white', activebackground='Green', font=self.font, relief=FLAT, command=self.generate_button)
        self.generate_password_button.pack(pady=5)

        # Show random generated password
        self.password_label = Label(self.master, font=('Calibri', 20))
        self.copy_button = Button(self.master, text='Copy', width=6, bg='Green', fg='white', activeforeground='white', activebackground='Green', font=self.font, relief=FLAT, command=self.copy_to_clipboard)

        self.master.bind('<Control-c>', self.copy_to_clipboard)
        self.master.bind('<Control-C>', self.copy_to_clipboard)
        self.master.bind('<Return>', lambda e: self.generate_button())
        self.master.bind('<Button>', self.bind_keys)

        self.master.after(0, self.master.deiconify)
        self.master.mainloop()

    def bind_keys(self, event):
        get = self.number_box_var.get().strip()

        if event.widget == self.number_box and get == 'Number of Character':
            self.number_box_var.set('')
            self.number_box.config(fg='black')

        elif event.widget in [self.master, self.image_label, self.title, self.check_box_frame, self.password_label] and not get:
            self.number_box_var.set('Number of Character')
            self.number_box.config(fg='grey')

            self.master.focus()

    def generate_password(self, string_combination, lengths):
        return ''.join([random.choice(string_combination) for lenght in range(lengths)])

    def copy_to_clipboard(self, event=None):
        '''Copy Generated Random Password to the clipboard'''

        text = self.password_label['text']

        if text:
            pyperclip.copy(text)
            self.copy_button['text'] = 'Copied!'
            self.master.after(1000, lambda: self.copy_button.config(text='Copy'))

    def generate_button(self):
        try:
            string_combination = ''
            get_var = [var.get() for var in self.vars]
            lengths = int(self.number_box_var.get().strip())
            string_combo = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation, string.printable[:94]]

            for index, value in enumerate(get_var):
                if value == 1:
                    string_combination += string_combo[index]

            password = self.generate_password(string_combination, lengths)
            self.password_label.config(text=password)
            self.password_label.pack()

            self.master.geometry(f'362x546')
            self.copy_button.pack(side=RIGHT)

        except ValueError:
            messagebox.showerror('Invalid Number', 'Input Valid Number')

        except IndexError:
            messagebox.showerror('No Option', 'No option selected')

    def resource_path(self, relative_path):
        """ Get absolute path to resource from temporary directory

        In development:
            Gets path of photos that are used in this script like in icons and title_image from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of photos that are used in this script like in icons and title image from temporary directory"""

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path in _MEIPASS

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Password_Generator()
