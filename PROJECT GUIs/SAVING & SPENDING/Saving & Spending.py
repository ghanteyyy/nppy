import os
import winsound
import PIL.Image
import PIL.ImageTk
import collections

try:  # Python 3
    from tkinter import *

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *

images_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files')  # Image path


def show_scrollbar():
    '''show scrollbar when text is more than the text area'''

    if text_area.cget('height') < int(text_area.index('end-1c').split('.')[0]):
        scrollbar.grid(column=1, row=0, sticky=N + S)
        text_area.config(yscrollcommand=scrollbar.set)
        root.after(100, hide_scrollbar)

    else:
        root.after(100, show_scrollbar)


def hide_scrollbar():
    '''hide scrollbar when text is less than the text area'''

    if text_area.cget('height') >= int(text_area.index('end-1c').split('.')[0]):
        scrollbar.grid_forget()
        text_area.config(yscrollcommand=None)
        root.after(100, show_scrollbar)

    else:
        root.after(100, hide_scrollbar)


def check_file(*file_names):
    '''Create 'saving.txt' and 'spending.txt' if not found'''

    for file_name in file_names:
        if not os.path.exists(file_name):
            with open(file_name, 'w'):
                pass


def protocol():
    '''Minimize and Maximize main window when working with another window'''

    root.destroy()
    window.deiconify()


def display_message(message, width, height, pos_x, pos_y):
    '''Display any message like info or error'''

    result = Label(earn_frame, width=width, height=height, bg='#cfe0c7', font=('Courier', 12), text='{}'.format(message))
    result.place(x=pos_x, y=pos_y)

    root.update()
    root.after(1500, result.place_forget)


def edit_display_message(message, width, height, pos_x, pos_y):
    '''Display any message like info or error'''

    result = Label(m_frame, width=width, height=height, bg='#cfe0c7', font=('Courier', 12), text='{}'.format(message))
    result.place(x=pos_x, y=pos_y)

    root.update()
    root.after(1500, result.place_forget)


def check_duplicates(file_name, name, amount):
    '''Check duplicates in your file'''

    with open(file_name, 'r') as file:
        lines = file.readlines()

        duplicate = f'{name.ljust(50)}{amount}'
        duplicates = [line.strip() for line in lines]

        if duplicate in duplicates:
            return True

        else:
            return False


def sort_file(*file_names):
    '''Sort details of file alphabetically'''

    for file_name in file_names:
        with open(file_name, 'r+') as file:
            lines = file.readlines()
            lines.sort()
            file.seek(0)

            for line in lines:
                file.write(line)


def delete_something(file_name, source, amount):
    '''Remove certain values from the text file'''

    with open(file_name, 'r+') as ea_read:
        lines = ea_read.readlines()  # Reading whole file
        lines.remove(f'{source.ljust(50)}{amount}\n')
        ea_read.seek(0)

        for line in lines:
            ea_read.write(line)

        ea_read.truncate()


