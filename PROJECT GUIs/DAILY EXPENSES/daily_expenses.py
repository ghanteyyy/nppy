import os
import time
import winsound
from tkinter import *


def enter(widget, condition):
    '''REMOVES ITEMS OR PRICE when user clicks on any ENTRY widget'''

    widget.focus()

    if widget.get() == condition:    # Delete 'ITEMS' or 'PRICE' if exists in any ENTRY widget
        widget.delete(0, END)

    widget.config(fg='black', highlightcolor='blue', highlightbackground='blue', highlightthickness=2)


def leave(widget, condition):
    '''ADDS ITEMS OR PRICE when user submits nothing on any ENTRY widget'''

    if len(widget.get().strip()) == 0:    # ADDING 'ITEMS' or 'PRICE' if user provide empty fields in any ENTRY widget
        widget.delete(0, END)
        widget.insert(END, condition)
        widget.config(fg='grey', highlightcolor='blue', highlightbackground='blue', highlightthickness=2)

        root.focus()


def hightlight_errors(*widgets):
    winsound.MessageBeep()

    for widget in widgets:
        widget.config(fg='red', highlightbackground='red')


def submit_command():
    '''Command when user clicks submit button'''

    TIME = ' '.join(time.ctime(time.time())[:10].split())
    get_item = items_box.get().title()     # Getting input from items_box widget
    get_price = price_box.get()     # Getting input from price_box widget

    if (len(get_item.strip()) == 0 or get_item == 'Items') and not get_price.isdigit():
        hightlight_errors(items_box, price_box)

    elif len(get_item.strip()) == 0 or get_item == 'Items':
        hightlight_errors(items_box)

    elif not get_price.isdigit():
        hightlight_errors(price_box)

    else:
        if not os.path.exists('daily_expenses.txt'):    # If daily_expenses.txt does not exists then creating it
            with open('daily_expenses.txt', 'w'):
                pass

        with open('daily_expenses.txt', 'r+') as rf:   # Reading files
            lines = rf.readlines()

            in_lines = [line for line in lines if get_item in line]    # Storing if input of "get_item" is already in a file

            if in_lines:  # if input of "get_item" is already in a file then adding price stored in a file and of value stored in "get_price" variable
                write = '{} >> {} >> Rs. {}\n'.format(TIME, get_item, int(in_lines[0].split()[-1]) + int(get_price))

                lines[lines.index(in_lines[0])] = write

                with open('daily_expenses.txt', 'w') as wf:   # Writting everything again to the file
                    for line in lines:
                        wf.write(line)

            else:   # Writing inputs to file if not already exists in a file
                write = f'{TIME}\t >> {get_item} >> Rs. {get_price}\n'
                rf.write(write)

        write_to_text_box()   # Calling function

        items_box.delete(0, END)  # Removing value from "items_box" after adding everything to the file
        price_box.delete(0, END)  # Removing value from "price_box" after adding everything to the file

        items_box.insert(END, 'ITEMS')     # Inserting 'ITEMS' again to the "items_box"
        price_box.insert(END, 'PRICE')     # Inserting 'PRICE' again to the "price_box"

        items_box.config(fg='grey')   # Also configuring text color to "grey"
        price_box.config(fg='grey')   # Also configuring text color to "grey"

        root.focus()


def center_the_text(text, color):
    display_box.config(state=NORMAL)
    display_box.config(fg=color)
    display_box.tag_configure('center', justify='center')
    display_box.insert('end', text, 'center')
    display_box.config(state=DISABLED)


def write_to_text_box():
    '''Display content that are stored in daily_expenses.txt'''

    display_box.config(state=NORMAL)
    display_box.delete('1.0', END)
    display_box.config(state=DISABLED)

    with open('daily_expenses.txt', 'r') as rf:
        lines = rf.readlines()

        for line in lines:
            center_the_text(line, 'black')


def preload():
    '''Display content of a file when program loads for the first time'''

    if not os.path.exists('daily_expenses.txt') or os.path.getsize('daily_expenses.txt') == 0:
        center_the_text('Your Expenses will be displayed here', 'grey')

    else:
        write_to_text_box()


root = Tk()
root.resizable(0, 0)
root.title('DAILY EXPENSES')
root.iconbitmap('included files/icon.ico')
root.geometry(f'448x570+{root.winfo_screenwidth() // 2 - 448 // 2}+{root.winfo_screenheight() // 2 - 570 // 2}')

items_box = Entry(root, width=70, fg='grey', highlightbackground='blue', highlightthickness=2, justify=CENTER)
items_box.insert(END, 'ITEMS')
items_box.grid(row=0, column=0, ipady=7, padx=10, pady=10)

price_box = Entry(root, width=70, fg='grey', highlightbackground='blue', highlightthickness=2, justify=CENTER)
price_box.insert(END, 'PRICE')
price_box.grid(row=1, column=0, ipady=7, padx=10, pady=5)

display_box = Text(root, width=52, fg='black', highlightbackground='blue', highlightthickness=2, state=DISABLED, cursor='arrow')
display_box.grid(row=2, column=0, pady=10)

submit_box = Button(root, text='SUBMIT', width=59, bg='green', fg='white', activebackground='green', activeforeground='white', command=submit_command)
submit_box.grid(row=3, column=0, ipady=10, padx=10)

items_box.bind('<Return>', lambda e: submit_command())
price_box.bind('<Return>', lambda e: submit_command())
items_box.bind('<Enter>', lambda e: enter(items_box, 'ITEMS'))
items_box.bind('<Leave>', lambda e: leave(items_box, 'ITEMS'))
price_box.bind('<Enter>', lambda e: enter(price_box, 'PRICE'))
price_box.bind('<Leave>', lambda e: leave(price_box, 'PRICE'))

preload()

root.mainloop()
