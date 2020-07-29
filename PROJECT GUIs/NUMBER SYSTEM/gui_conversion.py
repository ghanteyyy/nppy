import os
import sys
import winsound

try:  # Python 3
    from tkinter import *
    from tkinter.ttk import Combobox, Scrollbar

except (ImportError, ModuleNotFoundError):  # Python 2
    from Tkinter import *
    from ttk import Combobox, Scrollbar


class Number_System:
    def __init__(self):
        self.hex_to_num = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
        self.num_to_hex = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

    def is_valid_number_system(self, nums, check, name):
        '''Check if the given number is valid with resect to the number system from converting'''

        check = [True if num in check else False for num in nums]

        if all(check):
            return True

        winsound.MessageBeep()
        gui.display_answer(f'Invalid {name} Number')
        return False

    def binary_to_decimal(self, binary_number):
        '''Convert binary number to decimal number

            1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                    = 123 '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = 0
            len_bin_num = len(binary_number) - 1
            reverse_bin = binary_number[::-1]

            while len_bin_num != -1:
                decimal_num += int(reverse_bin[len_bin_num]) * 2 ** len_bin_num
                len_bin_num -= 1

            return str(decimal_num)

    def binary_to_octal(self, binary_number):
        '''Convert binary number to octal number

           To convert binary to octal you need to:
                1. Convert binary number to decimal number via "self.binary_to_decimal" function
                2. Convert obtained decimal number from step 1 to octal via "decimal_to_octal" function '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = self.binary_to_decimal(binary_number)
            octal_num = self.decimal_to_octal(decimal_num)

            return str(octal_num)

    def binary_to_hexadecimal(self, binary_number):
        '''Convert binary number to hexadecimal number

           To convert binary to hexadecimal you need to:
                1. Convert binary number to decimal number via "self.binary_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to hexadecimal via "decimal_to_hexadecimal" function '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = self.binary_to_decimal(binary_number)
            decimal_to_hexadecimal = self.decimal_to_hexadecimal(decimal_num)

            return str(decimal_to_hexadecimal)

    def binary_to_quinary(self, binary_number):
        '''Convert binary number to quinary number

           To convert binary to quinary you need to:
                1. Convert binary number to decimal number via "self.binary_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to quinary via "decimal_to_quinary" function '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = self.binary_to_decimal(binary_number)
            quinary_num = self.decimal_to_quinary(decimal_num)

            return str(quinary_num)

    def decimal_to_binary(self, decimal_number):
        '''Convert decimal number to binary number

                    2 | 123 | 1   >>> Remainder
                        ------
                   2 | 61  | 1    >>> Remainder
                     ------
                  2 | 30  | 0     >>> Remainder
                    -----
                 2 | 15  | 1     >>> Remainder
                    -----
                2 |  7  | 1      >>> Remainder
                  ------
               2 |  3  | 1       >>> Remainder
                 ------
                   1

            And writing the remainder in reverse way i.e 1111011 '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            binary_num = ''

            while decimal_num != 0:
                remainder = str(decimal_num % 2)
                binary_num += remainder
                decimal_num //= 2

            return str(binary_num[::-1])

    def decimal_to_octal(self, decimal_number):
        '''Convert decimal number to octal number

                8 | 123 | 3     >>> Remainder
                  -----
               8 |  15 | 7      >>> Remainder
                 -----
                   1           >>> Remainder

            And writing the remainder in reverse way i.e 173 '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            octal_num = ''

            while decimal_num != 0:
                remainder = str(decimal_num % 8)
                octal_num += remainder
                decimal_num //= 8

            return str(octal_num[::-1])

    def decimal_to_hexadecimal(self, decimal_number):
        '''Convert decimal number to hexadecimal number

                16| 123 | 11 (B)   >>> Remainder
                  ------
                    7              >>> Remainder

            And writing the remainder in reverse way i.e 7B '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            hexadecimal_num = ''

            while decimal_num != 0:
                remainder = decimal_num % 16

                if remainder >= 10:
                    hexadecimal_num += self.num_to_hex[remainder]

                else:
                    hexadecimal_num += str(remainder)

                decimal_num //= 16

            return str(hexadecimal_num[::-1])

    def decimal_to_quinary(self, decimal_number):
        '''Convert decimal number to quinary number

            To calculate decimal_number to quinary you need to:
                5 | 123 | 3    >>> Remainder
                  ------
               5 | 24  | 4    >>> Remainder
                 ------
                   4         >>> Remainder

            And writing the remainder in reverse way i.e 443 '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            quinary_num = ''

            while decimal_num != 0:
                remainder = str(decimal_num % 5)
                quinary_num += remainder
                decimal_num //= 5

            return str(quinary_num[::-1])

    def octal_to_binary(self, octal_number):
        '''Convert octal number system to binary number system

           To convert octal to binary you need to:
                1. Convert octal number to decimal number via "self.octal_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to binary via "decimal_to_binary" function '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            octal_to_decimal = self.octal_to_decimal(octal_number)
            binary_num = self.decimal_to_binary(octal_to_decimal)

            return binary_num

    def octal_to_decimal(self, octal_number):
        '''Convert octal number to decimal number

            173 = 1 * 8^2 + 7 * 8^1 + 3 * 8^0
                = 123 '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            decimal_num = 0
            len_oct_num = len(octal_number) - 1
            reverse_octal_num = octal_number[::-1]

            while len_oct_num != -1:
                decimal_num += int(reverse_octal_num[len_oct_num]) * 8 ** len_oct_num
                len_oct_num -= 1

            return str(decimal_num)

    def octal_to_hexadecimal(self, octal_number):
        '''Convert octal number to hexadecimal number

           To convert octal to hexadecimal you need to:
                1. Convert octal number to decimal number via "self.octal_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to hexadecimal via "decimal_to_hexadecimal" function '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            decimal_num = self.octal_to_decimal(octal_number)
            hexadecimal_num = self.decimal_to_hexadecimal(decimal_num)

            return str(hexadecimal_num)

    def octal_to_quinary(self, octal_number):
        '''Convert octal number to quinary number

           To convert octal to quinary you need to:
                1. Convert octal number to decimal number via "self.octal_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to quinary via "decimal_to_quinary" function '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            decimal_num = self.octal_to_decimal(octal_number)
            quinary_num = self.decimal_to_quinary(decimal_num)

            return str(quinary_num)

    def hexadecimal_to_binary(self, hexadecimal_number):
        '''Convert hexadecimal number to binary number

           To convert hexadecimal to binary you need to:
                1. Convert hexadecimal number to decimal number via "self.hexadecimal_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to binary via "decimal_to_binary" function '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = self.hexadecimal_to_decimal(hexadecimal_number)
            binary_num = self.decimal_to_binary(decimal_num)

            return str(binary_num)

    def hexadecimal_to_decimal(self, hexadecimal_number):
        '''Convert hexadecimal number to decimal number

            7B = 7 * 16^2 + 11 * 16^0       here B == 11
               = 123 '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = 0
            len_hexadecimal = len(hexadecimal_number) - 1
            reverse_hexadecimal = hexadecimal_number[::-1]

            while len_hexadecimal != -1:
                each_hexa = reverse_hexadecimal[len_hexadecimal]

                if each_hexa in self.hex_to_num:
                    each_hexa = self.hex_to_num[each_hexa]

                decimal_num += int(each_hexa) * 16 ** len_hexadecimal
                len_hexadecimal -= 1

            return str(decimal_num)

    def hexadecimal_to_octal(self, hexadecimal_number):
        '''Convert hexadecimal number to octal number

           To convert hexadecimal to octal you need to:
                1. Convert hexadecimal number to decimal number via "self.hexadecimal_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to octal via "decimal_to_octal" function '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = self.hexadecimal_to_decimal(hexadecimal_number)
            octal_num = self.decimal_to_octal(decimal_num)

            return str(octal_num)

    def hexadecimal_to_quinary(self, hexadecimal_number):
        '''Convert hexadecimal number to quinary number

           To convert hexadecimal to quinary you need to:
                1. Convert hexadecimal number to decimal number via "self.hexadecimal_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to quinary via "decimal_to_quinary" function '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = self.hexadecimal_to_decimal(hexadecimal_number)
            quinary_num = self.decimal_to_quinary(decimal_num)

            return str(quinary_num)

    def quinary_to_binary(self, quinary_number):
        '''Convert quinary number to binary number

           To convert quinary to binary you need to:
                1. Convert quinary number to decimal number via "self.quinary_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to binary via "decimal_to_binary" function '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = self.quinary_to_decimal(quinary_number)
            binary_num = self.decimal_to_binary(decimal_num)

            return str(binary_num)

    def quinary_to_decimal(self, quinary_number):
        '''Convert quinary number to decimal number

            443 = 4 * 5^2 + 4 * 5^1 + 3 * 5^0
                = 123 '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = 0
            len_quinary_num = len(quinary_number) - 1
            reverse_quinary_num = quinary_number[::-1]

            while len_quinary_num != -1:
                decimal_num += int(reverse_quinary_num[len_quinary_num]) * 5 ** len_quinary_num
                len_quinary_num -= 1

            return str(decimal_num)

    def quinary_to_octal(self, quinary_number):
        '''Convert quinary number to octal number

           To convert quinary to octal you need to:
                1. Convert quinary number to decimal number via "self.quinary_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to octal via "decimal_to_octal" function '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = self.quinary_to_decimal(quinary_number)
            octal_num = self.decimal_to_octal(decimal_num)

        return str(octal_num)

    def quinary_to_hexadecimal(self, quinary_number):
        '''Convert quinary number into hexadecimal number

           To convert quinary to hexadecimal you need to:
                1. Convert quinary number to decimal number via "self.quinary_to_decimal" function
                2. Convert obtained decimal number obtained from step 1 to hexadecimal via "decimal_to_hexadecimal" function '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = self.quinary_to_decimal(quinary_number)
            hexadecimal_num = self.decimal_to_hexadecimal(decimal_num)

            return str(hexadecimal_num)