def show_details(title, text, image, file_name, yet):
    '''Displays saving or spending details'''

    global root, text_area, scrollbar

    window.iconify()

    root = Toplevel()
    root.withdraw()
    root.after(0, root.deiconify)
    root.title(title)
    root.iconbitmap(os.path.join(images_path, 'icon.ico'))
    root.geometry(f'900x500+{pos_x}+{pos_y}')
    root.resizable(0, 0)

    # Adding text area to display the content of a file
    text_area_frame = Frame(root)
    text_area = Text(text_area_frame, width=47, height=27, highlightcolor='grey', highlightthickness=2, cursor='arrow')
    text_area.grid(row=0, column=0)
    text_area_frame.place(x=450, y=50)

    # Attaching scrollbar to the text area
    scrollbar = Scrollbar(text_area_frame, orient="vertical", command=text_area.yview)
    text_area['yscrollcommand'] = scrollbar.set

    # Displaying title of the window
    title_frame = Frame(root, bg='White')
    title_label = Label(title_frame, text=text, bg='White', fg='Black', font=('Courier', 30))
    title_label.grid(row=0, column=0)
    title_frame.place(x=100, y=30)

    # Inserting image
    spent_image_frame = Frame(root, bd=0)
    spent_image = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(images_path, image)))
    spent_label_image = Label(spent_image_frame, image=spent_image, borderwidth=0)
    spent_label_image.grid(row=0, column=0)
    spent_image_frame.place(x=10, y=220)

    # Inserting name image
    name_image_frame = Frame(root, bd=0)
    name_image = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(images_path, 'name.jpg')))
    name_label_image = Label(name_image_frame, image=name_image, borderwidth=0)
    name_label_image.grid(row=0, column=0)
    name_image_frame.place(x=460, y=10)

    # Inserting rupees image
    rupee_image_frame = Frame(root, bd=0)
    rupee_image = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(images_path, 'rupees.jpg')))
    rupee_label_name = Label(rupee_image_frame, image=rupee_image, borderwidth=0)
    rupee_label_name.grid(row=0, column=0)
    rupee_image_frame.place(x=715, y=10)

    # Frame for 'Not Earned Yet' label
    label_frame = Frame(root, bg='White')
    label_frame.place(x=480, y=250)

    sums = []

    check_file('saving.txt', 'spending.txt')

    with open(file_name, 'r') as exp:
        lines = exp.readlines()

        if len(lines) == 0:  # Checking if 'spending.txt' file is empty
            label = Label(label_frame, bg='White', font=('Courier', 30), text=yet)
            label.pack(anchor='center')

        else:
            for line in lines:  # If found not empty then displaying each line
                split = line.strip('\n').split(' ')
                text_area.insert(END, f'{split[0].ljust(35)}{split[-1]}\n')
                sums.append(int(split[-1]))

            text_area.insert(END, '{}{}{}'.format('\n' * 3, 'Total: '.rjust(20), sum(sums)))

    text_area.config(state=DISABLED)
    show_scrollbar()
    root.config(bg='white')
    root.protocol("WM_DELETE_WINDOW", protocol)
    root.mainloop()


def write_details(file_name, mode, source_value, amount=None, old_value=None, new_value=None):
    '''Save values or save replaced values'''

    check_file('saving.txt', 'spending.txt')

    if mode == 'w' and file_name == 'saving.txt':  # If you want to save income values
        with open('saving.txt', 'a') as save_write:
            save_write.write('{}{}\n'.format(source_value.ljust(50), amount))

    elif mode == 'w' and file_name == 'spending.txt':  # If you want to save spending values
        with open('spending.txt', 'a') as spent_write:
            spent_write.write('{}{}\n'.format(source_value.ljust(50), amount))

    elif mode == 'a' and file_name == 'saving.txt':  # If you want to replace values in your saving list
        with open('saving.txt', 'r+') as save_rw:
            lines = save_rw.readlines()
            check = '{}{}\n'.format(source_value.ljust(50), old_value)
            save_rw.seek(0)

            if check in lines:
                lines[lines.index(check)] = '{}{}\n'.format(source_value.ljust(50), new_value)

                for line in lines:
                    save_rw.write(line)
            save_rw.truncate()

    elif mode == 'a' and file_name == 'spending.txt':  # If you want to replace values in your spending list
        with open('spending.txt', 'r+') as spent_rw:
            lines = spent_rw.readlines()
            check = '{}{}\n'.format(source_value.ljust(50), old_value)
            spent_rw.seek(0)

            if check in lines:
                lines[lines.index(check)] = '{}{}\n'.format(source_value.ljust(50), new_value)

                for line in lines:
                    spent_rw.write(line)
                spent_rw.truncate()


