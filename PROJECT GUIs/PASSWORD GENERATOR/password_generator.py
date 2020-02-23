import string
import random
import pyperclip
import PIL.Image
import PIL.ImageTk

try:
    from tkinter import *
    from tkinter import messagebox

except (ImportError, ModuleNotFoundError):
    from Tkinter import *


def copy_to_clipboard(event=None):
    '''Copy Generated Random Password to the clipboard'''

    pyperclip.copy(pass_word['text'])
    copy_btn['text'] = 'Copied!'
    root.after(2000, lambda: copy_btn.config(text='Copy'))


def enter(event=None):
    '''Deletes "Number of Character" text when mouse cursor is within the input box.'''

    number_box.focus_set()

    if number_box.get() == 'Number of Character':
        number_box.delete(0, END)

    number_box['fg'] = 'black'


def leave(event=None):
    '''Inserts "Number of Characters" when user leaves input box and input box has nothing in it'''

    if len(number_box.get()) == 0:
        number_box.insert(0, 'Number of Character')
        number_box['fg'] = 'grey'

        root.focus_set()


def generate_password():
    '''Generate random password and show to the user'''

    possible_combination = [string.ascii_uppercase, string.ascii_lowercase, string.digits, string.punctuation, string.printable[:-6]]
    gets = [var_up.get(), var_lo.get(), var_nu.get(), var_sp.get(), var_al.get()]
    index = [i for i, x in enumerate(gets) if x == 1]
    user_combination = list(set(''.join([possible_combination[i] for i in index])))

    try:
        pass_word['text'] = ''.join([random.choice(user_combination) for i in range(int(number_box.get()))])   # Generating random password with all possible pythonic ways
        pass_word.pack()
        root.geometry(f'362x546')
        copy_btn.pack(side=RIGHT)

        root.focus_set()

    except ValueError:
        messagebox.showerror('Invalid Number', 'Input Valid Number')

    except IndexError:
        messagebox.showerror('No Option', 'No option selected')


root = Tk()
root.withdraw()
root.after(0, root.deiconify)
root.resizable(0, 0)
root.title('Password GENERATOR')
root.iconbitmap('included files/icon.ico')
root.geometry(f'362x529+{root.winfo_screenwidth() // 2 - 362 // 2}+{root.winfo_screenheight() // 2 - 529 // 2}')

title = Label(root, text='Password GENERATOR', font=('Calibri', 20))
title.pack(pady=5)

image_obj = PIL.ImageTk.PhotoImage(PIL.Image.open('included files/apg.png'))
image = Label(root, image=image_obj)
image.pack(pady=5)

# Input box to enter the length of password
number_box = Entry(root, width=25, fg='grey', font=('Calibri', 12), justify='center')
number_box.insert(END, 'Number of Character')
number_box.pack(pady=5)

check_box_frame = Frame(root)
check_box_items = ['UPPERCASE', 'LOWERCASE', 'NUMBERS', 'SPECIAL CHARACTERS', 'ALL']   # Options for generating password

# Variables to hold the selected option
var_up, var_lo, var_nu, var_sp, var_al = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
Var = [var_up, var_lo, var_nu, var_sp, var_al]

for index, value in enumerate(check_box_items):  # Creating Checkbuttons according to name stored in "check_box_items" and variables to hold selected options stored in "var"
    check_box = Checkbutton(check_box_frame, text=value, anchor='w', bd=0, variable=Var[index], font=('Calibri', 12))
    check_box.grid(row=index, column=0, sticky='w')

check_box_frame.pack(pady=5)

# Buttons to generate random password
btn = Button(root, text='Generate Password', bg='Green', fg='white', activeforeground='white', activebackground='Green', font=('Calibri', 12), relief=FLAT, command=generate_password)
btn.pack(pady=5)

# Show random generated password
pass_word = Label(root, font=('Calibri', 20))
copy_btn = Button(root, text='Copy', width=6, bg='Green', fg='white', activeforeground='white', activebackground='Green', font=('Calibri', 12), relief=FLAT, command=copy_to_clipboard)

number_box.bind('<Enter>', enter)
number_box.bind('<Leave>', leave)

root.mainloop()
