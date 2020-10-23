import os
import sys
import ctypes
import string
from math import *
from tkinter import *
from tkinter import messagebox


class Calculator:
    '''Calculator is a GUI script purely written in Python. This calculator is capable of performing addition, subtraction,
       multiplication, division, percentage of any digits numbers and calculation of some trigonometric functions. Moreover,
       this calculator is able to store history of each calculation and is able to place itself to the top of any other
       application windows so that you could do calculation above any window.'''

    def __init__(self):
        self.prev_ans = '0'
        self.operators = '+-*/^'
        self.digits = '0123456789'
        self.is_valid_brackets = True
        self.decimal_placeable = True
        self.hide_minimiz_maximize = False
        self.is_shown = False   # History is not shown yet
        self.zero_division_error = 'Cannot Divide By Zero'
        self.trigonometric_functions = ['sin', 'sin-\u00B9', 'cos', 'cos-\u00B9', 'log', 'tan', 'tan-\u00B9', 'abs', 'deg', 'rad']

        self.master = Tk()
        self.master.withdraw()
        self.master.title('Calculator')
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))

        self.hide_or_show = hide_or_show_maximize_minimize(self.master)

        self.var = StringVar()
        self.text_frame = Frame(self.master)
        self.text_area = Entry(self.text_frame, textvariable=self.var, borderwidth=1, width=47, bg='silver', font=("Arial", 20), cursor='arrow', justify=RIGHT, disabledbackground='white', disabledforeground='black', state='disabled')
        self.var.set('0')
        self.text_area.grid(row=0, column=0)

        # Creating image object
        self.pull_back_image = PhotoImage(file=self.resource_path('included_files\\pull_back.png'))
        self.push_front_image = PhotoImage(file=self.resource_path('included_files\\push_front.png'))

        # Buttons that push the window to the top of other window or pull the window from the top of other window
        self.push_front_button = Button(self.text_frame, image=self.push_front_image, bg='white', activebackground='white', fg='black', relief='groove', compound='top', cursor='hand2', command=self.place_at_top)
        self.push_front_button.grid(row=0, column=1, ipadx=15, ipady=3)
        self.text_frame.pack(anchor='w')

        # Buttons
        self.track = 0
        self.buttons_frame = Frame(self.master)  # Frame to place all buttons
        self.buttons_names = ['AC', 'DEL', '%', '/', 'x^y', 'abs', '(', '7', '8', '9', '*', 'n!', 'π', ')', '4', '5', '6', '-', 'sin', 'sin-\u00B9', 'deg', '1', '2', '3', '+', 'cos',
                              'cos-\u00B9', 'rad', '.', '0', '=', 'log', 'tan', 'tan-\u00B9', 'Prev Ans']   # buttons name

        # Adding buttons to the window
        for row in range(5):
            text = self.buttons_names[self.track: self.track + 7]

            for col, txt in enumerate(text):
                self.buttons = Button(self.buttons_frame, text=txt, width=10, height=2, bg='white', fg='black', activebackground='#cccccc', relief='groove', font=('Courier', 12))

                if txt == 'AC':
                    self.buttons.config(command=self.ac_command)

                elif txt == 'DEL':
                    self.buttons.config(command=self.del_command)

                elif txt == '=':
                    self.buttons.config(command=self.equals_to)

                elif txt in self.trigonometric_functions:
                    txt += '('
                    self.buttons.config(command=lambda txt=txt: self.keyaction(values=txt))

                else:
                    self.buttons.config(command=lambda txt=txt: self.keyaction(values=txt))

                self.buttons.grid(row=row, column=col)

            self.track += 7

        self.buttons_frame.pack()

        # History title
        self.history_frame = Frame(self.master, bg='#cccccc')
        self.history_label = Label(self.history_frame, text='History', font=('Courier', 15, 'bold'), bg='#cccccc')
        self.history_label.grid(row=0, column=0, sticky='w')

        # Clear and info Button
        self.button_framme = Frame(self.history_frame, bg='#cccccc')
        self.info_button = Button(self.button_framme, text='INFO', bg='white', activebackground='white', fg='black', relief='groove', cursor='hand2', command=self.info)
        self.clear_history_button = Button(self.button_framme, text='CLEAR', bg='white', activebackground='white', fg='black', relief='groove', cursor='hand2', command=self.clear_history)
        self.info_button.grid(row=0, column=1, padx=10, ipadx=8, ipady=2)
        self.clear_history_button.grid(row=0, column=2, ipadx=5, ipady=2)
        self.button_framme.grid(row=0, column=1)

        self.history_area_frame = Frame(self.history_frame)
        self.history_area = Text(self.history_area_frame, width=52, height=13, borderwidth=0, cursor='arrow', bg='#cccccc')
        self.history_area.insert(END, 'There\'s no history yet.')
        self.history_area.grid(row=0, column=0)
        self.history_area_frame.grid(row=1, column=0)

        # Button that has label "Show History"
        self.show_history_frame = Frame(self.master, bg='#cccccc')
        self.show_history_button = Button(self.show_history_frame, text='Show History', relief=GROOVE, bg='#cccccc', activebackground='#cccccc', cursor='hand2', width=47, command=self.show_history)
        self.show_history_button.grid(row=0, column=0, ipadx=215, ipady=5)
        self.show_history_frame.pack(anchor='w')

        # Attaching scrollbar to the text area
        self.scrollbar = Scrollbar(self.history_area_frame, orient="vertical", command=self.history_area.yview, cursor='arrow')
        self.history_area['yscrollcommand'] = self.scrollbar.set

        self.master.config(bg='#cccccc')
        self.history_area.config(state=DISABLED)

        self.master.bind('<Key>', self.keyaction)
        self.master.bind('<Control-h>', lambda e: self.ctrl_h())
        self.master.bind('<Control-H>', lambda e: self.ctrl_h())
        self.master.bind('<Return>', lambda e: self.equals_to())
        self.master.bind('<BackSpace>', lambda e: self.del_command())

        self.show_scrollbar()
        self.master.after(10, self.insert_zero)
        self.initial_position()
        self.re_position()
        self.master.mainloop()

    def initial_position(self):
        '''Position when the program opens'''

        self.master.update_idletasks()

        # Getting screen width and height of any system
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # pos_x and pos_y are calculated such that the window is at the center of the screen
        self.pos_x = self.screen_width // 2 - self.master.winfo_reqwidth() // 2
        self.pos_y = self.screen_height // 2 - self.master.winfo_reqheight() // 2

        self.master.geometry('+{}+{}'.format(self.pos_x, self.pos_y))
        self.master.after(250, self.master.deiconify)
        self.master.resizable(0, 0)

    def re_position(self):
        '''Position the window the window gets out of the screen'''

        self.master.update_idletasks()

        x_pos = self.master.winfo_x()
        y_pos = self.master.winfo_y()

        width = self.master.winfo_reqwidth()
        height = self.master.winfo_reqheight()

        if x_pos < 0:
            x_pos = 10

        if x_pos + width > self.screen_width:
            x_pos = self.screen_width - width - 10

        if y_pos + height > self.screen_height:
            y_pos = self.screen_height - height - 80

        self.master.geometry(f'+{x_pos}+{y_pos}')
        self.master.after(50, self.re_position)

    def show_history(self):
        '''Show history area and insert history label, history area, clear button, info button, place at top button and up arrow button'''

        self.is_shown = True
        self.history_frame.pack()
        self.show_history_frame.pack_forget()
        self.show_history_frame.pack()
        self.history_frame.pack(anchor='w', padx=10, pady=5)
        self.show_history_button.config(text='Hide History', command=self.hide_history)

    def hide_history(self):
        '''Hide history area and remove history label, history area, clear button, info button, place at top button and insert down arrow button'''

        self.is_shown = False
        self.history_frame.pack_forget()
        self.show_history_button.config(text='Show History', command=self.show_history)

    def place_at_top(self):
        '''Place the window to the top of any window opened in the background and resize some widgets'''

        if not self.hide_minimiz_maximize:
            self.hide_minimiz_maximize = True
            self.hide_or_show.hide_minimize_maximize()
            self.push_front_button.config(image=self.pull_back_image)

            self.master.attributes('-topmost', True)
            self.hide_history()

        else:
            self.hide_minimiz_maximize = False
            self.master.attributes('-topmost', False)
            self.hide_or_show.show_minimize_maximize()
            self.push_front_button.config(image=self.push_front_image)
            self.master.resizable(0, 0)

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

    def ac_command(self):
        '''Remove everything from entry_box and insert '0' when ac_button or 'a' key is pressed'''

        self.var.set('')
        self.var.set('0')
        self.decimal_placeable = True

    def insert_zero(self):
        '''Insert zero when there is no value in entry box.

           This is especially written because when user turn on or off the numlock then "0" gets removed
           from the entry box. So, this function reinserts removed "0" to the entry box even if user
           turn on or off the numlock only if there is no any value in entry box.'''

        get = self.var.get()

        if not get:
            self.var.set('0')

        self.master.after(10, self.insert_zero)

    def ctrl_h(self):
        '''Command for Ctrl+h'''

        if not self.is_shown:
            self.show_history()

        else:
            self.hide_history()

    def clear_all(self, event=None):
        '''Function to bind with key 'a' or 'A' '''

        self.ac_command()
        self.clear_history()

    def info(self, event=None):
        '''Show information about binded keys for different actions'''

        key_bindings = ['Q = Quit',
                        'A = Clear all',
                        'T = Place At Top',
                        'H = Clear history',
                        'C = Clear text box',
                        'I = Show this window',
                        'Ctrl+h = Hide / Show history']

        values = '\n'.join(key_bindings)
        messagebox.showinfo('Key Bindings', values)

    def del_command(self):
        '''Remove last character of entry_box when del_button or backspace is pressed'''

        try:
            entry_get = self.var.get()

            if entry_get == self.zero_division_error:
                self.var.set('')
                entry_get = '0'

            elif entry_get[-1] == '(' and entry_get[-2] in string.ascii_letters + '¹':  # Edge Case 5(iii)
                if entry_get[-2:] == '¹(':
                    entry_get = entry_get[:-5]

                else:
                    entry_get = entry_get[:-3]

            elif entry_get[-1] in self.operators:
                # Assign self.decimal_placeable to True if there is not any '.' between two operators i.e 850+450+ This means '.' can be placed
                # Assign self.decimal_placeable to False if there is '.' between two operators i.e 850+45.58+ This means decimal '.' cannot be placed

                found = True
                last_index = len(entry_get) - 2

                while found and last_index > 0:
                    last_value = entry_get[last_index]

                    if last_value == '.':
                        found = False
                        self.decimal_placeable = False

                    elif last_value in '+-*/':
                        found = False
                        self.decimal_placeable = True

                    last_index -= 1

            elif entry_get[-1] == '.':
                self.decimal_placeable = True

            entry_get = entry_get[:-1]

            if entry_get:
                self.var.set(entry_get)

            else:
                self.var.set('0')

        except IndexError:
            self.var.set('0')

    def equals_to(self, event=None):
        ''' When '=' button or enter key is presses:
                i. Make Calculation if two or more operators are in entry_box except '%'
                ii. Make calculation only if the last_value in entry_box has no any operators
                iii. Replace '%' with '/100', '^' with '**'.
                iv. Make calculation if only trigonometric functions are found without any operators'''

        try:
            entry_get = to_calculate = self.var.get()

            replace = {func: 'a' + func.split('-')[0] for func in self.trigonometric_functions if '-' in func and func in entry_get}
            replace.update({'^': '**', '%': '/100', 'π': 'pi', 'deg': 'degrees', 'rad': 'radians'})

            for k, v in replace.items():     # iii.
                to_calculate = to_calculate.replace(k, v)

            if entry_get.count('(') != entry_get.count(')'):  # Edge Case 9(vi)
                messagebox.showerror('Invalid Brackets', 'Brackets are not inserted in order')
                return

            count = sum([1 for x in entry_get if x in self.operators + '%'])   # Counting Operators

            if count == 0:
                count = sum([1 for x in self.trigonometric_functions + ['factorial'] if x in entry_get])  # iv

            if count > 0 and entry_get[-1] not in self.operators:   # i, ii
                calculated = self.prev_ans = str(eval(to_calculate))

                self.var.set(calculated)
                self.history(f'{entry_get} = {calculated}\n')

                if '.' in calculated:
                    self.decimal_placeable = False    # Making '.' unacceptable if the answer has '.' in it

        except ZeroDivisionError:
            self.var.set(self.zero_division_error)

        except ValueError:
            self.var.set('Inverse function must have value between 0 & 1')

        except OverflowError:
            self.var.set('OverflowError')

    def keyaction(self, event=None, values=None):
        ''' Edge Case:
                1. When only numbers(0-9) are inputed:
                    i. If initial_value in entry_box is '0' then remove that initial '0' and insert the input value.
                    ii. Insert '*' and value when number is inputed after adding '%'
                    iii. If initial_vaule in entry_box is not '0' then append the input_value with the value in entry_box

                2. When only operators(+-*/) are inputed:
                    i.Insert '.0' when any operator is inputed after '.'
                    ii. Insert user_input operator in entry_box if last value in entry_box has no any operator.
                    iii. If last value in entry_box and user_input is operator then replace entry_box operator with user_input operator.

                3. When decimal_point(.) is inputed:
                    i. Insert '.' when not insert previously.
                    ii. Insert '0.' when '.' is inputed after any operator or '('
                    iii. Don't repeat decimal unless any other operator is inputed

                4. When percentage('%') is inserted:
                    i. Insert '%' only if the last value in entry_box is not in '+-/*%.'

                5. When trigonometric function is pressed:
                    i. If initial_value in entry_box is '0' then remove that initial '0' and insert trigonometric_functions.
                    ii. Insert trigonometric functions only if the last value in entry_get is operator, '('.
                    iii. Remove trigonometric function if 'del' button or 'backspace' key is pressed.

                6. When 'n!' button is pressed:
                    i. If initial_value in entry_box is '0' then remove that initial '0' and insert 'factorial('.
                    ii. Insert 'factorial(' only if there is only operator at the end.

                7. When 'π' button is pressed:
                    i. If initial_value in entry_box is '0' then remove that initial '0' and insert 'π'.
                    ii. Insert 'π' only if there is only operator or '(' at the end.

                8. When 'Prev Ans' button is pressed:
                    i. If initial_value in entry_box is '0' then remove that initial '0' and insert previous_answer.
                    ii. If there is no initial_value then insert the previous_answer only if the last value in entry_box is in operator and ( .
                    iii. Don't insert 'prev_ans' if 'prev_ans' have decimal and decimal_placeable is False or last_value in entry_get is in  ), % or last_value is numbers.
                    iv. If last_value in entry_get is '-' and 'prev_ans' also have '-' then put wrap the 'prev_ans' with '()'

                9. When '(' or ')' button is pressed:
                    i.  If initial_value in entry_box is '0' then remove that and insert '('.
                    ii. Don't insert ')' if the initial value is '('.
                    iii. Don't insert '(' if last_value is in numbers, ')%'.
                    iv. Don't insert ')' if number of '(' is 0.
                    v. Don't insert ')' if the number of '(' and ')' are equal.
                    vi. Do not do calculation if the number of  '(' and ')' are equal.'''

        try:
            valid = list(self.digits + self.operators) + [x + '(' for x in self.trigonometric_functions] + ['(', ')', '%', '.', 'π', 'x^y', 'n!']

            if event:
                char = event.char

            else:
                char = values

            entry_get = self.var.get()

            if entry_get in [self.zero_division_error, 'OverflowError', 'Inverse function must have value between 0 & 1']:
                entry_get = '0'

            if char == 'x^y':
                char = '^'

            if char in valid:
                if char in self.digits:
                    set_var = self.edge_case_1(entry_get, char)   # Edge Case 1

                elif char in self.operators:
                    set_var = self.edge_case_2(entry_get, char)   # Edge Case 2

                elif char == '.':
                    set_var = self.edge_case_3(entry_get, char)   # Edge Case 3

                elif char == '%':
                    set_var = self.edge_case_4(entry_get, char)   # Edge Case 4

                elif char.strip('(') in self.trigonometric_functions:
                    set_var = self.edge_case_5(entry_get, char)   # Edge Case 5

                elif char == 'n!':
                    set_var = self.edge_case_6(entry_get, char)   # Edge Case 6

                elif char == 'π':
                    set_var = self.edge_case_7(entry_get, char)   # Edge Case 7

                elif char in ['(', ')']:
                    set_var = self.edge_case_9(entry_get, char)  # Edge Case 9

            elif char.lower() == 'q':
                self.master.destroy()

            elif char.lower() == 'a':
                self.clear_all()

            elif char.lower() == 'i':
                self.info()

            elif char.lower() == 'h':
                self.clear_history()

            elif char.lower() == 'c':
                self.ac_command()

            elif char.lower() == 't':
                self.place_at_top()

            elif char == 'Prev Ans':
                set_var = self.edge_case_8(entry_get)  # Edge Case 8

            if set_var:
                self.var.set(set_var)

        except Exception:  # Just in case
            pass

    def edge_case_1(self, entry_get, char):
        '''When only numbers are entered'''

        if len(entry_get) == 1 and entry_get[0] == '0':    # Edge Case 1(i)
            self.var.set('')
            set_var = char

        elif entry_get[-1] == '%':   # Edge Case 1(ii)
            set_var = entry_get + '*' + char

        else:   # Edge Case 1(iii)
            set_var = entry_get + char

        return set_var

    def edge_case_2(self, entry_get, char):
        '''When only operators are entered'''

        if entry_get[-1] == '.':   # Edge Case 2(i)
            set_var = entry_get + '0' + char

        elif entry_get[-1] not in self.operators + '(':    # Edge Case 2(ii) and 5(vii)
            set_var = entry_get + char

        elif entry_get[-1] in self.operators:   # Edge Case 2(iii)
            set_var = entry_get[:-1] + char

        self.decimal_placeable = True

        return set_var

    def edge_case_3(self, entry_get, char):
        '''When decimal_point (.) is entered'''

        if self.decimal_placeable:
            if entry_get[-1] in self.operators + '(':  # Edge Case 3(ii)
                set_var = entry_get + '0.'

            else:   # Edge Case 3(i)
                set_var = entry_get + char

            self.decimal_placeable = False   # Edge Case 3(iii)
            return set_var

    def edge_case_4(self, entry_get, char):
        '''When '%' is entered'''

        if entry_get[-1] not in self.operators + '.%(':   # Edge Case 4(i) and 5(vi)
            set_var = entry_get + char

            return set_var

    def edge_case_5(self, entry_get, char):
        '''When trigonometric functions is entered'''

        if len(entry_get) == 1 and entry_get[0] == '0':  # Edge Case 5(i)
            self.var.set('')
            set_var = char

        elif entry_get[-1] in self.operators + '(':  # Edge Case 5(ii)
            set_var = entry_get + char

        else:
            return

        return set_var

    def edge_case_6(self, entry_get, char):
        '''When 'n!' button is pressed'''

        if len(entry_get) == 1 and entry_get[0] == '0':  # Edge Case 6(i)
            set_var = 'factorial('

        elif entry_get[-1] in self.operators + '(':  # Edge Case 6(ii)
            set_var = entry_get + 'factorial('

        return set_var

    def edge_case_7(self, entry_get, char):
        '''When 'π' button is pressed'''

        if len(entry_get) == 1 and entry_get[0] == '0':  # Edge Case 7(i)
            set_var = 'π'

        elif entry_get[-1] in self.operators + '(':  # Edge Case 7(ii)
            set_var = entry_get + char

        return set_var

    def edge_case_8(self, entry_get):
        '''When 'Prev Ans' button is pressed.'''

        if len(entry_get) == 1 and entry_get[0] == '0':  # Edge Case 8(i)
            set_var = self.prev_ans

        elif self.prev_ans and entry_get[-1] == self.prev_ans[0] == '-':  # Edge Case 8(iv)
            set_var = f'{entry_get}({self.prev_ans})'

        elif entry_get[-1] in self.operators + '(':  # Edge Case 8(ii)
            set_var = entry_get + self.prev_ans

        elif '.' in self.prev_ans and self.decimal_placeable is False or entry_get[-1] in '%)' + self.digits:  # Edge Case 8(iii)
            return

        return set_var

    def edge_case_9(self, entry_get, char):
        '''When '(' or ')' button is pressed'''

        start_bracket = entry_get.count('(')
        end_bracket = entry_get.count(')')

        if len(entry_get) == 1 and entry_get[0] == '0':  # Edge Case 9(i)
            set_var = char

        elif entry_get[-1] == '(' and char == ')':  # Edge Case 9(ii)
            return

        elif entry_get[-1] in self.digits + ')%' and char == '(':  # Edge Case 9(iii)
            return

        elif start_bracket == 0 and char == ')':  # Edge Case 9(iv)
            return

        elif start_bracket == end_bracket and char == ')':  # Edge Case 9(v)
            return

        else:
            set_var = entry_get + char

        return set_var

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS.

        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