def add_details(event=None):
    '''Add details to the file'''

    global get_source_of_earning, get_money_earned

    values = [var_one.get(), var_two.get(), var_three.get(), var_four.get(), var_five.get()]  # Store values of checkbuttons either 0 or 1 where 0 is unchecked and 1 is checked

    get_source_of_earning = entry_box.get().title()
    get_money_earned = entry_box_two.get()

    count_values = collections.Counter(values)
    check_file('saving.txt', 'spending.txt')

    if values[-1] == 1 and count_values[0] == 4:  # When 'delete all' checkbutton is checked
        with open('saving.txt', 'w'), open('spending.txt', 'w'):
            pass

        display_message('DELETED ALL', width=15, height=4, pos_x=20, pos_y=144)

    elif len(get_source_of_earning) == 0 or len(get_money_earned) == 0:  # When 'source of money' and 'amount' fields are empty
        winsound.MessageBeep()
        display_message(message='Some fields are\nleft empty', width=17, height=4, pos_x=12, pos_y=144)

    elif not get_money_earned.isdigit():  # When 'Amount' field is not number
        winsound.MessageBeep()
        display_message(message='Money must be\nin number', width=15, height=4, pos_x=20, pos_y=144)

    elif count_values[0] == 5:  # When not any button is selected
        winsound.MessageBeep()
        display_message(message='No Buttons\nwere selected', width=17, height=4, pos_x=12, pos_y=144)

    elif count_values[1] == 1:  # When only one button is selected except 'delete all button'
        winsound.MessageBeep()
        display_message(message='Select at least\ntwo buttons', width=17, height=4, pos_x=12, pos_y=144)

    elif count_values[1] > 2:  # When more than two buttons are selected
        winsound.MessageBeep()
        display_message(message='Select only\ntwo buttons', width=17, height=4, pos_x=12, pos_y=144)

    elif values[0] == 1 and (values[2] == 0 or values[3] == 0) and values[1] == values[-1] == 0:  # When you select either (add and income) or (add and spent) checkbutton is selected
        if values[0] == values[2] == 1:  # When checkbutton selection is (add and income)
            if check_duplicates('saving.txt', get_source_of_earning, get_money_earned):  # Checking if provided value is already in a file.
                winsound.MessageBeep()
                display_message(message='Value Exists', width=16, height=4, pos_x=17, pos_y=144)  # If value already in file then showing 'Value Exists'

            else:  # If provided value not in file then adding to file
                write_details(file_name='saving.txt', mode='w', source_value=get_source_of_earning, amount=get_money_earned)
                display_message(message='Value Added', width=15, height=4, pos_x=19, pos_y=144)  # Showing 'Value Added'

        elif values[0] == values[3] == 1:  # When checkbutton selection is (add and spent)
            if check_duplicates('spending.txt', get_source_of_earning, get_money_earned):  # Checking if provided value is already in a file.
                winsound.MessageBeep()
                display_message(message='Value Exists', width=16, height=4, pos_x=17, pos_y=144)  # If value already in file then showing 'Value Exists'

            else:  # If provided value not in file then adding to file
                write_details(file_name='spending.txt', mode='w', source_value=get_source_of_earning, amount=get_money_earned)
                display_message(message='Value Added', width=15, height=4, pos_x=19, pos_y=144)  # Showing 'Value Added' after adding details to file

    elif values[1] == 1 and (values[2] == 0 or values[3] == 0) and values[0] == values[4] == 0:  # When you select either (delete and income) or (delete and spent) checkbutton is selected
        if values[1] == values[2] == 1:  # When checkbutton selection is (delete and income)
            if not check_duplicates('saving.txt', get_source_of_earning, get_money_earned):  # Checking if provided value not in file.
                winsound.MessageBeep()
                display_message(message='Value Not\nFound', width=15, height=4, pos_x=17, pos_y=144)  # Showing 'Value Not Found'

            else:  # If provided value is in file then deleting it
                delete_something('saving.txt', get_source_of_earning, get_money_earned)
                display_message(message='Value Removed', width=15, height=4, pos_x=17, pos_y=144)  # Showing 'Value Removed'

        elif values[1] == values[3] == 1:  # When checkbutton selection is (delete and spent)
            if not check_duplicates('spending.txt', get_source_of_earning, get_money_earned):  # Checking if provided value not in file.
                winsound.MessageBeep()
                display_message(message='Value Not\nFound', width=15, height=4, pos_x=17, pos_y=144)  # Showing 'Value Not Found'

            else:  # If provided value is in file then deleting it
                delete_something('spending.txt', get_source_of_earning, get_money_earned)
                display_message(message='Value Removed', width=15, height=4, pos_x=17, pos_y=144)  # Showing 'Value Not Found'

    else:
        ''' Invalid button selection happens when:
                ->>->>->>->>- Add and Delete button is selected
                ->>->>->>->>- Income and Spent button is selected
                ->>->>->>->>- Add and Delete all button is selected
                ->>->>->>->>- Delete and Delete all button is selected '''

        winsound.MessageBeep()
        display_message(message='Invalid button\nselected', width=16, height=4, pos_x=17, pos_y=144)

    sort_file('saving.txt', 'spending.txt')


