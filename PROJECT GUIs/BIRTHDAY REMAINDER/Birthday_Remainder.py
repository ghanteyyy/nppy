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

    error_frame = Frame(root, bg='dark green')
    label_error_message = Label(error_frame, text=message, font=('Courier', 20), fg='white', bg='dark green')
    label_error_message.grid(row=0, column=0)
    error_frame.place(x=pos_x, y=pos_y)

    root.update()
    root.after(1000, label_error_message.grid_forget)


def check_duplicate(name, date):
    '''Check if name and date provided is already in file or not'''

    with open('details.txt', 'r') as details:
        if f'{name.ljust(50)}{date}\n' in details.readlines():
            return True

        return False


def sort_details():
    '''Sort details alphabetically'''

    with open('details.txt', 'r+') as read_write:
        lines = read_write.readlines()
        lines.sort()
        read_write.seek(0)

        for line in lines:
            read_write.write(line)


def add_info(event=None):
    '''Get value from user and add/delete them'''

    get_values = [name_box.get().strip().upper(), month_box.get(), date_box.get()]

    if len(get_values[0]) == 0 or len(get_values[1]) == 0:  # Check if the field is empty
        MessageBeep()
        show_info(message='Empty Field', pos_x=35, pos_y=415)
        name_box.delete(0, END)

    elif get_values[1] not in month_number or not get_values[-1].isdigit() or get_values[-1] == 'Select Date' or get_values[1] == 'Select Month':  # Check entered date is not digit or alphabets
        MessageBeep()
        show_info(message='Invalid Date', pos_x=25, pos_y=415)

    elif int(get_values[-1]) > 32 or int(get_values[-1]) == 0:  # Check entered date is integer and between 01-32
        MessageBeep()
        show_info(message='Invalid Date', pos_x=25, pos_y=415)

    elif var.get() != 1 and var.get() != 2:  # Check if no buttons are selected
        MessageBeep()
        show_info(message='No button\nselected', pos_x=50, pos_y=400)

    else:
        date = '{}-{}'.format(month_number[get_values[1]].zfill(2), get_values[-1].zfill(2))

        if var.get() == 1:  # Check if add button is selected
            if check_duplicate(get_values[0], date):  # Check if input date already exists
                MessageBeep()
                show_info(message='Details Exists', pos_x=12, pos_y=415)

            else:  # If not already in file
                with open('details.txt', 'a') as append:
                    append.write('{}{}\n'.format(get_values[0].ljust(50), date))

                show_info(message='Details Added', pos_x=17, pos_y=415)

        elif var.get() == 2:  # Check if delete button is selected
            if not check_duplicate(get_values[0], date):  # Check if entered value not in file
                MessageBeep()
                show_info(message='Invalid Details', pos_x=2, pos_y=415)

            else:  # Check if entered value in file
                with open('details.txt', 'r+') as read_write_details:
                    lines = read_write_details.readlines()  # Reading file
                    lines.remove('{}{}\n'.format(get_values[0].ljust(50), date))
                    read_write_details.seek(0)

                    for line in lines:  # Writing everything except details entered by user
                        read_write_details.write(line)

                    read_write_details.truncate()

                show_info(message='Details Deleted', pos_x=2, pos_y=415)

    sort_details()


def main():
    '''Main function of the script'''

    global root, name_box, var, date_box, label_birthday_quote, month_box

    root = Tk()
    root.withdraw()
    root.after(0, root.deiconify)
    root.resizable(0, 0)
    root.iconbitmap('icon.ico')
    root.title('Birthday Remainder')
    root.geometry(f'426x500+{root.winfo_screenwidth() // 2 - 426 // 2}+{root.winfo_screenheight() // 2 - 500 // 2}')

    # Inserting image
    birthday_quote_frame = Frame(root)
    birthday_quote_image = PIL.ImageTk.PhotoImage(PIL.Image.open('image.jpg', 'r'))
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

    date_box = Combobox(combo_box_frame, values=[i for i in range(1, 33)], width=10)
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
    try:
        if not os.path.exists('details.txt'):
            with open('details.txt', 'w'):
                pass

        main()

    except FileNotFoundError:
        main()
