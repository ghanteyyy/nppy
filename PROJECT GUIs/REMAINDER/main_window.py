try:  # Python 3
    from tkinter import *
    from tkinter.ttk import Combobox

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *
    from ttk import Combobox


def enter():
    '''This function tiggers when the mouse cursor within the boundry of Remind Me about! field'''

    if event_entry.get() == 'Remind Me About ...':
        event_entry.delete(0, END)
        event_entry.insert(END, '')
        event_entry.config(fg='black')
        event_entry.focus()


def leave():
    '''This function tiggers when the mouse cursor out of the boundry of Remind Me about! field'''

    if len(event_entry.get().strip()) == 0:
        event_entry.delete(0, END)
        event_entry.insert(END, 'Remind Me About ...')
        event_entry.config(fg='grey')
        root.focus()


def show_info(text):
    '''SHowing errors and info to the user'''

    info.config(text=text)
    info.pack(side='bottom')
    root.after(1250, info.pack_forget)


def add_command():
    '''When user press the add remainder button'''

    is_valid = True

    values = [event_entry.get().strip('\t'), combo_box_month.get(), combo_box_date.get(), combo_box_hour.get(), combo_box_minute.get(), combo_box_am_pm.get()]

    for value in values:
        if value in ['Remind Me about ...', 'Month', 'Day', 'Hour', 'Min', 'AM / PM']:
            is_valid = False
            show_info('Some field(s) are left empty or not valid')
            break

    if is_valid is True:
        if values[-1] == "PM":   # Converting to 24 hour system if last value of values is "PM"
            values[values.index(values[3])] = str(int(values[3]) + 12)

        with open('remind_me.txt', 'a') as w_rm:
            w_rm.write('{} || {}\n'.format(values[0], ' '.join(values[1:])))   # Writing to file if everything goes well

        show_info('Added')

        combo_box_month.delete(0, END)
        combo_box_month.insert(0, 'Remind Me About')

        combo_box_date.set('')
        combo_box_date.set('Month')

        combo_box_hour.set('')
        combo_box_hour.set('Hour')

        combo_box_minute.set('')
        combo_box_minute.set('Min')

        combo_box_am_pm.set('')
        combo_box_am_pm.set('AM / PM')


root = Tk()
root.title('REMIND ME !')
root.resizable(0, 0)
root.config(bg='grey')
root.geometry('446x230+{}+{}'.format(root.winfo_screenwidth() // 2 - 446 // 2, root.winfo_screenheight() // 2 - 230 // 2))

title_label = Label(root, text='REMIND ME!', bg='grey', font=('ISOCP', 40, 'bold'))
title_label.pack()

event_entry = Entry(root, fg='grey', width=25, font=('ISOCP', 12, 'bold'))
event_entry.insert(END, 'Remind Me About ...')
event_entry.pack(pady=10)

combo_box_frame = Frame(root)

month_number = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
combo_box_month = Combobox(combo_box_frame, value=[k for k in month_number], width=8)
combo_box_month.set('Month')
combo_box_month.pack(side=LEFT)

combo_box_date = Combobox(combo_box_frame, value=[str(k).zfill(2) for k in range(1, 33)], width=5)
combo_box_date.set('Date')
combo_box_date.pack(side=LEFT)

combo_box_hour = Combobox(combo_box_frame, value=[str(i).zfill(2) for i in range(1, 13)], width=5)
combo_box_hour.set('Hour')
combo_box_hour.pack(side=LEFT)

combo_box_minute = Combobox(combo_box_frame, value=[str(i).zfill(2) for i in range(0, 60)], width=5)
combo_box_minute.set('Min')
combo_box_minute.pack(side=LEFT)

combo_box_am_pm = Combobox(combo_box_frame, value=['AM', 'PM'], width=8)
combo_box_am_pm.set('AM / PM')
combo_box_am_pm.pack(side=LEFT)

combo_box_frame.pack(pady=10)

info = Label(root, fg='white', bg='black', font=('ISOCP', 15, 'bold'))

add_button = Button(root, text='ADD REMAINDER', width=35, fg='black', bg='grey', font=('ISOCP', 12, 'bold'), activebackground='grey', activeforeground='black', border=0, command=add_command)
add_button.pack(pady=10, side='bottom')

event_entry.bind('<Enter>', lambda e: (enter()))
event_entry.bind('<Leave>', lambda e: (leave()))

root.mainloop()
