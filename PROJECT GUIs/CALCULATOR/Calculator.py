import os
import sys
from math import *
from tkinter import *
from tkinter import messagebox


class Calculator:
    def __init__(self):
        self.track = 0
        self.prev_ans = '0'
        self.is_at_top = False
        self.operators = '+-*/^'
        self.digits = '0123456789'
        self.is_valid_brackets = True
        self.decimal_placeable = True
        self.width, self.height = 505, 286
        self.zero_division_error = 'Cannot Divide By Zero'
        self.trigonometric_functions = ['sin', 'sin-\u00B9', 'cos', 'cos-\u00B9', 'log', 'tan', 'tan-\u00B9', 'abs', 'deg', 'rad']
        self.buttons_names = ['AC', 'DEL', '%', '/', 'x^y', 'abs', '(', '7', '8', '9', '*', 'n!', 'π', ')', '4', '5', '6', '-', 'sin', 'sin-\u00B9', 'deg', '1', '2', '3', '+', 'cos',
                              'cos-\u00B9', 'rad', '.', '0', '=', 'log', 'tan', 'tan-\u00B9', 'Prev\nAns']   # buttons name

        self.master = Tk()
        self.master.title('Calculator')

        self.var = StringVar()
        self.text_frame = Frame(self.master)
        self.text_area = Entry(self.text_frame, textvariable=self.var, borderwidth=1, width=47, bg='silver', font=('Arial', 20), cursor='arrow', justify=RIGHT, disabledbackground='white', disabledforeground='black', state='disabled')
        self.var.set('0')
        self.text_area.grid(row=0, column=0, sticky='NSEW')

        # Creating image object
        self.pull_back_image = PhotoImage(file=self.resource_path('included_files\\pull_back.png'))
        self.push_front_image = PhotoImage(file=self.resource_path('included_files\\push_front.png'))

        self.push_front_button = Button(self.text_frame, image=self.push_front_image, bg='white', activebackground='white', fg='black', relief='groove', compound='top', cursor='hand2', command=self.place_at_top)
        self.push_front_button.grid(row=0, column=1, ipadx=15, ipady=3, sticky='NSEW')
        self.text_frame.grid(row=0, column=0, sticky='NSEW')

        self.buttons_frame = Frame(self.master)
        self.buttons_frame.grid(row=1, column=0, sticky='nsew')

        for row in range(5):
            text = self.buttons_names[self.track: self.track + 7]

            for col, txt in enumerate(text):
                button = Button(self.buttons_frame, text=txt, width=10, height=2, bg='white', fg='black', activebackground='#cccccc', relief='groove', font=('Courier', 12))
                button.grid(row=row, column=col, sticky='NSEW')

                if txt == 'AC':
                    button.config(command=self.ac_command)

                elif txt == 'DEL':
                    button.config(command=self.del_command)

                elif txt == '=':
                    button.config(command=self.equals_to)

                elif txt in self.trigonometric_functions:
                    txt += '('
                    button.config(command=lambda txt=txt: self.keyaction(values=txt))

                else:
                    button.config(command=lambda txt=txt: self.keyaction(values=txt))

            self.track += 7

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        for i in range(7):
            if i < 5:
                self.buttons_frame.grid_rowconfigure(i, weight=1)

            self.buttons_frame.grid_columnconfigure(i, weight=1)

        self.initial_position()

        self.master.bind('<Key>', self.keyaction)
        self.master.minsize(self.width, self.height)
        self.master.bind('<Return>', lambda e: self.equals_to())
        self.master.bind('<BackSpace>', lambda e: self.del_command())

        self.master.mainloop()

    def initial_position(self):
        '''Position when the program opens'''

        self.master.withdraw()
        self.master.update()

        self.master.iconbitmap(self.resource_path('included_files\\icon.ico'))

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        pos_x = screen_width // 2 - self.width // 2
        pos_y = screen_height // 2 - self.height // 2

        self.master.geometry(f'{self.width}x{self.height}+{pos_x}+{pos_y}')
        self.master.deiconify()

        self.master.after(10, self.insert_zero)

    def place_at_top(self):
        '''Place the window to the top of any window opened in the background and resize some widgets'''

        if self.is_at_top:
            self.is_at_top = False
            self.master.overrideredirect(False)
            self.master.attributes('-topmost', False)
            self.push_front_button.config(image=self.push_front_image)

        else:
            self.is_at_top = True
            self.master.overrideredirect(True)
            self.master.attributes('-topmost', True)
            self.push_front_button.config(image=self.pull_back_image)

            pos_x = self.master.winfo_screenwidth() - self.width - 10
            self.master.geometry(f'{self.width}x{self.height}+{pos_x}+3')

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

            if entry_get.count('(') != entry_get.count(')'):  # Edge Case 9(vii)
                messagebox.showerror('Invalid Brackets', 'Brackets are not inserted in order')
                return

            count = sum([1 for x in entry_get if x in self.operators + '%'])   # Counting Operators

            if count == 0:
                count = sum([1 for x in self.trigonometric_functions + ['factorial'] if x in entry_get])  # iv

            if count > 0 and entry_get[-1] not in self.operators:   # i, ii
                calculated = self.prev_ans = str(eval(to_calculate))

                self.var.set(calculated)

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
                    ii. Don't insert ')' if the initial value in entry_box is '0'.
                    iii. Don't insert ')' if the initial value is '('.
                    iv. Don't insert '(' if last_value is in numbers, ')%'.
                    v. Don't insert ')' if number of '(' is 0.
                    vi. Don't insert ')' if the number of '(' and ')' are equal.
                    vii. Do not do calculation if the number of  '(' and ')' are equal.'''

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

            elif char.lower() == 'i':
                self.info()

            elif char.lower() in 'ac':
                self.ac_command()

            elif char.lower() == 't':
                self.place_at_top()

            elif char == 'Prev\nAns':
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
            if char != ')':  # Edge Case 9(ii)
                set_var = char

        elif entry_get[-1] == '(' and char == ')':  # Edge Case 9(iii)
            return

        elif entry_get[-1] in self.digits + ')%' and char == '(':  # Edge Case 9(iv)
            return

        elif start_bracket == 0 and char == ')':  # Edge Case 9(v)
            return

        elif start_bracket == end_bracket and char == ')':  # Edge Case 9(vi)
            return

        else:
            set_var = entry_get + char

        return set_var

    def info(self, event=None):
        '''Show information about binded keys for different actions'''

        key_bindings = ['Q = Quit',
                        'A = Clear all',
                        'T = Place At Top',
                        'C = Clear text box',
                        'I = Show this window']

        values = '\n'.join(key_bindings)
        messagebox.showinfo('Key Bindings', values)

    def resource_path(self, relative_path):
        '''Get absolute path to resource from temporary directory

        In development:
            Gets path of files that are used in this script like icons, images or file of any extension from current directory

        After compiling to .exe with pyinstaller and using --add-data flag:
            Gets path of files that are used in this script like icons, images or file of any extension from temporary directory'''

        try:
            base_path = sys._MEIPASS  # PyInstaller creates a temporary directory and stores path of that directory in _MEIPASS

        except AttributeError:
            path = sys.argv

            if path:
                base_path = os.path.split(path[0])[0]

            else:
                base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    Calculator()