def edit_get_details(event=None):
    '''save values of edit window'''

    check_file('saving.txt', 'spending.txt')

    get_source_of_earning = source_entry_box.get().title()
    get_old_amount = old_money_entry.get()
    get_new_amount = new_money_entry.get()

    if len(get_source_of_earning) == 0 or len(get_old_amount) == 0 or len(get_new_amount) == 0:   # Check if any entry text is empty
        winsound.MessageBeep()
        edit_display_message(message='Some fields\nare empty', width=20, height=4, pos_x=40, pos_y=200)

    elif not get_old_amount.isdigit() or not get_new_amount.isdigit():   # Check if amount entry value have digits
        winsound.MessageBeep()
        edit_display_message(message='Amount must be\nin number', width=20, height=4, pos_x=40, pos_y=200)

    elif var.get() != 1 and var.get() != 2:   # Check if any buttons is not selected
        winsound.MessageBeep()
        edit_display_message(message='Select button', width=20, height=4, pos_x=70, pos_y=200)

    else:   # Saving to file
        if var.get() == 1:   # Saving values to saving.txt file
            if check_duplicates('saving.txt', get_source_of_earning, get_old_amount):   # Replace old value with new value
                write_details(file_name='saving.txt', mode='a', source_value=get_source_of_earning, old_value=get_old_amount, new_value=get_new_amount)
                edit_display_message(message='Value Added', width=15, height=4, pos_x=70, pos_y=200)

            else:   # If above condition fails then value doesn't exists
                winsound.MessageBeep()
                edit_display_message(message='Value not found', width=15, height=4, pos_x=70, pos_y=200)

        elif var.get() == 2:   # Saving values to saving.txt file
            if check_duplicates('spending.txt', get_source_of_earning, get_old_amount):   # Replace old value with new value
                write_details(file_name='spending.txt', mode='a', source_value=get_source_of_earning, old_value=get_old_amount, new_value=get_new_amount)
                edit_display_message(message='Value Added', width=15, height=4, pos_x=70, pos_y=200)

            else:   # If above condition fails then value doesn't exists
                winsound.MessageBeep()
                edit_display_message(message='Value not found', width=15, height=4, pos_x=70, pos_y=200)


def back_button_command(event=None):
    '''Command for Go Back command'''

    root.destroy()
    gui_earning()


def edit_command(event=None):
    '''Command from edit window'''

    if var_six.get() == 1:
        edit_window()


def edit_window(event=None):
    '''Create window to enter source of spending'''

    global root, m_frame, var, source_entry_box, old_money_entry, new_money_entry

    root.destroy()   # Destroy previous opened window

    root = Toplevel()
    root.withdraw()
    root.after(0, root.deiconify)
    root.title('Edit')
    root.iconbitmap(os.path.join(images_path, 'icon.ico'))
    root.geometry(f'900x500+{pos_x}+{pos_y}')
    root.resizable(0, 0)

    # Adding image
    edit_frame = Frame(root, bd=0)
    edit_image = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(images_path, 'edit.png')))
    edit_label_image = Label(edit_frame, image=edit_image, borderwidth=0)
    edit_label_image.grid(row=0, column=0)
    edit_frame.place(x=80, y=120)

    # Adding first entry box
    m_frame = Frame(root, bg='white', height=250, highlightthickness=1, highlightbackground='silver')
    source_label = Label(m_frame, padx=20, pady=20, bg='White', font=('Courier', 13), text='Source of Money')
    source_entry_box = Entry(m_frame, width=50, bg='White', highlightthickness=2, highlightbackground='silver')
    source_label.grid(row=0, column=0)
    source_entry_box.grid(row=0, column=1)
    m_frame.place(x=350, y=100)
    source_entry_box.bind('<Return>', edit_get_details)

    # Adding second entry box
    old_money_label = Label(m_frame, padx=20, pady=20, bg='White', text='Old Amount', font=('Courier', 13))
    old_money_entry = Entry(m_frame, bg='White', width=50, highlightthickness=2, highlightbackground='silver')
    old_money_label.grid(row=1, column=0)
    old_money_entry.grid(row=1, column=1, padx=10)
    old_money_entry.bind('<Return>', edit_get_details)

    # Adding second entry box
    new_money_label = Label(m_frame, padx=20, pady=20, bg='White', text='New Amount', font=('Courier', 13))
    new_money_entry = Entry(m_frame, bg='White', width=50, highlightthickness=2, highlightbackground='silver')
    new_money_label.grid(row=2, column=0)
    new_money_entry.grid(row=2, column=1, padx=10)
    new_money_entry.bind('<Return>', edit_get_details)

    # Radio-buttons
    var = IntVar()
    radio_button_frame = Frame(root, bg='white')
    save_radio_buttons = Radiobutton(radio_button_frame, text='Saving', value=1, variable=var, bg='white')
    spend_radio_buttons = Radiobutton(radio_button_frame, text='Spending', value=2, variable=var, bg='white')
    save_radio_buttons.grid(row=0, column=0)
    spend_radio_buttons.grid(row=0, column=1)
    radio_button_frame.place(x=712, y=276)

    # Adding submit button
    append_button = Button(m_frame, height=3, width=16, bg='#36e800', activebackground='#36e800', text='APPEND', font=('Courier', 13), command=edit_get_details)
    append_button.grid(row=3, column=1, pady=11, padx=5, sticky='e')
    append_button.bind('<Return>', edit_get_details)

    # back button
    back_frame = Frame(root, bg='white')
    back_button = Button(back_frame, text='Go Back', bd=0, bg='white', fg='red', cursor='hand2', command=back_button_command)
    back_button.grid(row=0, column=0)
    back_frame.place(x=350, y=415)

    # Bind Keys
    source_entry_box.bind('<Return>', edit_get_details)
    old_money_entry.bind('<Return>', edit_get_details)
    new_money_entry.bind('<Return>', edit_get_details)
    append_button.bind('<Return>', edit_get_details)
    back_button.bind('<Enter>', (lambda e: back_button.config(fg='green')))
    back_button.bind('<Leave>', (lambda e: back_button.config(fg='red')))

    root.config(bg='White')
    root.protocol("WM_DELETE_WINDOW", protocol)
    root.mainloop()


