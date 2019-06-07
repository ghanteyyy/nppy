import PIL.Image  # Install if not installed
import PIL.ImageTk  # Install if not installed
from winsound import MessageBeep

try:
    from tkinter import *
    from tkinter.ttk import Combobox, Scrollbar

except (ImportError, ModuleNotFoundError):
    from Tkinter import *
    from ttk import Combobox, Scrollbar


hex_to_num = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}
num_to_hex = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}


def remove_error():
    text_area.delete('1.0', 'end')
    text_area.config(state=DISABLED)


def is_binary(binary_number):
    '''Check if the given number is binary'''

    try:
        count = 0

        for binn in str(binary_number):
            if not binn.isdigit() or int(binn) > 1:
                count += 1

        if count == 0:
            return True

        else:
            return False

    except ValueError:
        MessageBeep()
        display_answer('Invalid Binary Number')


def is_octal(octal_number):
    '''Check if the given number is octal'''

    try:
        count = 0

        for oct_num in str(octal_number):
            if not oct_num.isdigit() or int(oct_num) > 7:
                count += 1

        if count == 0:
            return True

        else:
            return False

    except ValueError:
        MessageBeep()
        display_answer('Invalid Octal Number')


def is_hexadecimal(hexadecimal_number):
    '''Check if the given number is hexadecimal'''

    count = 0

    if hexadecimal_number.isalpha() or hexadecimal_number.isalnum():
        for hexa_decimal in hexadecimal_number:
            if hexa_decimal.isalpha() and hexa_decimal.upper() not in list('ABCDEF'):
                count += 1

    if count == 0:
        return True

    else:
        return False


def is_quinary(quinary_number):
    '''Check if the given number is quinary'''

    try:
        count = 0

        for quinary in str(quinary_number):
            if int(quinary) >= 5:
                count += 1

        if count == 0:
            return True

        else:
            return False

    except ValueError:
        MessageBeep()
        display_answer('Invalid Quinary Number')


def binary_to_decimal(binary_number):
    '''Convert binary number to decimal number

        To convert binary to decimal you need to:
            Multipy each number by base 2 with its own power increase from left to right(first power is 0)
                1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                       = 123

            Required decimal number is 123
    '''

    global decimal_number

    decimal_number = 0

    if is_binary(binary_number):
        reversed_binary = str(binary_number)[::-1]

        # Converting to decimal
        for bin_num in range(len(binary_number)):
            decimal_number += int(reversed_binary[bin_num]) * 2 ** bin_num

        return decimal_number

    else:
        MessageBeep()
        display_answer('Invalid Binary Number')


