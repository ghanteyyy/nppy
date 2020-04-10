from __future__ import division  # If python is 2.x

import os
import sys
import winsound

try:  # Python 3
    import ctypes
    from tkinter import *
    from tkinter import PhotoImage
    from tkinter import messagebox

    PY3 = True

except (ImportError, ModuleNotFoundError):  # Python 2
    import PIL.Image   # PIL does not come pre-install in python 2 so you need to install it using "pip install Pillow"
    import PIL.ImageTk
    from Tkinter import *
    import tkMessagebox as messagebox

    PY3 = False


hide_minimiz_maximize = False


class hide_or_show_maximize_minimize:
    '''Hide the minimize and maximize buton when the window is place at the top of other applications windows.
       And show the minimize and maximize button when the window is not place at the top of other applications windows'''

    def __init__(self, window):
        self.window = window

        #   shortcuts to the WinAPI functionality
        self.set_window_pos = ctypes.windll.user32.SetWindowPos
        self.set_window_long = ctypes.windll.user32.SetWindowLongW
        self.get_window_long = ctypes.windll.user32.GetWindowLongW
        self.get_parent = ctypes.windll.user32.GetParent

        #   some of the WinAPI flags
        self.SWP_NOSIZE = 1
        self.SWP_NOMOVE = 2
        self.GWL_STYLE = -16
        self.SWP_NOZORDER = 4
        self.SWP_FRAMECHANGED = 32
        self.WS_MAXIMIZEBOX = 65536
        self.WS_MINIMIZEBOX = 131072

    def hide_minimize_maximize(self):
        '''Hide minimize and maximize button of the window'''

        global hide_minimiz_maximize

        hide_minimiz_maximize = True
        hwnd = self.get_parent(self.window.winfo_id())
        old_style = self.get_window_long(hwnd, self.GWL_STYLE)  # getting the old style
        new_style = old_style & ~ self.WS_MAXIMIZEBOX & ~ self.WS_MINIMIZEBOX  # building the new style (old style AND NOT Maximize AND NOT Minimize)
        self.set_window_long(hwnd, self.GWL_STYLE, new_style)  # setting new style
        self.set_window_pos(hwnd, 0, 0, 0, 0, 0, self.SWP_NOMOVE | self.SWP_NOSIZE | self.SWP_NOZORDER | self.SWP_FRAMECHANGED)  # updating non-client area

    def show_minimize_maximize(self,):
        '''Hide minimize and maximize button of the window'''

        global hide_minimiz_maximize

        hide_minimiz_maximize = False
        hwnd = self.get_parent(self.window.winfo_id())
        old_style = self.get_window_long(hwnd, self.GWL_STYLE)  # getting the old style
        new_style = old_style | self.WS_MAXIMIZEBOX | self.WS_MINIMIZEBOX  # building the new style (old style OR Maximize OR Minimize)
        self.set_window_long(hwnd, self.GWL_STYLE, new_style)  # setting new style
        self.set_window_pos(hwnd, 0, 0, 0, 0, 0, self.SWP_NOMOVE | self.SWP_NOSIZE | self.SWP_NOZORDER | self.SWP_FRAMECHANGED)  # updating non-client area