def gui_earning(event=None):
    '''Create window to enter source of spending'''

    global root, entry_box, entry_box_two, earn_frame
    global var_one, var_two, var_three, var_four, var_five, var_six

    window.iconify()

    root = Toplevel()
    root.withdraw()
    root.after(0, root.deiconify)
    root.title('Add Earning | Expenditure')
    root.iconbitmap(os.path.join(images_path, 'icon.ico'))
    root.geometry(f'900x500+{pos_x}+{pos_y}')
    root.resizable(0, 0)

    # Displaying title of the window
    title_frame = Frame(root, bg='White')
    title_label = Label(title_frame, bg='White', fg='Black', text='ADD\nSAVING\nOR\nSPENDING'.rjust(8), font=('Courier', 30))
    title_label.grid(row=1, column=0)
    title_frame.place(x=50, y=10)

    # Adding image
    spent_image_frame = Frame(root, bd=0)
    spent_image = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(images_path, 'earning.jpg')))
    spent_label_image = Label(spent_image_frame, image=spent_image, borderwidth=0)
    spent_label_image.grid(row=0, column=0)
    spent_image_frame.place(x=70, y=200)

    # Adding first entry box
    earn_frame = Frame(root, bg='white', height=250, highlightthickness=1, highlightbackground='silver')
    earn_label = Label(earn_frame, padx=20, pady=20, bg='White', font=('Courier', 13), text='Source of Money')
    entry_box = Entry(earn_frame, width=50, bg='White', highlightthickness=2, highlightbackground='silver')
    earn_label.grid(row=0, column=0)
    entry_box.grid(row=0, column=1)
    earn_frame.place(x=350, y=150)
    entry_box.bind('<Return>', add_details)

    # Adding second entry box
    entry_label = Label(earn_frame, padx=20, pady=20, bg='White', text='Amount', font=('Courier', 13))
    entry_box_two = Entry(earn_frame, bg='White', width=50, highlightthickness=2, highlightbackground='silver')
    entry_label.grid(row=1, column=0)
    entry_box_two.grid(row=1, column=1, padx=10)
    entry_box_two.bind('<Return>', add_details)

    var_one, var_two, var_three, var_four, var_five, var_six = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()

    # Adding first row checkbox
    check_button_frame = Frame(root)
    add_check_button = Checkbutton(check_button_frame, bd=0, text='ADD', anchor='e', bg='White', variable=var_one, onvalue=1)
    del_check_button = Checkbutton(check_button_frame, bd=0, bg='White', anchor='w', variable=var_two, text='DELETE', onvalue=1, offvalue=0, padx=20)
    add_check_button.grid(row=2, column=0, padx=0, sticky='ewns')
    del_check_button.grid(row=2, column=1, padx=0, sticky='ewns')
    check_button_frame.place(x=548, y=290)

    # Adding second row checkbox
    check_button_frame_two = Frame(root)
    earn_check_button = Checkbutton(check_button_frame_two, bd=0, text='INCOME', anchor='e', bg='White', variable=var_three, onvalue=1)
    expenditure_check_button = Checkbutton(check_button_frame_two, bd=0, text='SPENT', anchor='w', bg='White', variable=var_four, onvalue=1)
    earn_check_button.grid(row=0, column=0)
    expenditure_check_button.grid(row=0, column=1)
    check_button_frame_two.place(x=548, y=312)

    # Adding third row checkbox
    delete_check_button_frame = Frame(root)
    delete_all_button = Checkbutton(delete_check_button_frame, text='DELETE ALL', bg='White', variable=var_five, onvalue=1)
    delete_all_button.grid(row=0, column=0)
    delete_check_button_frame.place(x=548, y=334)

    # edit checkbox
    edit_frame = Frame(root)
    edit_check_box = Checkbutton(edit_frame, text='EDIT', bg='White', variable=var_six, command=edit_command)
    edit_check_box.grid(row=0, column=0)
    edit_frame.place(x=548, y=357)

    # Adding submit button
    submit_button = Button(earn_frame, height=4, width=16, bg='#36e800', activebackground='#36e800', text='SUBMIT', font=('Courier', 13), command=add_details)
    submit_button.grid(row=3, column=1, pady=11, padx=5, sticky='e')
    submit_button.bind('<Return>', add_details)

    root.config(bg='White')
    root.protocol("WM_DELETE_WINDOW", protocol)
    root.mainloop()