class GUI:
    def __init__(self):
        self.master = Tk()
        self.master.withdraw()
        self.master.after(0, self.master.deiconify)
        self.master.iconbitmap(self.resource_path('included_files/icon.ico'))
        self.master.title('Number System')
        self.pos_x, self.pos_y = self.master.winfo_screenwidth() // 2 - 300 // 2, self.master.winfo_screenheight() // 2 - 300 // 2
        self.master.geometry(f'260x369+{self.pos_x}+{self.pos_y}')
        self.master.resizable(0, 0)

        self.file_image_file = PhotoImage(file='included_files/cover.png')

        self.label_image = Label(self.master, image=self.file_image_file, bg='blue', borderwidth=0)
        self.label_image.place(x=0, y=0)

        self.combo_values = ['Binary to Decimal', 'Binary to Octal', 'Binary to Hexadecimal', 'Binary to Quinary',
                             'Decimal to Binary', 'Decimal to Octal', 'Decimal to Hexadecimal', 'Decimal to Quinary',
                             'Octal to Binary', 'Octal to Decimal', 'Octal to Hexadecimal', 'Octal to Quinary',
                             'Hexadecimal to Binary', 'Hexadecimal to Decimal', 'Hexadecimal to Octal', 'Hexadecimal to Quinary',
                             'Quinary to Binary', 'Quinary to Decimal', 'Quinary to Octal', 'Quinary to Hexadecimal']

        self.entry_var = StringVar()
        self.entry_box = Entry(self.master, width=33, fg='grey', textvariable=self.entry_var, justify='center')
        self.entry_var.set('Enter Number')
        self.entry_box.place(x=30, y=130)

        self.combo_box = Combobox(self.master, values=self.combo_values, width=30)
        self.combo_box.set('Select Number System')
        self.combo_box.place(x=30, y=160)

        self.convert_button = Button(self.master, width=28, height=2, fg='white', bg='Green', activebackground='Green', activeforeground='white', text='CONVERT', command=self.calculation)
        self.convert_button.place(x=30, y=190)

        self.text_area_frame = Frame(self.master)
        self.text_area = Text(self.text_area_frame, width=23, height=5, bg='black', font="-weight bold", bd=0, fg='White', cursor='arrow', state=DISABLED)
        self.text_area.grid(column=0, row=0)
        self.text_area_frame.place(x=30, y=240)

        self.scrollbar = Scrollbar(self.text_area_frame, orient="vertical", command=self.text_area.yview)
        self.show_scrollbar()

        self.master.bind('<Button-1>', self.bind_keys)
        self.master.bind('<Return>', self.calculation)
        self.entry_box.bind('<FocusIn>', self.bind_keys)
        self.entry_box.bind('<Button-1>', self.bind_keys)
        self.entry_box.bind('<FocusOut>', lambda event, focus_out=True: self.bind_keys(event, focus_out))
        self.combo_box.bind('<FocusOut>', lambda event, focus_out=True: self.bind_keys(event, focus_out))

        self.master.mainloop()

    def bind_keys(self, event, focus_out=False):
        '''Commands when user clicks in and out of the entry widget'''

        entry_get = self.entry_var.get().strip()
        combo_get = self.combo_box.get().strip()

        if event.widget == self.entry_box and entry_get == 'Enter Number' and not focus_out:
            self.entry_var.set('')
            self.entry_box.config(fg='black')

            if not combo_get:
                self.combo_box.set('Select Number System')

        elif event.widget == self.combo_box and not entry_get and not focus_out:
            self.entry_var.set('Enter Number')
            self.entry_box.config(fg='grey')

        else:
            if not entry_get:
                self.entry_var.set('Enter Number')
                self.entry_box.config(fg='grey')

            if combo_get in ['', 'Select Number System']:
                self.combo_box.set('Select Number System')

        if event.widget not in [self.entry_box, self.combo_box, self.convert_button]:
            self.master.focus()

    def remove_error(self):
        '''Remove error message after three seconds'''

        self.text_area.delete('1.0', 'end')
        self.text_area.config(state=DISABLED)

    def add_newline(self, result):
        '''Add new line character at the end of the line'''

        li = []
        result = str(result)

        for _ in range((len(result) // 20) + 1):
            li.append(result[:20] + '\n')
            result = result[20:]

            if len(result) < 20:
                li.append(result)
                result = ''

        return ''.join(li).strip()

    def show_scrollbar(self):
        '''Show scrollbar when the character in the text is more than the height of the text widget'''

        if self.text_area.cget('height') < int(self.text_area.index('end-1c').split('.')[0]):
            self.scrollbar.grid(column=1, row=0, sticky=N + S)
            self.text_area.config(yscrollcommand=self.scrollbar.set)
            self.master.after(100, self.hide_scrollbar)

        else:
            self.master.after(100, self.show_scrollbar)

    def hide_scrollbar(self):
        '''Hide scrollbar when the character in the text is less than the height of the text widget'''

        if self.text_area.cget('height') >= int(self.text_area.index('end-1c').split('.')[0]):
            self.scrollbar.grid_forget()
            self.text_area.config(yscrollcommand=None)
            self.master.after(100, self.show_scrollbar)

        else:
            self.master.after(100, self.hide_scrollbar)

    def display_answer(self, result):
        '''Display answer or errors'''

        if len(str(result)) > 20:
            result = self.add_newline(result)

        else:
            result = str(result)

        self.text_area.config(state=NORMAL)
        self.text_area.delete('1.0', 'end')
        self.text_area.tag_configure("center", justify='center')
        self.text_area.insert("1.0", result)
        self.text_area.tag_add("center", "1.0", "end")

        if 'Invalid' in result or 'Input' in result:
            self.master.after(3000, self.remove_error)

        else:
            self.text_area.config(state=DISABLED)

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

    def calculation(self, event=None):
        '''Converting number with respective selected conversion'''

        get_value = self.entry_var.get().strip()

        if get_value == 'Enter Number' or not get_value:
            winsound.MessageBeep()
            answer = 'Input Valid Number'

        elif self.combo_box.get() == 'Select Number System':
            winsound.MessageBeep()
            answer = 'Select Valid Conversion'

        else:
            combo_get = self.combo_box.get()
            number_system = Number_System()

            if combo_get == 'Binary to Decimal':
                answer = number_system.binary_to_decimal(get_value)

            elif combo_get == 'Binary to Octal':
                answer = number_system.binary_to_octal(get_value)

            elif combo_get == 'Binary to Hexadecimal':
                answer = number_system.binary_to_hexadecimal(get_value)

            elif combo_get == 'Binary to Quinary':
                answer = number_system.binary_to_quinary(get_value)

            elif combo_get == 'Decimal to Binary':
                answer = number_system.decimal_to_binary(get_value)

            elif combo_get == 'Decimal to Octal':
                answer = number_system.decimal_to_octal(get_value)

            elif combo_get == 'Decimal to Hexadecimal':
                answer = number_system.decimal_to_hexadecimal(get_value)

            elif combo_get == 'Decimal to Quinary':
                answer = number_system.decimal_to_quinary(get_value)

            elif combo_get == 'Octal to Binary':
                answer = number_system.octal_to_binary(get_value)

            elif combo_get == 'Octal to Decimal':
                answer = number_system.octal_to_decimal(get_value)

            elif combo_get == 'Octal to Hexadecimal':
                answer = number_system.octal_to_hexadecimal(get_value)

            elif combo_get == 'Octal to Quinary':
                answer = number_system.octal_to_quinary(get_value)

            elif combo_get == 'Hexadecimal to Binary':
                answer = number_system.hexadecimal_to_binary(get_value)

            elif combo_get == 'Hexadecimal to Decimal':
                answer = number_system.hexadecimal_to_decimal(get_value)

            elif combo_get == 'Hexadecimal to Octal':
                answer = number_system.hexadecimal_to_octal(get_value)

            elif combo_get == 'Hexadecimal to Quinary':
                answer = number_system.hexadecimal_to_quinary(get_value)

            elif combo_get == 'Quinary to Binary':
                answer = number_system.quinary_to_binary(get_value)

            elif combo_get == 'Quinary to Decimal':
                answer = number_system.quinary_to_decimal(get_value)

            elif combo_get == 'Quinary to Octal':
                answer = number_system.quinary_to_octal(get_value)

            elif combo_get == 'Quinary to Hexadecimal':
                answer = number_system.quinary_to_hexadecimal(get_value)

        if answer:
            self.display_answer(answer)


if __name__ == '__main__':
    gui = GUI()