class Calculator:
    '''Calculator is a GUI script purely written in Python. This calculator is capable of performing addtion, subtraction,
       multiplication, division and percentage of any digtis numbers. Moreover, this calculator is able to store history of
       each calculation and is able to place itself to the top of any other application windows so that you could do calculation
       above any window.'''

    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.title('Calculator')
        self.master.iconbitmap('included files/icon.ico')

        self.hide_or_show = hide_or_show_maximize_minimize(self.master)
        self.decimal_placeable = True  # Not inserted decimal '.' yet.

        # Getting screen width and height of any system
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # pos_x and pos_y are calculated such that the window is at the center of the screen
        self.pos_x = self.screen_width // 2 - 460 // 2
        self.pos_y = self.screen_height // 2 - 340 // 2

        self.master.geometry('460x340+{}+{}'.format(self.pos_x, self.pos_y))
        self.master.resizable(0, 0)

        self.is_shown = False   # History is not shown yet

        self.var = StringVar()
        self.text_frame = Frame(self.master)
        self.text_area = Entry(self.text_frame, textvariable=self.var, borderwidth=1, width=25, bg='silver', font=("Arial", 20), cursor='arrow', justify=RIGHT, disabledbackground='white', disabledforeground='black', state='disabled')
        self.var.set('0')
        self.text_area.grid(row=0, column=0, columnspan=5)
        self.text_frame.place(x=10, y=10)

        # Buttons
        self.track = 0
        self.buttons_frame = Frame(self.master)  # Frame to place all buttons
        self.buttons_names = ['AC', 'DEL', '%', '÷', '9', '8', '7', '*', '6', '5', '4', '-', '3', '2', '1', '+', '.', '0', '=']   # buttons name

        # Adding buttons to the window
        for row in range(5):
            text = self.buttons_names[self.track: self.track + 4]

            for col, txt in enumerate(text):
                self.buttons = Button(self.buttons_frame, text=txt, width=10, height=2, bg='white', fg='black', activebackground='#cccccc', relief='groove', command=lambda txt=txt: set_value(txt), font=('Courier', 12))

                if txt == 'AC':
                    self.buttons.config(command=self.ac_command)
                    self.buttons.grid(row=row, column=col)

                elif txt == 'DEL':
                    self.buttons.config(command=self.del_command)
                    self.buttons.grid(row=row, column=col)

                elif txt == '=':
                    self.buttons.config(command=self.equals_to)
                    self.buttons.grid(row=row, column=col, columnspan=2, ipadx=55)

                else:
                    self.buttons.config(command=lambda txt=txt: self.keyaction(values=txt))
                    self.buttons.grid(row=row, column=col)

            self.track += 4

        self.buttons_frame.place(x=10, y=50)

        # History title
        self.history_label_frame = Frame(self.master)
        self.history_label = Label(self.history_label_frame, text='History', font=('Courier', 15, 'bold'), bg='#cccccc')
        self.history_label.grid(row=0, column=0)

        # Storing calculated history
        self.history_frame = Frame(self.master)
        self.history_area = Text(self.history_frame, width=52, height=13, borderwidth=0, cursor='arrow', bg='#cccccc')
        self.history_area.grid(row=0, column=0)

        # Button that has label "Show History"
        self.show_history_frame = Frame(self.master)
        self.show_history_button = Button(self.show_history_frame, text='Show History', relief=GROOVE, bg='#cccccc', activebackground='#cccccc', command=self.show_history)
        self.show_history_button.grid(row=0, column=0, ipadx=215, ipady=5)
        self.show_history_frame.place(x=0, y=303)

        # Button that has label "Hide History"
        self.hide_history_frame = Frame(self.master)
        self.hide_history_button = Button(self.hide_history_frame, text='Hide History', relief=GROOVE, bg='#cccccc', activebackground='#cccccc', command=self.hide_history)
        self.hide_history_button.grid(row=0, column=0, ipadx=215, ipady=5)

        # Attaching scrollbar to the text area
        self.scrollbar = Scrollbar(self.history_frame, orient="vertical", command=self.history_area.yview, cursor='arrow')
        self.history_area['yscrollcommand'] = self.scrollbar.set

        # Creating image object
        if PY3:
            self.pull_back_image = PhotoImage(file=self.resource_path('included files\\pull_back.png'))
            self.push_front_image = PhotoImage(file=self.resource_path('included files\\push_front.png'))

        else:
            self.pull_back_image = PIL.ImageTk.PhotoImage(PIL.Image.open(self.resource_path('included files\\pull_back.png')))
            self.push_front_image = PIL.ImageTk.PhotoImage(PIL.Image.open(self.resource_path('included files\\push_front.png')))

        # Buttons that push the window to the top of other window or pull the window from the top of other window
        self.push_front_frame = Frame(self.master)
        self.pull_back_image = PhotoImage(file='included files/pull_back.png')
        self.push_front_image = PhotoImage(file='included files/push_front.png')
        self.push_front_button = Button(self.push_front_frame, image=self.push_front_image, bg='white', activebackground='white', fg='black', relief='groove', compound='top', command=self.place_at_top)
        self.push_front_button.grid(row=0, column=0, padx=1, ipadx=13, ipady=4)
        self.push_front_frame.place(x=391, y=10)

        # Clear and info Button
        self.clear_history_frame = Frame(self.master, bg='#cccccc')
        self.info_button = Button(self.clear_history_frame, text='INFO', bg='white', activebackground='white', fg='black', relief='groove', command=self.info)
        self.clear_history_button = Button(self.clear_history_frame, text='CLEAR', bg='white', activebackground='white', fg='black', relief='groove', command=self.clear_history)
        self.info_button.grid(row=0, column=1, padx=10, ipadx=8, ipady=2)
        self.clear_history_button.grid(row=0, column=2, ipadx=5, ipady=2)

        # Binding keys
        self.master.bind('<Control-h>', lambda e: self.ctrl_h())
        self.master.bind('<Control-H>', lambda e: self.ctrl_h())
        self.master.bind('<Return>', self.equals_to)
        self.master.bind('<Delete>', self.ac_command)
        self.master.bind('<BackSpace>', self.del_command)
        self.master.bind('<Key>', lambda evt: self.keyaction(evt))

        self.clear_history()  # Calling history function
        self.show_scrollbar()

        self.master.config(bg='#cccccc')
        self.history_area.config(state=DISABLED)

        self.master.after(10, self.insert_zero)
        self.master.mainloop()

    def ac_command(self, event=None):
        '''Command for ac button, "a" key and "Delete" key from the keyboard'''

        self.text_area.delete(0, END)
        self.var.set('0')
        self.decimal_placeable = True

    def del_command(self, event=None):
        '''Commands for backspace key and del button'''

        get = self.var.get()

        if get == 'Cannot divide by ZERO':
            self.ac_command()

        else:
            if get[-1] == '.':   # Edge Cases 08
                self.decimal_placeable = True

            self.var.set(get[:-1])

            if not get:
                self.var.set('0')

    def get_updated_postition(self):
        '''Get x-coordinates and y-coordinates of the window if user displaces the window from the default position'''

        self.master.update()

        xpos = self.master.winfo_x()    # new x-coordinate of the window
        ypos = self.master.winfo_y()    # new y-coordinate of the window

        if xpos < 0:
            xpos = 5

        if xpos > self.screen_width - self.master.winfo_width() - 20:
            xpos = self.screen_width - self.master.winfo_width() - 20

        if ypos > 99:
            ypos = 99

        return (xpos, ypos)

    def place_at_top(self):
        '''Place the window to the top of any window opened in the background and resize some widgets'''

        xpos, ypos = self.get_updated_postition()
        xpos = self.screen_width - self.master.winfo_width() - 20   # This is done to place the window to the top right ot the screen

        if not hide_minimiz_maximize:
            self.hide_or_show.hide_minimize_maximize()
            self.push_front_button.config(image=self.pull_back_image)

            self.master.attributes('-topmost', True)
            self.master.geometry(f'460x340+{xpos}+{ypos}')
            self.hide_history()

        else:
            self.master.attributes('-topmost', False)
            self.hide_or_show.show_minimize_maximize()
            self.push_front_button.config(image=self.push_front_image)

    def show_history(self):
        '''Show history area and insert history label, history area, clear button, info button, place at top button and up arrow button'''

        self.is_shown = True
        xpos, ypos = self.get_updated_postition()

        self.text_area.config(width=29)
        self.push_front_frame.place_forget()
        self.history_frame.place(x=10, y=342)
        self.show_history_frame.place_forget()
        self.hide_history_frame.place(x=0, y=555)
        self.push_front_frame.place(x=270, y=310)
        self.history_label_frame.place(x=10, y=305)
        self.clear_history_frame.place(x=318, y=310)
        self.master.geometry(f'460x593+{xpos}+{ypos}')
        self.push_front_button.grid(row=0, column=0, ipadx=9, ipady=0)

    def hide_history(self):
        '''Hide history area and remove history label, history area, clear button, info button, place at top button and insert down arrow buton'''

        self.is_shown = False

        self.master.geometry(f'460x340')
        self.history_frame.place_forget()
        self.push_front_frame.place_forget()
        self.history_label_frame.place_forget()
        self.clear_history_frame.place_forget()
        self.show_history_frame.place(x=0, y=303)

        self.text_area.config(width=25)
        self.text_frame.place(x=10, y=10)
        self.push_front_frame.place(x=391, y=10)
        self.push_front_button.grid(row=0, column=0, padx=1, ipadx=13, ipady=4)

    def ctrl_h(self):
        '''Command for crl+h'''

        if not self.is_shown:
            self.show_history()

        else:
            self.hide_history()

    def keyaction(self, event=None, values=None):
        '''Check if the input key from both keyboard and buttons is between 0123456789+-*./%c

        Edge Cases:
            01. Make sure user only enters value within '0123456789+*-÷.%'.
            02. Do not repeat '.' (deicmal) until any operators is inserted.
            03. Remove default value '0' if '.' (decimal) is not supplied at the first place.
            04. If the last value is operators and another operator is entered again then replace the recent entered operators with the previous operators.
            05. Do not supply any operators if the last value is '.' (decimal).
            06. Do not make calculation if value is operator except '%'.
            07. Replace "Cannot divide by Zero" with any number when supplied else replace with '0'
            08. Do not repeat '.' (decimal) when removed using "DEL" button or "Backspace" key.
            09. Insert '0' before '.' (decimal) when only '.' (decimal) is supplied.
            10. Do not insert '%' after operator or '%' itself.
            11. Don't insert any number if the last value is '%' except operators
            12. If user inserts '0' right after operator follwed by  numbers then remove that '0'. Eg: 450+052, remove '0' from 052 which changes to 450+52
                because "eval" function treats "450+052" as invalid expression except if user inserts '0.022' here don't remove '0' from '022' beacuse it
                contains '.' (decimal) which is valid.
            13. If user inserts '45.00000' and enters any operators after that then remove '.00000'
            14. If (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13) are not caused then insert as per the user.
        '''

        if event:   # Check if the value is provided from the keyboard
            value = event.char.replace('/', '÷')

        else:      # Check if the value is provided from clicking button
            value = values

        if value in '0123456789+-*.÷%':   # Edge Cases 01
            try:
                get = self.var.get()

                if get == 'Cannot divide by ZERO':   # Edge Cases 07
                    if value in '0123456789':
                        self.var.set('')
                        val = value

                    elif value in '+-.*÷%':
                        self.var.set('')
                        val = '0'

                elif value in '+-.*÷%' and self.avoid_duplicate_operator(value):   # Edge Cases 2, 5, 6, 10 and 11 in avoid_duplicate_operator function
                    if self.decimal_placeable and value == '.':   # Edge Cases 02
                        val = get + value
                        self.decimal_placeable = False

                    if value != '.':
                        try:
                            if int(get[get.rfind('.') + 1:]) == 0:   # Edge Cases 13
                                val = get[:get.rfind('.')] + value

                            else:
                                val = get + value
                            self.decimal_placeable = True

                        except ValueError:
                            val = get + value

                elif value in '0123456789':
                    if any(s in get for s in '+-*÷') and get[-1] in '0123456789' and get[-2] == '0' and self.decimal_placeable:    # Edge Cases 12
                        val = f'{get[:-2]}{get[-1]}{value}'

                    elif get[:2] != '0.':
                        if get[-1] == '%' and value in '0123456789':   # Edge Cases 11
                            pass

                        elif get[0] == '0' and get[1] not in '+-*÷':  # This condition is to produce IndexError if the first value in text area is 0 and the second value is not operator
                            pass

                        else:
                            val = get + value

                    else:     # Edge Cases 14
                        val = get + value

                self.var.set(val)

            except IndexError:
                val = get.lstrip('0') + value   # Edge Cases 03
                self.var.set(val)

            except UnboundLocalError:   # This error is caused when user enters '.' (decimal) when previous answer has already decimal in text area
                pass

        elif value.lower() == 'a':
            self.ac_command()
            self.clear_history()

        elif value.lower() == 'c':
            self.ac_command()

        elif value.lower() is 'h':
            self.clear_history()

        elif value.lower() == 'i':
            self.info()

        elif value.lower() == 'q':
            self.master.destroy()

    def avoid_duplicate_operator(self, value=None):
        '''Restricts user for entering continous operators (+ - ÷ *)'''

        get = self.var.get()

        if get[-1] in '+-*÷' and value == '.':   # Edge Cases 09
            val = get + '0.'
            self.var.set(val)
            self.decimal_placeable = False
            return False

        if get[-1] == '.':   # Edge Cases 05
            return False

        if get[-1] == '%' and value in '+-*÷':
            val = get + value
            self.var.set(val)
            return False

        if get[-1] == value == '%' or (get[-1] in '+-*÷' and value == '%'):    # Edge Case 10
            return False

        if get[-1] in '+-*÷%' and value in '+-*÷%':   # Edge Cases 04
            val = get[:-1] + value
            self.var.set(val)
            return False

        return True

    def equals_to(self, event=None):
        '''Calculate the given equation'''

        value = self.var.get().replace('%', '/100').replace('÷', '/')

        try:
            if self.count_operators(value):
                get = self.var.get()
                answer = str(eval(value))

                if '.' in answer:   # if answer contains '.' (decimal)
                    split = answer.split('.')

                    if int(split[1]) == 0:   # Removing .0 when the value in answer after '.' (decimal) is all '0'
                        self.var.set(split[0])
                        hist = f'{get} = {split[0]}\n'
                        self.decimal_placeable = True

                    else:   # If value in answer after '.'(decimal) is not all '0'
                        self.var.set(answer)
                        hist = f'{get} = {answer}\n'
                        self.decimal_placeable = False

                else:  # if answer does not contain '.' (decimal)
                    self.var.set(answer)
                    hist = f'{get} = {answer}\n'
                    self.decimal_placeable = True

                self.history(hist)

        except ZeroDivisionError:    # This error is caused if any number is divided by "0"
            winsound.MessageBeep()
            self.var.set('Cannot divide by ZERO')

    def count_operators(self, value):
        '''Counts number of operators in the expression.

           If the number of operators is more than 1 then only the expression can be calculated else nothing will happen
           when "=" button or "enter" key is pressed'''

        count = 0

        if self.var.get()[-1] in '+-*÷':    # Edge Cases 06
            return False

        if not value.startswith('-'):
            count += 1

        for val in value:
            if val in '+-*/':
                count += 1

        if count > 1:
            return True

        return False

    def show_scrollbar(self):
        '''show scrollbar when text is more than the height of text area'''

        if self.history_area.cget('height') < int(self.history_area.index('end-1c').split('.')[0]):
            self.scrollbar.grid(column=1, row=0, sticky=N + S)
            self.history_area.config(yscrollcommand=self.scrollbar.set)
            self.master.after(100, self.hide_scrollbar)

        else:
            self.master.after(100, self.show_scrollbar)

    def hide_scrollbar(self):
        '''hide scrollbar when text is less than the height of text area'''

        if self.history_area.cget('height') >= int(self.history_area.index('end-1c').split('.')[0]):
            self.scrollbar.grid_forget()
            self.history_area.config(yscrollcommand=None)
            self.master.after(100, self.show_scrollbar)

        else:
            self.master.after(100, self.hide_scrollbar)

    def history(self, value=None):
        '''Display previous calculations'''

        self.history_area.config(state=NORMAL)

        if self.history_area.get('1.0', 'end-1c') == 'There\'s no history yet.':
            self.history_area.delete('1.0', END)

        self.history_area.insert(END, value)
        self.history_area.config(state=DISABLED)

    def clear_history(self):
        '''Clear calculation history'''

        self.history_area.config(state=NORMAL)
        self.history_area.delete('1.0', 'end')
        self.history_area.insert('end', 'There\'s no history yet.')
        self.history_area.config(state=DISABLED)

    def insert_zero(self):
        '''Insert zero when there is no value in entry box.

           This is especially witten because when user turn on or off the numlock then "0" gets removed
           from the entry box. So, this function reinserts removed "0" to the entry box even if user
           turn on or off the numlock only if there is no any value in entry box.'''

        get = self.var.get().strip()

        if not get:
            self.var.set('0')

        self.master.after(10, self.insert_zero)

    def info(self):
        '''Show information about binded keys for different actions'''

        values = '\n'.join(['Q = Quit', 'A = Clear all', 'H = Clear history', 'C = Clear text box', 'I = Show this window', 'Ctrl+h = Hide / Show history'])
        messagebox.showinfo('Key Bindings', values)

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
    Calculator()
