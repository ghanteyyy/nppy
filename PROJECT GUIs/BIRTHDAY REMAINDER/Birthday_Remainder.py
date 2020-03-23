import os
import PIL.Image
import PIL.ImageTk
from winsound import MessageBeep

try:  # Python 3
    from tkinter import *
    from tkinter.ttk import Combobox

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *
    from ttk import Combobox

month_number = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


def show_info(message, pos_x, pos_y):
    '''Display result to user'''

    error_frame = Frame(root, bg='dark green')  # Creating "frame" object
    label_error_message = Label(error_frame, text=message, font=('Courier', 20), fg='white', bg='dark green')  # Creating "label" object
    label_error_message.grid(row=0, column=0)  # Packing "label" object
    error_frame.place(x=pos_x, y=pos_y)  # Placing "frame" to the given coordinates

    root.update()  # Updating whole window
    root.after(1000, label_error_message.grid_forget)   # Removing "label" object after 1 second. 1000ms = 1 sec


def check_duplicate(name, date):
    '''Check if name and date provided exists in file'''

    with open('details.txt', 'r') as details:  # Opening file in reading mode
        if f'{name.ljust(50)}{date}\n' in details.readlines():   # Checking if the given name and date exists in file
            return True  # Returing True if given name and date exists in file

        return False  # If not returning False


def sort_details():
    '''Sort contents of file alphabetically'''

    with open('details.txt', 'r+') as read_write:   # Opening files in both reading and writing mode
        lines = read_write.readlines()   # Reading contents of file
        lines.sort()   # Sorting the contents alphabetically
        read_write.seek(0)  # Placing the cursor back to the starting of the file

        # Writing sorted contents to the file line by line
        for line in lines:
            read_write.write(line)


def check_for_file():
    '''Create "details.txt" if not exists'''

    if not os.path.exists('details.txt'):  # If "details.txt" not exists
        with open('details.txt', 'w'):   # Creating "details.txt"
            pass


def add_info(event=None):
    '''Get value from user and add/delete them'''

    name, month, date = name_box.get().strip().upper(), month_box.get(), date_box.get()   # Getting content from GUI

    if len(name) == 0 or len(month) == 0:  # Check if the field is empty
        MessageBeep()  # Playing error sound
        show_info(message='Empty Field', pos_x=35, pos_y=415)  # Displaying error message to the user
        name_box.delete(0, END)

    elif month not in month_number or not date.isdigit() or date == 'Select Date' or month == 'Select Month':  # Check entered date is not digit or alphabets
        MessageBeep()  # Playing error sound
        show_info(message='Invalid Date', pos_x=25, pos_y=415)  # Displaying error message to the user

    elif int(date) > 32 or int(date) == 0:  # Check entered date is integer and between 01-32
        MessageBeep()  # Playing error sound
        show_info(message='Invalid Date', pos_x=25, pos_y=415)  # Displaying error message to the user

    elif var.get() != 1 and var.get() != 2:  # Check if no buttons are selected
        MessageBeep()  # Playing error sound
        show_info(message='No button\nselected', pos_x=50, pos_y=400)  # Displaying error message to the user

    else:   # If no errors then preceding to save the details in text file
        check_for_file()   # Checking if file exists where we can store data

        date = '{}-{}'.format(month_number[month].zfill(2), date.zfill(2))   # Formatting date

        if var.get() == 1:  # Check if add button is selected
            if check_duplicate(name, date):  # Check if input date already exists
                MessageBeep()  # Playing error sound
                show_info(message='Details Exists', pos_x=12, pos_y=415)

            else:  # If not already in file
                with open('details.txt', 'a') as append:   # Opening file for editing
                    append.write('{}{}\n'.format(name.ljust(50), date))   # Writing to the file

                show_info(message='Details Added', pos_x=17, pos_y=415)   # Showing details added info

        elif var.get() == 2:  # Check if delete button is selected
            if not check_duplicate(name, date):  # Check if entered value not in file
                MessageBeep()  # Playing error sound
                show_info(message='Invalid Details', pos_x=2, pos_y=415)   # Showing invalid info

            else:  # Check if entered value in file
                with open('details.txt', 'r+') as read_write_details:   # opening file for both reading and writing
                    lines = read_write_details.readlines()  # Reading file
                    lines.remove('{}{}\n'.format(name.ljust(50), date))   # Removing the targeted value from "lines" list
                    read_write_details.seek(0)   # Placing cursor to the starting of the file

                    for line in lines:  # Writing everything except details entered by user
                        read_write_details.write(line)   # Writing to the file

                    read_write_details.truncate()

                show_info(message='Details Deleted', pos_x=2, pos_y=415)   # Showing deletion info

        sort_details()   # Sorting file


