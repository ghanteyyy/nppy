def octal_to_hexadecimal(octal_number):
    '''Convert octal number to hexadecimal number

        To convert octal number to hexadecimal you need to first convert the octal number to decimal and obtained decimal to hexadecimal
            For an instance, lets take an octal number 276
                Step 1: Convert octal number(276) to decimal
                        276 = 2 * 8^2 + 7 * 8^1 + 6 * 8^0
                            = 190 (decimal number)

                Step 2: Then, convert obtained decimal number to octal
                                16 | 190 | 14 (E)   >>> Remainder
                                   ------
                               16 |  11 | 11 (B)    >>> Remainder
                                  ------
                                    0


                            And our required hexadecimal is BE (taking remainder in reverse(i.e from down to up))
    '''

    def is_octal():
        global check

        count = 0

        for oct_num in str(octal_number):
            if int(oct_num) >= 8:
                count += 1

        if count == 0:
            return True

        else:
            return False

    if is_octal():
        decimal_number = 0
        reversed_oct_num = str(octal_number)[::-1]
        hexadecimal_num = ''

        hexx_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}

        # Converting to decimal
        for x in range(len(reversed_oct_num)):
            test_decimal = int(reversed_oct_num[x]) * 8 ** x
            decimal_number += test_decimal
            octal_number = octal_number // 8

        # Converting to hexadecimal
        while decimal_number > 0:
            test_hexadecimal = str(decimal_number % 16)

            if int(test_hexadecimal) > 9:
                hexadecimal_num += hexx_value[test_hexadecimal]

            else:
                hexadecimal_num += test_hexadecimal

            decimal_number = decimal_number // 16

        print(hexadecimal_num[::-1])

    else:
        print('Invalid octal number')


if __name__ == '__main__':
    try:
        octal_to_hexadecimal(276)

    except (ValueError, NameError):
        print('Integers was expected')