class hide_or_show_maximize_minimize:
    '''Hide the minimize and maximize button when the window is place at the top of other applications windows.
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

        hwnd = self.get_parent(self.window.winfo_id())
        old_style = self.get_window_long(hwnd, self.GWL_STYLE)  # getting the old style
        new_style = old_style & ~ self.WS_MAXIMIZEBOX & ~ self.WS_MINIMIZEBOX  # building the new style (old style AND NOT Maximize AND NOT Minimize)
        self.set_window_long(hwnd, self.GWL_STYLE, new_style)  # setting new style
        self.set_window_pos(hwnd, 0, 0, 0, 0, 0, self.SWP_NOMOVE | self.SWP_NOSIZE | self.SWP_NOZORDER | self.SWP_FRAMECHANGED)  # updating non-client area

    def show_minimize_maximize(self,):
        '''Hide minimize and maximize button of the window'''

        hwnd = self.get_parent(self.window.winfo_id())
        old_style = self.get_window_long(hwnd, self.GWL_STYLE)  # getting the old style
        new_style = old_style | self.WS_MAXIMIZEBOX | self.WS_MINIMIZEBOX  # building the new style (old style OR Maximize OR Minimize)
        self.set_window_long(hwnd, self.GWL_STYLE, new_style)  # setting new style
        self.set_window_pos(hwnd, 0, 0, 0, 0, 0, self.SWP_NOMOVE | self.SWP_NOSIZE | self.SWP_NOZORDER | self.SWP_FRAMECHANGED)  # updating non-client area


if __name__ == '__main__':
    Calculator()