def binary_to_octal(binary_number):
    '''Convert binary number to octal number

        Binary number = 1111011

        To convert it to octal number:
            Step 1: Split each three value from backward like
                    1           111            011

            Step 2: Here, we have all splited value having length 3 except one i.e 1 so adding extra two '0's in the front of 1
                    001 to make its length 3

                    Then finally we have,
                        001               111               011

            Step 3: Now using 4,2,1 rule so,
                        first,
                            001 = 0 * 4 + 0 * 2 + 1 * 1
                                = 1
                        second,
                            111 = 1 * 4 + 1 * 2 + 1 * 1
                                = 7
                        third,
                            011 = 0 * 4 + 1 * 2 + 1 * 1
                                = 3

            Step 4: Append each value from first, second, and third which becomes to 173

            Required octal number is 173
    '''

    global octal_number

    if is_binary(binary_number):
        binary_number = str(binary_number)[::-1]

        test_octal = 0
        rule = [4, 2, 1]

        listed_value = []
        octal_number = ''

        for i in range(len(binary_number) // 3 + 1):
            '''
                Here, len(binary_number) = 8
                    Then, len(binary_number) // 3 + 1 = 2 + 1 = 3
                    So, xrange = (0, 1, 2)
            '''

            sliced_binary = binary_number[:3]  # Storing three value from binary_number in each itreation
            binary_number = binary_number[3:]  # Overwriting binary_number variable excluding value stored in sliced_binary using slicing

            if len(sliced_binary) == 3:  # Checking if the length of value stored in sliced_binary variable
                listed_value.append(sliced_binary[::-1])  # Then, appending listed_value list by reversing value stored in sliced_binary

            else:
                listed_value.append(sliced_binary[::-1].zfill(3))
                '''If length of sliced_binary is less than 3 then:
                    First, reversing value of sliced_binary
                    Second, filling 0 to make three character value

                For instance,
                    At last we get, 01 whose length is less than 3
                        then we reverse it so we get 10
                        and we fill that value '10' with '0' using zfill(3) '010' so that the length becomes 3
                '''

        listed_value = listed_value[::-1]  # Reversing the value of listed_value "list"

        for l in listed_value:  # looping to each value in listed_value list
            for x in range(len(l)):  # Then we get range value (0,1,2) which is stored in temporary variable 'x' in each iteration. Here, xrange is generator (python 2.7)
                test_octal += int(l[x]) * rule[x]  # Here, first slicing value from 'l' and rule with the value 'x' and converting value got from l by slicing into integer

            octal_number += str(test_octal)  # Converting integer value stored in test_octal to string and appending it to octal_number variable
            test_octal = 0  # Overwriting test_octal variable to '0' again

        octal_number = octal_number.lstrip('0')

    else:
        MessageBeep()
        display_answer('Invalid binary number')


def binary_to_hexadecimal(binary_number):
    '''Convert binary number to hexadecimal number

        Binary number = 1111011

        To convert it to hexadecimal number:
            Step 1: Split each four value from backward like
                    111                         1011

            Step 2: Here, in first part the length is less than 4 so adding extra 0 at its front and 111 becomes 0111

            Step 3: Now using 8,4,2,1 rule in each splitted value so,
                        first,
                            0111 = 0 * 8 + 1 * 4 + 1 * 2 + 1 * 1
                                 = 7

                        second,
                            1011 = 1 * 8 + 0 * 4 + 1 * 2 + 1 * 1
                                 = 11 (B)

                                In Hexadecimal,
                                    10 = A
                                    11 = B
                                    12 = C
                                    13 = D
                                    14 = E
                                    15 = F


            Step 4: Append each value from first, second, and third which becomes to 7B

                Required hexadecimal number is 7B
    '''

    global hexadecimal_number

    if is_binary(binary_number):
        binary_number = str(binary_number)[::-1]
        hexa_decimal_value = {'10': 'A',
                              '11': 'B',
                              '12': 'C',
                              '13': 'D',
                              '14': 'E',
                              '15': 'F'}
        get_remainder = 0
        rule = [8, 4, 2, 1]

        listed_value = []
        hexadecimal_number = ''

        for i in range(len(binary_number) // 4 + 1):
            '''
                Here, len(binary_number) = 8
                    Then, len(binary_number) // 4 + 1 = 2 + 1 = 4
                    So, xrange = (0, 1, 2, 3)
            '''

            sliced_binary = binary_number[:4]  # Storing three value from binary_number in each itreation
            binary_number = binary_number[4:]  # Overwriting binary_number variable excluding value stored in sliced_binary using slicing

            if len(sliced_binary) == 4:  # Checking if the length of value stored in sliced_binary variable
                listed_value.append(sliced_binary[::-1])  # Then, appending listed_value list by reversing value stored in sliced_binary

            else:
                listed_value.append(sliced_binary[::-1].zfill(4))
                '''If length of sliced_binary is less than 4 then:
                    First, reversing value of sliced_binary
                    Second, filling 0 to make three character value

                For instance,
                    At last we get, 01 whose length is less than 4
                        then we reverse it so we get 10
                        and we fill that value '10' with '0' using zfill(3) '010' so that the length becomes 4
                '''

        listed_value = listed_value[::-1]  # Reversing the value of listed_value "list"

        for l in listed_value:  # looping to each value in listed_value list
            for x in range(len(l)):  # Then we get range value (0,1,2, 3) which is stored in temporary variable 'x' in each iteration. Here, xrange is generator (python 2.7)
                get_remainder += int(l[x]) * rule[x]  # Here, first slicing value from 'l' and rule with the value 'x' and converting value got from 'l' by slicing into integer

            if get_remainder > 9:
                get_remainder = hexa_decimal_value[str(get_remainder)]

            hexadecimal_number += str(get_remainder)  # Converting integer value stored in get_remainder to string and appending it to hexadecimal_number variable
            get_remainder = 0  # Overwriting get_remainder variable to '0' again

        hexadecimal_number = hexadecimal_number.lstrip('0')

    else:
        MessageBeep()
        display_answer('Invalid binary number')


def binary_to_quinary(binary_number):
    '''Convert binary number to quinary number

        To convert quinary to binary we need to:
            Step 1: Convert given binary to decimal

                For instance, lets take binary_number as 1111011 then,
                    Converting 1111011 to decimal, we get:
                        1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                                = 123 (decimal number)

            Step 2: Convert the obtained decimal number to quinary number

                        =  5 | 123 | 3  >>> Remainder
                             ------
                          5 |  24 | 4  >>> Remainder
                            ------
                              4

                    Required quinary number is 443 taken in reverse ways

    '''

    global quinary_number

    if is_binary(binary_number):
        quinary_number = ''
        decimal_number = 0
        reversed_binary = str(binary_number)[::-1]

        # Converting binary to decimal
        decimal_number = binary_to_decimal(reversed_binary)

        # Converting obtained decimal to quinary
        while decimal_number > 0:
            quinary_number += str(decimal_number % 5)
            decimal_number = decimal_number // 5

        quinary_number = quinary_number[::-1]

    else:
        MessageBeep()
        display_answer('Inalid quinary number')


def decimal_to_binary(decimal_number):
    '''Convert decimal number to binary number

        To convert decimal to binary you need to divide the decimal number by 2 and write the remainder in reverse way
            For an instance, lets take decimal number as 33, then the calculation is as follow:
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

                Required binary number is 1111011 (writing in reverse)
    '''

    global binary_number

    try:
        binary_number = ''
        decimal_number = int(decimal_number)

        # Converting into binary number
        while decimal_number > 0:
            binary_number += str(decimal_number % 2)
            decimal_number = decimal_number // 2

        binary_number = binary_number[::-1]
        return binary_number

    except ValueError:
        MessageBeep()
        display_answer('Invalid Decimal Number')


def decimal_to_octal(decimal_number):
    '''Convert decimal number to octal number

        To convert decimal to octal you need to divide decimal number by 0:
            For an instance, lets take decimal number as 98
                            8 | 123 | 3     >>> Remainder
                              -----
                           8 |  15 | 7      >>> Remainder
                             -----
                               1           >>> Remainder

            And writing the remainder in reverse way i.e 173
    '''

    try:
        global octal_number

        octal_number = ''
        decimal_number = int(decimal_number)

        # Converting into octal
        while decimal_number > 0:
            octal_number += str(decimal_number % 8)
            decimal_number = decimal_number // 8

        octal_number = octal_number[::-1]
        return octal_number

    except ValueError:
        MessageBeep()
        display_answer('Invalid Decimal Number')


def decimal_to_hexadecimal(decimal_number):
    '''Convert decimal number to hexadecimal number

            To convert decimal number to hexadecimal, you need to:
                    For instance, lets take decimal number as 123

                    Divide decimal number until remainder becomes 0
                                            16| 123 | 11 (B)  >>> Remainder
                                              ------
                                                7   >>> Remainder

                    Required hexadecimal number is 7B
    '''

    try:
        global hexadecimal_number

        hexadecimal_number = ''
        decimal_number = int(decimal_number)

        # Converting intto hexadecimal number
        while decimal_number > 0:
            get_remainder = decimal_number % 16

            if get_remainder > 9:
                hexadecimal_number += num_to_hex[str(get_remainder)]

            else:
                hexadecimal_number += str(get_remainder)

            decimal_number = decimal_number // 16

        hexadecimal_number = hexadecimal_number[::-1]
        return hexadecimal_number

    except ValueError:
        MessageBeep()
        display_answer('Invalid Decimal Number')


def decimal_to_quinary(decimal_number):
    '''Convert decimal number to quinary number

        For an instance, lets take decimal_number as 123 then,

        To calculate decimal_number to quinary you need to:
                        5 | 123 | 3    >>> Remainder
                          ------
                       5 | 24  | 4    >>> Remainder
                         ------
                           4         >>> Remainder

        Required quinary number is 443
    '''

    try:
        global quinary_number

        quinary_number = ''
        decimal_number = int(decimal_number)

        # Converting into quinary
        while decimal_number > 0:
            quinary_number += str(decimal_number % 5)
            decimal_number = decimal_number // 5

        quinary_number = quinary_number[::-1]
        return quinary_number

    except ValueError:
        MessageBeep()
        display_answer('Invalid Decimal Number')


def octal_to_binary(octal_number):
    '''
        For an instance, lets take an octal number 123

            To calculate you need to:
                Step 1: Convert the given octal number to decimal.
                            123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                                 = 83

                Step 2: Convert the obtained decimal to binary
                                    2 | 83 | 1  <<< Remainder
                                      -------
                                   2 | 41 | 1  <<< Remainder
                                     -------
                                  2 | 20 | 0  <<< Remainder
                                    -------
                                 2 | 10 | 0  <<< Remainder
                                   -------
                                2 |  5 | 1  <<< Remainder
                                  -------
                               2 |  2 | 0  <<< Remainder
                                 -------
                                   1

                        And our required binary is 1010011
    '''

    global binary_number

    if is_octal(octal_number):
        binary_number = ''
        decimal_number = octal_to_decimal(octal_number)

        # Converting into obtained decimal to binary
        while decimal_number > 0:
            binary_number += str(decimal_number % 2)
            decimal_number = decimal_number // 2

        binary_number = binary_number[::-1]

    else:
        MessageBeep()
        display_answer('Invalid Octal Number')


def octal_to_decimal(octal_number):
    '''Convert octal number to decimal number

        To convert octal to decimal you need to:
            Multipy each number by base 8 with its own power increase from left to right(first power is 0)
                123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                    =  83
    '''

    global decimal_number

    if is_octal(octal_number):
        decimal_number = 0
        reversed_octal = str(octal_number)[::-1]

        for x in range(len(reversed_octal)):
            decimal_number += int(reversed_octal[x]) * 8 ** x

        return decimal_number

    else:
        MessageBeep()
        display_answer('Invalid Octal Number')


def octal_to_hexadecimal(octal_number):
    '''Convert octal number to hexadecimal number

        To convert octal number to hexadecimal you need to first convert the octal number to decimal and obtained decimal to hexadecimal
            For an instance, lets take an octal number 123
                Step 1: Convert octal number(123) to decimal
                        123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                            = 83 (decimal number)

                Step 2: Then, convert obtained decimal number to octal
                                16 | 83 | 3   >>> Remainder
                                   ------
                                     5    >>> Remainder

                        And our required hexadecimal is 53 (taking remainder in reverse(i.e from down to up))
    '''

    global hexadecimal

    if is_octal(octal_number):
        decimal_number = 0
        hexadecimal = ''

        decimal_number = octal_to_decimal(octal_number)

        # Converting to hexadecimal
        while decimal_number > 0:
            get_remainder = str(decimal_number % 16)

            if int(get_remainder) > 9:
                hexadecimal += num_to_hex[get_remainder]

            else:
                hexadecimal += get_remainder

            decimal_number = decimal_number // 16

        hexadecimal = hexadecimal[::-1]

    else:
        MessageBeep()
        display_answer('Invalid Octal Number')


def octal_to_quinary(octal_number):
    '''Convert octal number to quinary number

        You can covert octal_number to binary by converting the given octal_number to decimal and then obtained decimal to quinary
            For an instance, lets take an octal number to be 123

                Step 1: Covert octal number to decimal number
                        123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                            = 83 (decimal number)

                Step 2: Convert the obtained decimal number to quinary number
                            5 | 83 | 3
                              -----
                           5 | 16 | 1
                             -----
                               3

                REQUIRED QUINARY NUMBER is 313 (taking remainder in reverse order)
    '''

    global quinary_number

    quinary_number = ''

    if is_octal(octal_number):
        # Converting to decimal
        decimal_number = octal_to_decimal(octal_number)

        # Converting obtained decimal to quinary
        while decimal_number > 0:
            quinary_number += str(decimal_number % 5)
            decimal_number = decimal_number // 5

        quinary_number = quinary_number[::-1]

    else:
        MessageBeep()
        display_answer('Invalid Octal Number')


def hexadecimal_to_binary(hexadecimal_number):
    '''Convert hexadecimal number to binary number

        To convert hexadecimal to binary, you need to first convert hexadecimal to decimal and obtained decimal to binary

            Step 1: Convert hexadecimal to decimal
                    123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                        = 291 (decimal number)

            Step 2: Convert the obtained decimal to binary
                                2 | 291 | 1
                                  ------
                               2 | 145 | 1
                                 ------
                              2 |  72 | 0
                                ------
                             2 |  36 | 0
                               ------
                            2 |  18 | 0
                              ------
                           2 |  9  | 1
                             ------
                          2 |   4 | 0
                            ------
                         2 |   2 | 0
                           ------
                             1

                        Required binary number is 100100011 (taking remainder in reverse order)
    '''

    global binary_number

    decimal_number = 0

    if is_hexadecimal(hexadecimal_number):
        if hexadecimal_number.isalpha() or not hexadecimal_number.isdigit():
            split_hexadecimal = list(str(hexadecimal_number))

            for index, split_hexa_decimal in enumerate(split_hexadecimal):
                if split_hexa_decimal.upper() in hex_to_num:
                    split_hexadecimal[index] = hex_to_num[split_hexa_decimal.upper()]

            reverse_split_hexadecimal = split_hexadecimal[::-1]

            for index, value in enumerate(reverse_split_hexadecimal):
                decimal_number += int(reverse_split_hexadecimal[index]) * 16 ** index

            binary_number = decimal_to_binary(decimal_number)

        else:
            reversed_hexadecimal = hexadecimal_number[::-1]

            # Converting to decimal
            for x in range(len(reversed_hexadecimal)):
                decimal_number += int(reversed_hexadecimal[x]) * 16 ** x

        binary_number = decimal_to_binary(decimal_number)

    else:
        MessageBeep()
        display_answer('Invalid Hexadecimal Number')


def hexadecimal_to_decimal(hexadecimal_number):
    '''Convert hexadecimal number to decimal number

        To convert hexadecimal to decimal you need to:
            Multipy each number by base 16 with its own power increase from left to right(first power is 0)
                123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                    = 291
    '''

    global decimal_number

    decimal_number = 0

    if is_hexadecimal(hexadecimal_number):
        if hexadecimal_number.isalpha() or not hexadecimal_number.isdigit():
            split_hexadecimal = list(str(hexadecimal_number))

            for index, split_hexa_decimal in enumerate(split_hexadecimal):
                if split_hexa_decimal.upper() in hex_to_num:
                    split_hexadecimal[index] = hex_to_num[split_hexa_decimal.upper()]

            reverse_split_hexadecimal = split_hexadecimal[::-1]

            for index, value in enumerate(reverse_split_hexadecimal):
                decimal_number += int(value) * 16 ** index

        else:
            reversed_hexadecimal = hexadecimal_number[::-1]

            # Converting to decimal
            for index, value in enumerate(reversed_hexadecimal):
                decimal_number += int(value) * 16 ** index

        return decimal_number

    else:
        MessageBeep()
        display_answer('Invalid Hexadecimal Number')


def hexadecimal_to_octal(hexadecimal_number):
    '''Convert hexadecimal number to octal number

        To calculate hexadecimal to octal you need to first convert hexadecimal to decimal and obtained decimal to octal
            For an instance, lets take hexadecimal number as 123
                Step 1: Converting to decimal number
                        123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                            = 291 (decimal number)

                Step 2: Convert obtained decimal number to octal number
                                8 | 291 | 3
                                  ------
                               8 |  36 | 4
                                 ------
                                    4

                    And our required octal number is 443 (taken in reverse order)
    '''

    global octal_number

    decimal_number = hexadecimal_to_decimal(hexadecimal_number)
    octal_number = decimal_to_octal(decimal_number)


def hexadecimal_to_quinary(hexadecimal_number):
    '''Convert hexadecimal number to quinary number

        To convert hexadecimal to quinary you need to first convert hexadecimal number to decimal and obtained decimal to quinary
            For an instance, lets take hexadecimal number as 123
                Step 1: Convert the hexadecimal number to decimal
                            123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                                = 291 (decimal number)

                Step 2: Now, convert obtained decimal to quinary
                                5 | 291 | 1
                                  ------
                               5 |  58 | 3
                                 ------
                              5 |  11 | 1
                                ------
                                  2

                    And our required quinary number is 2131 (taken in reverse order)
    '''

    global quinary_number

    decimal_number = hexadecimal_to_decimal(hexadecimal_number)
    quinary_number = decimal_to_quinary(decimal_number)


def quinary_to_binary(quinary_number):
    '''Convert quinary number to binary number

        You can convert quinary number to binary, first by converting quinary number to decimal and obtained decimal to binary number
            For an instance, lets take quinary number be 123

                Step 1: Convert quinary number to decimal
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38 (Decimal)

                Step 2: Convert obtained decimal number to binary
                              2 | 38 | 0
                                -----
                             2 | 19 | 1
                               -----
                            2 |  9 | 1
                              -----
                           2 |  4 | 0
                             -----
                          2 |  2 | 0
                            -----
                              1


                        And our required binary number is 100110 (taken remainder in reverse way)
    '''

    global binary_number

    if is_quinary(quinary_number):
        decimal_number = 0
        reversed_quinary = str(quinary_number)[::-1]

        for index, value in enumerate(reversed_quinary):
            decimal_number += int(value) * 5 ** index

        binary_number = decimal_to_binary(decimal_number)

    else:
        MessageBeep()
        display_answer('Invalid Quinary Number')


def quinary_to_decimal(quinary_number):
    '''Convert quinary number to decimal number

        You can convert quinary number to decimal by multiplying each quinary number with base of 5 with power starting from 0 increasing from left to right.
            For an instance, lets take quinary number be 123

                Step 1: Converting to decimal number
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38

                    And our required quinary number is 38
    '''

    global decimal_number

    if is_quinary(quinary_number):
        decimal_number = 0
        reversed_binary = str(quinary_number)[::-1]

        for index, value in enumerate(reversed_binary):
            decimal_number += int(value) * 5 ** index

        return decimal_number

    else:
        MessageBeep()
        display_answer('Invalid Quinary Number')


def quinary_to_octal(quinary_number):
    '''Convert quinary number to octal number

        You can convert quinary number to octal, first by converting quinary number to decimal and obtained decimal number to quinary number
            For an instance, lets take binary number be 123

                Step 1: Convert to deicmal
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38 (Decimal)

                Step 2: Convert to octal from the obtained decimal
                                    8 | 38 | 6
                                      -----
                                        4

                            And our required octal number is 46 (taken in a reverse way)
    '''
    global octal_number

    decimal_number = quinary_to_decimal(quinary_number)
    octal_number = decimal_to_octal(decimal_number)


def quinary_to_hexadecimal(quinary_number):
    '''Convert quinary number into hexadecimal number

        You can convert quinary number, first by converting quinary number to decimal and then obtained decimal to hexadecimal number
            For an instance, lets take quinary number to be 123

            Step 1: Convert to quinary number to decimal
                    123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                        = 38 (Decimal)

            Step 2: Convert obtained decimal number to hexadecimal
                            16 | 38 | 6
                               -----
                                 2


                        And our required hexadecimal number is 26
    '''

    global hexadecimal_number

    decimal_number = quinary_to_decimal(quinary_number)
    hexadecimal_number = decimal_to_hexadecimal(decimal_number)


def add_newline(result):
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


def show_scrollbar():
    '''Show scrollbar when the character in the text is more than the height of the text widget'''

    if text_area.cget('height') < int(text_area.index('end-1c').split('.')[0]):
        scrollbar.grid(column=1, row=0, sticky=N + S)
        text_area.config(yscrollcommand=scrollbar.set)
        root.after(100, hide_scrollbar)

    else:
        root.after(100, show_scrollbar)


def hide_scrollbar():
    '''Hide scrollbar when the character in the text is less than the height of the text widget'''

    if text_area.cget('height') >= int(text_area.index('end-1c').split('.')[0]):
        scrollbar.grid_forget()
        text_area.config(yscrollcommand=None)
        root.after(100, show_scrollbar)

    else:
        root.after(100, hide_scrollbar)


def entry_enter(event=None):
    '''when cursor is inside the entry box'''

    entry.focus_set()

    if entry.get() == 'Enter Number':
        entry.delete(0, END)


def entry_leave(event=None):
    '''when cursor is outside the entry box'''

    if len(entry.get()) == 0:
        entry.delete(0, END)
        entry.insert(0, 'Enter Number')

    text_area.focus_set()


def display_answer(result):
    '''Display answer or errors'''

    if len(str(result)) > 20:
        result = add_newline(result)

    else:
        result = str(result)

    text_area.config(state=NORMAL)
    text_area.delete('1.0', 'end')
    text_area.tag_configure("center", justify='center')
    text_area.insert("1.0", result)
    text_area.tag_add("center", "1.0", "end")

    if 'Invalid' in result or 'Input' in result:
        root.after(3000, remove_error)

    else:
        text_area.config(state=DISABLED)


def calculation(event=None):
    '''Calculate number with respective selected conversion'''

    if entry.get() == 'Enter Number' or len(entry.get()) == 0:
        MessageBeep()
        display_answer('Input Valid Number')

    elif combo_box.get() == 'Select Number System':
        MessageBeep()
        display_answer('Select Valid Conversion')

    elif len(entry.get()) != 0:
        get_value = entry.get()

        if combo_box.get() == 'Binary to Decimal':
            binary_to_decimal(get_value)
            if is_binary(get_value) and len(str(decimal_number)) != 0:
                display_answer(decimal_number)

        elif combo_box.get() == 'Binary to Octal':
            binary_to_octal(get_value)
            if is_binary(get_value) and len(octal_number) != 0:
                display_answer(octal_number)

        elif combo_box.get() == 'Binary to Hexadecimal':
            binary_to_hexadecimal(get_value)
            if is_binary(get_value) and len(hexadecimal_number) != 0:
                display_answer(hexadecimal_number)

        elif combo_box.get() == 'Binary to Quinary':
            binary_to_quinary(get_value)
            if is_binary(get_value) and len(quinary_number) != 0:
                display_answer(quinary_number)

        elif combo_box.get() == 'Decimal to Binary':
            decimal_to_binary(get_value)
            if len(binary_number) != 0:
                display_answer(binary_number)

        elif combo_box.get() == 'Decimal to Octal':
            decimal_to_octal(get_value)
            if len(octal_number) != 0:
                display_answer(octal_number)

        elif combo_box.get() == 'Decimal to Hexadecimal':
            decimal_to_hexadecimal(get_value)
            if len(hexadecimal_number) != 0:
                display_answer(hexadecimal_number)

        elif combo_box.get() == 'Decimal to Quinary':
            decimal_to_quinary(get_value)
            if len(quinary_number) != 0:
                display_answer(quinary_number)

        elif combo_box.get() == 'Octal to Binary':
            octal_to_binary(get_value)
            if is_octal(get_value) and len(binary_number) != 0:
                display_answer(binary_number)

        elif combo_box.get() == 'Octal to Decimal':
            octal_to_binary(get_value)
            if is_octal(get_value) and len(str(decimal_number)) != 0:
                display_answer(decimal_number)

        elif combo_box.get() == 'Octal to Hexadecimal':
            octal_to_hexadecimal(get_value)
            if is_octal(get_value) and len(str(hexadecimal)) != 0:
                display_answer(hexadecimal)

        elif combo_box.get() == 'Octal to Quinary':
            octal_to_quinary(get_value)
            if is_octal(get_value) and len(str(quinary_number)) != 0:
                display_answer(quinary_number)

        elif combo_box.get() == 'Hexadecimal to Binary':
            hexadecimal_to_binary(get_value)
            if is_hexadecimal(get_value) and len(str(binary_number)) != 0:
                display_answer(binary_number)

        elif combo_box.get() == 'Hexadecimal to Decimal':
            hexadecimal_to_decimal(get_value)
            if is_hexadecimal(get_value) and len(str(decimal_number)) != 0:
                display_answer(decimal_number)

        elif combo_box.get() == 'Hexadecimal to Octal':
            hexadecimal_to_octal(get_value)
            if is_hexadecimal(get_value) and len(str(octal_number)) != 0:
                display_answer(octal_number)

        elif combo_box.get() == 'Hexadecimal to Quinary':
            hexadecimal_to_quinary(get_value)
            if is_hexadecimal(get_value) and len(str(quinary_number)) != 0:
                display_answer(quinary_number)

        elif combo_box.get() == 'Quinary to Binary':
            quinary_to_binary(get_value)
            if is_quinary(get_value) and len(str(binary_number)) != 0:
                display_answer(binary_number)

        elif combo_box.get() == 'Quinary to Decimal':
            quinary_to_decimal(get_value)
            if is_quinary(get_value) and len(str(decimal_number)) != 0:
                display_answer(decimal_number)

        elif combo_box.get() == 'Quinary to Octal':
            quinary_to_octal(get_value)
            if is_quinary(get_value) and len(str(octal_number)) != 0:
                display_answer(octal_number)

        elif combo_box.get() == 'Quinary to Hexadecimal':
            quinary_to_hexadecimal(get_value)
            if is_quinary(get_value) and len(str(hexadecimal_number)) != 0:
                display_answer(hexadecimal_number)


def main():
    '''Main window of the program'''

    global root, entry, combo_box, text_area, scrollbar

    root = Tk()
    root.withdraw()
    root.after(0, root.deiconify)
    root.iconbitmap('icon.ico')
    root.title('Number System')
    pos_x, pos_y = root.winfo_screenwidth() // 2 - 300 // 2, root.winfo_screenheight() // 2 - 300 // 2
    root.geometry(f'260x369+{pos_x}+{pos_y}')
    root.resizable(0, 0)

    label_image_frame = Frame(root, bd=0, width=237, height=280)
    file_image_file = PIL.ImageTk.PhotoImage(PIL.Image.open('temp.jpg'))
    label_image = Label(label_image_frame, image=file_image_file, bg='blue', borderwidth=0)
    label_image.grid(row=0, column=0)
    label_image_frame.place(x=0, y=0)

    combo_values = ['Binary to Decimal', 'Binary to Octal', 'Binary to Hexadecimal', 'Binary to Quinary',
                    'Decimal to Binary', 'Decimal to Octal', 'Decimal to Hexadecimal', 'Decimal to Quinary',
                    'Octal to Binary', 'Octal to Decimal', 'Octal to Hexadecimal', 'Octal to Quinary',
                    'Hexadecimal to Binary', 'Hexadecimal to Decimal', 'Hexadecimal to Octal', 'Hexadecimal to Quinary',
                    'Quinary to Binary', 'Quinary to Decimal', 'Quinary to Octal', 'Quinary to Hexadecimal']

    entry_field = Frame(root)
    entry = Entry(entry_field, width=33, highlightcolor='grey', highlightthickness=1)
    entry.insert(0, 'Enter Number')
    entry.grid(row=0, column=0)
    entry_field.place(x=30, y=130)

    combo_frame = Frame(root)
    combo_box = Combobox(combo_frame, values=combo_values, width=30)
    combo_box.set('Select Number System')
    combo_box.grid(row=0, column=0)
    combo_frame.place(x=30, y=160)

    convert_frame = Frame(root)
    convert_button = Button(convert_frame, width=28, height=2, bg='Green', activebackground='Green', text='CONVERT', command=calculation)
    convert_button.pack()
    convert_frame.place(x=30, y=190)

    # Binding Keys
    entry.bind('<Return>', calculation)
    combo_box.bind('<Return>', calculation)
    convert_button.bind('<Return>', calculation)
    entry.bind('<Enter>', entry_enter)
    entry.bind('<Leave>', entry_leave)

    text_area_frame = Frame(root)
    text_area = Text(text_area_frame, width=23, height=5, bg='black', font="-weight bold", bd=0, fg='White', cursor='arrow')
    text_area.grid(column=0, row=0)
    text_area_frame.place(x=30, y=240)

    scrollbar = Scrollbar(text_area_frame, orient="vertical", command=text_area.yview)
    show_scrollbar()
    root.mainloop()


if __name__ == '__main__':
    main()
