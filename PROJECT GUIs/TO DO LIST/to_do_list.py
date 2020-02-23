import os
import ctypes
from tkinter import *


def hide_minimize_maximize(window):
    # Shortcuts WinAPI functionality
    set_window_pos = ctypes.windll.user32.SetWindowPos
    set_window_long = ctypes.windll.user32.SetWindowLongW
    get_window_long = ctypes.windll.user32.GetWindowLongW
    get_parent = ctypes.windll.user32.GetParent

    # Some WinAPI flags
    GWL_STYLE = -16
    WS_MINIMIZEBOX = 131072
    WS_MAXIMIZEBOX = 65536
    SWP_NOZORDER = 4
    SWP_NOMOVE = 2
    SWP_NOSIZE = 1
    SWP_FRAMECHANGED = 32

    hwnd = get_parent(window.winfo_id())
    old_style = get_window_long(hwnd, GWL_STYLE)  # getting the old style
    new_style = old_style & ~ WS_MAXIMIZEBOX & ~ WS_MINIMIZEBOX  # building the new style (old style AND NOT Maximize AND NOT Minimize)
    set_window_long(hwnd, GWL_STYLE, new_style)  # setting new style
    set_window_pos(hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)  # updating non-client area


def enter(event=None):
    '''When cursor enters the entry box'''

    if entry_box.get() == 'I have to do ...':
        entry_box.delete(0, END)
        entry_box.focus()
        entry_box.config(fg='black')


def leave(event=None):
    '''When cursor leaves the entry box'''

    if len(entry_box.get()) == 0:
        entry_box.insert(END, 'I have to do ...')
        entry_box.config(fg='grey')

    root.focus()


def collapse():
    '''Expand and shrink window'''

    if _var_.get() == 0:
        _var_.set(1)
        root.geometry('{}x{}+{}+{}'.format(0, root.winfo_screenheight() - 74, root.winfo_screenwidth() - 33, 0))
        collapse_button.config(text='<<', bg='#4b4d51', activeforeground='black')
        load_prev_button.config(bg='#4b4d51')
        exit_frame.place(x=2, y=root.winfo_screenheight() - 110)

    else:
        _var_.set(0)
        root.geometry('{}x{}+{}+{}'.format(400, root.winfo_screenheight() - 74, root.winfo_screenwidth() - 401, 0))
        collapse_button.config(text='>>', bg='#4b4d51', activeforeground='black')
        load_prev_button.config(bg='#666666')
        exit_frame.place_forget()


def insert_data(event=None):
    '''Insert data to the list box'''

    get_entry_box = entry_box.get().title()
    get_list_box = list_box.get(0, END)

    if len(get_entry_box) != 0 and (get_entry_box not in get_list_box):
        list_box.insert(len(get_list_box), get_entry_box)

    entry_box.delete(0, END)
    entry_box.insert(END, 'I have to do ...')
    entry_box.config(fg='grey')

    root.focus()
    save_to_file()


def delet_one_value(event=None):
    '''Delete selected values'''

    get_selected_values = [cs for cs in list_box.curselection()][::-1]

    for i in get_selected_values:
        list_box.delete(i)

    del_write()
    show_scrollbar()


def delete_all(event=None):
    '''Delete all values'''

    list_box.delete(0, END)

    del_prev_data()
    show_scrollbar()


def popup_menu(event=None):
    '''Display menu when right click is clicked'''

    try:
        delete_menu.tk_popup(event.x_root, event.y_root, 0)

    finally:
        delete_menu.grab_release()


def show_scrollbar():
    '''show scrollbar when text is more than the text area'''

    if len(list_box.get(0, END)) > 22:
        scrollbar.grid(column=1, row=0, sticky=N + S)
        list_box.config(yscrollcommand=scrollbar.set)
        root.after(100, hide_scrollbar)

    else:
        root.after(100, show_scrollbar)


def hide_scrollbar():
    '''hide scrollbar when text is less than the text area'''

    if len(list_box.get(0, END)) <= 22:
        scrollbar.grid_forget()
        list_box.config(yscrollcommand=None)
        root.after(100, show_scrollbar)

    else:
        root.after(100, hide_scrollbar)


def save_to_file():
    '''Save items of list box in a file'''

    get_value = [line.strip('\n') for line in list_box.get(0, END)]

    with open('load_prev.txt', 'r') as rlp, open('load_prev.txt', 'a') as alp:
        lines = [line.strip('\n') for line in rlp.readlines()]

        for value in get_value:
            if value not in lines:
                alp.write(f'{value}\n')


