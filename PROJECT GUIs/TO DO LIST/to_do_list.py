import os
import ctypes
import winsound
from tkinter import *


class To_Do_List:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()   # Minimizing window
        self.master.resizable(0, 0)   # Making window unresizable
        self.master.title('TO-DO LIST')   # Giving name of window
        self.file_name = 'to_do_list.txt'   # File to store data
        self.master.after(0, self.master.deiconify)   # Restoring window to the normal state after 0 second
        self.master.wm_attributes("-topmost", 'true')   # Placing the window to top of any other window
        self.master.iconbitmap('included files/icon.ico')   # Setting the icon of the window
        self.master.geometry('{}x{}+{}+{}'.format(400, self.master.winfo_screenheight() - 74, self.master.winfo_screenwidth() - 401, 0))   # Width, height and the x,y cordinates

        self.is_collapsed = False   # Boolean value to check if the window is collapsed or not
        self.collapse_frame = Frame(self.master)   # Frame to place collapse_button
        self.collapse_button = Button(self.collapse_frame, text='>>', bg='#002157', activebackground='#002157', activeforeground='white', fg='white', height=47, relief=GROOVE, command=self.collapse)   # Collapsed button widget with respective to its attributes
        self.collapse_button.grid(row=0, column=0)  # Placing button to the collpased_frame
        self.collapse_frame.place(x=0, y=0)   # Placing collapse_frame to the window

        self.label_frame = Frame(self.master)   # Frame to place 'MY TO-DO LIST' label
        self.label = Label(self.label_frame, text='MY TO-DO LIST', bg='#002157', fg='white', font=('Courier', 28))  # Label widget with respective to its attributes
        self.label.grid(row=0, column=0)   # Placing label to the label_frame
        self.label_frame.place(x=210, y=25, anchor="center")   # Placing label_frame to the window

        self.entry_frame = Frame(self.master, bg='#002157')   # Frame to place entry widget
        self.entry_box = Entry(self.entry_frame, font=("Arial", 15), fg='grey')   # Entry widget with respective to its attributes
        self.entry_box.insert(END, 'I have to do ...')   # Inserting default text to make user ensure what to insert in the entry widget
        self.add_button = Button(self.entry_frame, text='ADD', width=10, height=2, bg='Green', fg='white', activebackground='Green', activeforeground='white', command=self.add_command)   # Add button with respective to its attributes
        self.entry_box.grid(row=0, column=0)  # Placing entry widget to the entry_frame
        self.add_button.grid(row=0, column=1, padx=20)  # Placing button widget to the entry_frame
        self.entry_frame.place(x=40, y=50)   # Placing entry_frame to window

        self.list_box_frame = Frame(self.master, relief="sunken")  # Frame to place list_box_widget
        self.list_box = Listbox(self.list_box_frame, bg='#002157', fg='white', width=27, height=22, font=('Courier', 15), selectmode=MULTIPLE)  # Listbox widget with respctive to its attributes
        self.list_box.grid(row=0, column=0)   # Placing Listbox widget to the label_box_frame
        self.list_box_frame.place(x=40, y=103)   # Placing label_box_frame to the window

        self.scrollbar = Scrollbar(self.list_box_frame, orient="vertical", command=self.list_box.yview)   # Placing scrollbar widget in listbox widget

        self.delete_menu = Menu(self.master, tearoff=0)   # Popup menu
        self.delete_menu.add_command(label="Delete from list", command=self.popup_delete)   # Adding option to popup menu
        self.delete_menu.add_command(label="Delete from list and file", command=lambda: self.popup_delete(mode='from both file and list'))  # Adding option to popup menu

        self.load_prev_frame = Frame(self.master)   # Frame to place load_prev_button
        self.load_prev_button = Button(self.load_prev_frame, text='LOAD PREVIOUS DATA', width=30, height=2, fg='white', bg='#002157', activebackground='#002157', activeforeground='white', bd=1, relief=GROOVE, command=self.add_to_list)   # LOAD PREVIOUS DATA button with respective to its attributes
        self.load_prev_button.grid(row=0, column=0)   # Placing load_prev_button to the load_prev_button frame
        self.load_prev_frame.place(x=150, y=self.master.winfo_screenheight() - 153)   # Placing load_prev_frame to the window

        self.del_prev_frame = Frame(self.master)   # Frame to place del_prev_button
        self.del_prev_button = Button(self.del_prev_frame, text='DELETE ALL PREVIOUS DATA', width=30, height=2, fg='white', bg='#002157', activebackground='#002157', activeforeground='white', bd=1, relief=GROOVE, command=lambda: self.check_for_file(clear_all=True))  # DELETE PREVIOUS DATA button with respective to its attributes
        self.del_prev_button.grid(row=0, column=0)   # Placing del_prev_button to the del_prev_frame
        self.del_prev_frame.place(x=150, y=self.master.winfo_screenheight() - 114)   # Placing del_prev_frame to the window

        self.clear_frame = Frame(self.master)   # Frame to palce clear_button
        self.clear_button = Button(self.clear_frame, text='CLEAR', width=13, height=4, fg='white', bg='#002157', activebackground='#002157', activeforeground='white', bd=1, relief=GROOVE, command=self.clear)   # Clear button with respective to its attributes
        self.clear_button.grid(row=0, column=0, ipadx=4, ipady=4)   # Placing clear_button to the clear_frame
        self.clear_frame.place(x=40, y=self.master.winfo_screenheight() - 152)   # Placing clear_frame to the window

        self.exit_frame = Frame(self.master)   # Frame to place exit button
        self.exit_button = Button(self.exit_frame, text='X', font=('Arial Black', 9, 'bold'), fg='white', bg='red', activebackground='red', activeforeground='white', bd=0, command=self.master.destroy)  # "X" button with respective to its attribute
        self.exit_button.grid(row=0, column=0, ipadx=2, ipady=1)   # Placing exit_button to the exit_frame

        self.entry_box.bind('<Enter>', self.enter)    # Binding entry widget when the cursor enters the entry widget
        self.entry_box.bind('<Leave>', self.leave)    # Binding entry widget when the cursor leaves the entry widget
        self.entry_box.bind('<Return>', self.add_command)  # Binding enter key with enter function
        self.list_box.bind("<Button-3>", self.popup_menu)  # Showing popup menu option when right button is clicked
        self.clear_button.bind('<Enter>', lambda e: self.clear_button.config(cursor='hand2'))    # Binding clear button when the cursor enters the clear button
        self.del_prev_button.bind('<Enter>', lambda e: self.del_prev_button.config(cursor='hand2'))    # Binding del_prev_button button when the cursor enters the del_prev_button button
        self.load_prev_button.bind('<Enter>', lambda e: self.load_prev_button.config(cursor='hand2'))    # Binding load_prev_button button when the cursor enters the load_prev_button button

        self.add_to_list()  # Adding the content from "to_do_list.txt" if the file is not empty
        self.show_scrollbar()  # Showing scrollbar at the right side of list_box
        self.hide_minimize_maximize(self.master)  # Hiding maximize and minimize button

        self.master.config(bg='#002157')   # Setting background color of whole window to hex value

    def hide_minimize_maximize(self, window):
        '''Hide minimize and maximize button'''

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

    def collapse(self):
        '''Expand and shrink window'''

        if not self.is_collapsed:   # Checking if the window is not collapsed
            self.is_collapsed = True   # Changing the boolean value for self.is_collapsed
            self.master.geometry('{}x{}+{}+{}'.format(0, self.master.winfo_screenheight() - 74, self.master.winfo_screenwidth() - 33, 0))   # Decreasing the width of the window
            self.collapse_button.config(text='<<')   # Changing the text of collapse_button
            self.exit_frame.place(x=3, y=self.master.winfo_screenheight() - 102)   # Placing the frame to the respective coordinates

        else:    # Checking if the window is collapsed already
            self.is_collapsed = False   # Changing the boolean value for self.is_collapsed
            self.master.geometry('{}x{}+{}+{}'.format(400, self.master.winfo_screenheight() - 74, self.master.winfo_screenwidth() - 401, 0))   # Increasing the width of the window
            self.collapse_button.config(text='>>')   # Changing the text of button
            self.exit_frame.place_forget()   # Removing "exit_frame"

    def enter(self, event=None):
        '''When cursor enters the entry box'''

        if self.entry_box.get() == 'I have to do ...':    # Checking if user have the default text
            self.entry_box.delete(0, END)    # Emptying "entry_box"
            self.entry_box.focus()   # Setting focus to "entry_box"
            self.entry_box.config(fg='black')   # Setting text color to black

    def leave(self, event=None):
        '''When cursor leaves the entry box'''

        if len(self.entry_box.get().strip()) == 0:   # Checking if user didn't provide any value in "entry_box"
            self.entry_box.delete(0, END)    # Emptying "entry_box"
            self.entry_box.insert(END, 'I have to do ...')    # Inserting value in "entry_box"
            self.entry_box.config(fg='grey')   # Setting text color to grey

        self.master.focus()

    def show_scrollbar(self):
        '''show scrollbar when text is more than the text area'''

        if len(self.list_box.get(0, END)) > 22:    # Checking if the length of value in list_box is more than 22
            self.scrollbar.grid(column=1, row=0, sticky=N + S)   # Putting scrollbar next to "list_box"
            self.list_box.config(yscrollcommand=self.scrollbar.set)   # Setting command for scrollbar
            self.master.after(100, self.hide_scrollbar)    # Calling "hide_scrollbar" function every 100 ms

        else:
            self.master.after(100, self.show_scrollbar)   # Calling "show_scrollbar" function every 100 ms

    def hide_scrollbar(self):
        '''hide scrollbar when text is less than the text area'''

        if len(self.list_box.get(0, END)) <= 22:   # Checking if the length of value in list_box is less than or equal to 22
            self.scrollbar.grid_forget()   # Removing scrollbar
            self.list_box.config(yscrollcommand=None)   # Removing scrollbar command
            self.master.after(100, self.show_scrollbar)   # Calling "show_scrollbar" function every 100 ms

        else:
            self.master.after(100, self.hide_scrollbar)      # Calling "hide_scrollbar" function every 100 ms

    def popup_menu(self, event=None):
        '''Display menu when right click is clicked'''

        try:
            self.delete_menu.tk_popup(event.x_root, event.y_root, 0)   # Displaying menu with the coordinate of the cursor

        finally:
            self.delete_menu.grab_release()   # Removing the menu list

    def check_for_file(self, clear_all=False):
        '''Create "to_do_list.txt" file if not exists or delete the contents of file if user press delete previous data'''

        if not os.path.exists(self.file_name) or clear_all:     # Checking if "to_do_list.txt" exists or "clear_all" parameter is set to True
            with open(self.file_name, 'w'):    # Opening file with reading mode. (Here, Opening means creating file)
                pass

            self.clear()    # Clearing the list_box

    def save_content(self, contents):
        '''Save user list to the file'''

        with open(self.file_name, 'a') as file:  # Opening "to_do_list.txt" file in appending mode
            for content in contents:   # Lopping through each value of "contents" parameter
                file.write(f'{content}\n')  # Appending each value from "contents" parameter

    def read_content(self):
        '''Read contents of the file'''

        with open(self.file_name, 'r') as file:   # Opening "to_do_list.txt" file in reading mode
            contents = [content.strip('\n') for content in file.readlines()]    # Removing new_line('\n') from each line of the file

        return contents   # Returing the list of values of file after removing new_line('\n')

    def add_to_list(self, data=None):
        '''Get the contents from the file and add them to the list box'''

        if os.path.exists(self.file_name):     # Checking if 'to_do_list.txt' file exists
            if data:   # Checking if "data" parameter is not None
                contents = data    # Getting content from the data

            else:   # Here, "data" parameter is None
                contents = self.read_content()    # Getting content from the file

            self.clear()   # Clearing items in "self.list_box"

            for index, content in enumerate(contents):   # Looping through elements containing in contents
                self.list_box.insert(index, content.strip('\n'))   # Inserting elements in the "self.list_box" with respective index

    def add_command(self, event=None):
        '''Command for add button'''

        get_from_entry_box = self.entry_box.get().strip()   # Getting values from the entry box

        if get_from_entry_box and get_from_entry_box != 'I have to do ...':   # Checking if the entry box is not empty and the entry box doesnot contain the default value i.e "I have to do ..."
            self.check_for_file()   # Checking if "to_do_file_.txt" exists before saving the contents into the file
            self.save_content([get_from_entry_box])   # Saving value from the entry box in the file
            self.add_to_list()   # Adding the got values from the entry box to the list box

            self.entry_box.delete(0, END)   # Removing the user entered value from the entry_box in order to set the default values
            self.leave()   # Adding the default values to the entry_box

        else:
            winsound.MessageBeep()

    def clear(self):
        '''Command for clear button'''

        self.list_box.delete(0, END)    # Emptying the list_box

    def popup_delete(self, mode=None):
        '''Command when user right clicks'''

        selection = self.list_box.curselection()   # Getting indexes of selected items in list_box
        from_list = [value for index, value in enumerate(self.list_box.get(0, END)) if index not in selection]   # Filtering values except selected values in list_box

        if mode == 'from both file and list':    # Checking if user has selected "Delete from list_box and file" options
            self.check_for_file(clear_all=True)   # Emptying file

            if from_list:  # Checking if "from_list" is not empty
                self.save_content(from_list)   # Saving non selected values from the list_box
                self.add_to_list(from_list)    # Removing the selected values from the list_box and only inserting the non-selected values

        else:   # Checking if user has selected "Delete from list"
            self.clear()    # Clearing items in "self.list_box"

            if from_list:  # Checking if "from_list" is not empty
                self.add_to_list(from_list)   # Removing the selected values from the list_box and only inserting the non-selected values


if __name__ == '__main__':
    root = Tk()
    To_Do_List(root)
    root.mainloop()
