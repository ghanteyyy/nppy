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

    quinary_number = ''
    decimal_number = 0
    hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

    hexadecimal_number = str(hexadecimal_number)

    def is_hexadecimal():
        count = 0

        if hexadecimal_number.isalpha() or hexadecimal_number.isalnum():
            for hexa_decimal in hexadecimal_number:
                if hexa_decimal.isalpha() and hexa_decimal not in list('ABCDEF'):
                    count += 1

        if count == 0:
            return True

        else:
            return False

    if is_hexadecimal():
        if hexadecimal_number.isalpha() or hexadecimal_number.isalnum():
            split_hexadecimal = list(str(hexadecimal_number))

            for index, split_hexa_decimal in enumerate(split_hexadecimal):
                if split_hexa_decimal in hex_value:
                    split_hexadecimal[index] = hex_value[split_hexa_decimal]

            reverse_split_hexadecimal = split_hexadecimal[::-1]

            for index, value in enumerate(reverse_split_hexadecimal):
                decimal_number += int(value) * 16 ** index

            while decimal_number > 0:
                quinary_number += str(decimal_number % 5)
                decimal_number = decimal_number // 5

            print(quinary_number[::-1])

        else:
            reversed_hexadecimal = hexadecimal_number[::-1]

            # Converting to decimal
            for index, value in enumerate(reversed_hexadecimal):
                decimal_number += int(value) * 16 ** index

            # Converting to binary
            while decimal_number > 0:
                quinary_number += str(decimal_number % 5)
                decimal_number = decimal_number // 5

            print(quinary_number[::-1])

    else:
        print('Invalid hexadecimal number')


if __name__ == '__main__':
    try:
        hexadecimal_to_quinary('123')

    except (ValueError, NameError):
        print('Integers was expected')