def load_prev_data():
    '''Retrive previous data'''

    try:
        save_to_file()

        with open('load_prev.txt', 'r') as rsv:
            lines = rsv.readlines()

            list_box.delete(0, END)

            for index, line in enumerate(lines):
                list_box.insert(index, line.strip('\n'))

    except FileNotFoundError:
        pass


def del_prev_data():
    '''Delete all previous values'''

    with open('load_prev.txt', 'w'):
        pass


def del_write():
    get_values = list_box.get(0, END)

    with open('load_prev.txt', 'w') as alp:
        for value in get_values:
            alp.write(f'{value}\n')


def main_window():
    global root, collapse_button, entry_box, _var_, list_box, scrollbar, delete_menu, load_prev_button, exit_frame

    root = Tk()
    root.withdraw()
    root.after(0, root.deiconify)
    root.resizable(0, 0)
    root.title('TO-DO LIST')
    root.geometry('{}x{}+{}+{}'.format(400, root.winfo_screenheight() - 74, root.winfo_screenwidth() - 401, 0))
    root.iconbitmap('included files/icon.ico')
    root.wm_attributes("-topmost", 'true')

    _var_ = IntVar()
    collapse_frame = Frame(root)
    collapse_button = Button(collapse_frame, text='>>', bg='#4b4d51', activebackground='#4b4d51', activeforeground='black', fg='white', height=47, command=collapse, relief=GROOVE)
    collapse_button.grid(row=0, column=0)
    collapse_frame.place(x=0, y=0)

    label_frame = Frame(root)
    label = Label(label_frame, text='MY TO-DO LIST', bg='#4b4d51', fg='white', font=('Courier', 28))
    label.grid(row=0, column=0)
    label_frame.place(x=210, y=20, anchor="center")

    entry_frame = Frame(root, bg='#4b4d51')
    entry_box = Entry(entry_frame, font=("Arial", 15), fg='grey')
    entry_box.insert(END, 'I have to do ...')
    add_button = Button(entry_frame, text='ADD', width=10, height=2, bg='Green', fg='white', activebackground='Green', activeforeground='black', command=insert_data)
    entry_box.grid(row=0, column=0)
    add_button.grid(row=0, column=1, padx=20)
    entry_frame.place(x=40, y=50)

    list_box_frame = Frame(root, relief="sunken")
    list_box = Listbox(list_box_frame, bg='#4b4d51', fg='white', width=29, height=22, font=('Courier', 15), selectmode=MULTIPLE)
    list_box.grid(row=0, column=0)
    list_box_frame.place(x=28, y=103)

    scrollbar = Scrollbar(list_box_frame, orient="vertical", command=list_box.yview)

    delete_menu = Menu(root, tearoff=0)
    delete_menu.add_command(label="Delete", command=delet_one_value)
    delete_menu.add_command(label="Delete All", command=delete_all)

    load_prev_frame = Frame()
    load_prev_button = Button(load_prev_frame, text='LOAD PREVIOUS DATA', width=30, height=2, fg='white', bg='#666666', activebackground='#666666', activeforeground='white', bd=0, command=load_prev_data)
    load_prev_button.grid(row=0, column=0)
    load_prev_frame.place(x=150, y=root.winfo_screenheight() - 153)

    del_prev_frame = Frame()
    del_prev_button = Button(del_prev_frame, text='DELETE PREVIOUS DATA', width=30, height=2, fg='white', bg='#666666', activebackground='#666666', activeforeground='white', bd=0, command=del_prev_data)
    del_prev_button.grid(row=0, column=0)
    del_prev_frame.place(x=150, y=root.winfo_screenheight() - 114)

    clear_frame = Frame()
    clear_button = Button(clear_frame, text='CLEAR', width=15, height=4, fg='white', bg='#666666', activebackground='#666666', activeforeground='white', bd=0, command=lambda: list_box.delete(0, END))
    clear_button.grid(row=0, column=0)
    clear_frame.place(x=33, y=root.winfo_screenheight() - 148)

    exit_frame = Frame(root)
    exit_button = Button(exit_frame, text='X', font=('Arial Black', 11, 'bold'), fg='white', bg='#4b4d51', activebackground='#4b4d51', activeforeground='white', bd=0, command=root.destroy)
    exit_button.grid(row=0, column=0)

    entry_box.bind('<Enter>', enter)
    entry_box.bind('<Leave>', leave)
    entry_box.bind('<Return>', insert_data)
    list_box.bind("<Button-3>", popup_menu)

    show_scrollbar()
    hide_minimize_maximize(root)

    root.config(bg='#4b4d51')
    root.mainloop()


if __name__ == '__main__':
    if not os.path.exists('load_prev.txt'):
        with open('load_prev.txt', 'w'):
            pass

    main_window()