def main():
    '''Starting script'''

    global root, name_box, var, date_box, label_birthday_quote, month_box

    root = Tk()
    root.withdraw()  # Minimizing the window
    root.after(0, root.deiconify)   # Restoring window after 0 seconds
    root.resizable(0, 0)  # Making window unresizable
    root.iconbitmap('included Files/icon.ico')   # Inserting icon to the window
    root.title('Birthday Remainder')  # Setting window's title name
    root.geometry(f'426x500+{root.winfo_screenwidth() // 2 - 426 // 2}+{root.winfo_screenheight() // 2 - 500 // 2}')

    # Inserting image
    birthday_quote_frame = Frame(root)
    birthday_quote_image = PIL.ImageTk.PhotoImage(PIL.Image.open('included Files/image.jpg', 'r'))
    label_birthday_quote = Label(birthday_quote_frame, image=birthday_quote_image)
    label_birthday_quote.grid(row=0, column=0)
    birthday_quote_frame.place(x=0, y=0)

    # Insert Name label and entry field
    label_entry_frame = Frame(root, bg='dark green')
    name_label = Label(label_entry_frame, text='Name', fg='white', font=('Courier', 12), bg='dark green')
    name_box = Entry(label_entry_frame, width=30)
    name_label.grid(row=0, column=0)
    name_box.grid(row=0, column=1, padx=30, pady=20)

    # Insert date of birth label
    birthday_label = Label(label_entry_frame, text='Date of Birth', fg='white', font=('Courier', 12), bg='dark green')
    birthday_label.grid(row=1, column=0)
    label_entry_frame.place(x=70, y=240)

    # Options to select month and dates
    combo_box_frame = Frame(root, bg='dark green')
    month_box = Combobox(combo_box_frame, values=[month for month in month_number], width=13)
    month_box.set('Select Month')
    month_box.grid(row=0, column=0)

    date_box = Combobox(combo_box_frame, values=[i for i in range(1, 32)], width=10)
    date_box.set('Select Date')
    date_box.grid(row=0, column=1, padx=5)

    combo_box_frame.place(x=235, y=300)

    # Insert radiobuttons add or delete
    var = IntVar()
    radio_frame = Frame(root, bg='dark green')
    add_radio_button = Radiobutton(radio_frame, text='Add', fg='#000000', activebackground='dark green', font=('Courier', 12), bg='dark green', value=1, variable=var, disabledforeground='black')
    delete_radio_button = Radiobutton(radio_frame, text='Delete', fg='#000000', activebackground='dark green', font=('Courier', 12), bg='dark green', value=2, variable=var, disabledforeground='black')
    add_radio_button.grid(row=0, column=0)
    delete_radio_button.grid(row=0, column=1)
    radio_frame.place(x=255, y=360)

    # Insert submit button
    button_frame = Frame(root)
    submit_button = Button(button_frame, text='SUBMIT', fg='white', bg='#039e05', activebackground='#039e05', font=('Courier', 12), width=16, height=3, relief=RAISED, command=add_info)
    submit_button.grid(row=2, column=0)
    button_frame.place(x=250, y=400)

    # Bind keys
    name_box.bind_class('<Return>', add_info)
    date_box.bind('<Return>', add_info)
    name_box.bind('<Enter>', lambda e: name_box.focus_set())
    name_box.bind('<Leave>', lambda e: birthday_label.focus_set())

    root.config(bg='dark green')
    root.mainloop()


if __name__ == '__main__':
    main()