def main():
    global window, pos_x, pos_y

    window = Tk()
    window.withdraw()
    window.after(0, window.deiconify)
    window.title('Saving & Spending')
    window.iconbitmap(os.path.join(images_path, 'icon.ico'))
    window.resizable(0, 0)

    pos_x, pos_y = window.winfo_screenwidth() // 2 - 900 // 2, window.winfo_screenheight() - 650
    window.geometry(f'900x500+{pos_x}+{pos_y}')

    # Setting and Inserting title
    title_frame = Frame(window, bg='White')
    title_label_one = Label(title_frame, bg='White', fg='Black', text='SAVING\n&\nSPENDING', font=('Courier', 30))
    title_label_one.grid(row=0, column=0)
    title_frame.place(x=100, y=30)

    # Adding first title image
    label_image_frame = Frame(window, bd=0, width=237, height=280)
    file_image_file = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(images_path, 'istock.jpg')))
    label_image = Label(label_image_frame, image=file_image_file, bg='blue', borderwidth=0)
    label_image.grid(row=0, column=0)
    label_image_frame.place(x=3, y=200)

    # Adding earned button
    earned_button_frame = Frame(window)
    earned_button = Button(earned_button_frame, bd=3, bg='Red', activebackground='Red', height=3, width=60, fg='White', borderwidth=2, relief='raise', text='MY EARNING', command=lambda: (show_details('Earned details', 'MY\nEARNING', 'save.jpg', 'saving.txt', 'Not Earned Yet')))
    earned_button.grid(row=0, column=0)
    earned_button_frame.place(x=425, y=200)
    earned_button.bind('<Return>', (lambda e: (show_details('Earned details', 'MY\nEARNING', 'save.jpg', 'saving.txt', 'Not Earned Yet'))))

    # Adding spent button
    spent_button_frame = Frame(window)
    spent_button = Button(spent_button_frame, bd=3, height=3, width=60, fg='White', bg='#01912f', activebackground='#01912f', borderwidth=2, relief='raise', text='MY SPENDING', command=lambda: (show_details('Spent details', 'MY\nSPENDING', 'spent.jpg', 'spending.txt', 'Not Spent Yet')))
    spent_button.grid(row=0, column=0)
    spent_button_frame.place(x=425, y=260)
    spent_button.bind('<Return>', (lambda e: (show_details('Spent details', 'MY\nsSPENDING', 'spent.jpg', 'spending.txt', 'Not Spent Yet'))))

    # Add source of saving and spent
    add_button_frame = Frame(window)
    add_button = Button(add_button_frame, bd=3, height=3, width=60, fg='White', bg='Purple', activebackground='Purple', borderwidth=2, relief='raise', text='ADD SOURCE OF EARNING | EXPENDITURE', command=gui_earning)
    add_button.grid(row=0, column=0)
    add_button_frame.place(x=425, y=320)
    add_button.bind('<Return>', gui_earning)

    window.config(bg='White')
    window.mainloop()


if __name__ == '__main__':
    main()
