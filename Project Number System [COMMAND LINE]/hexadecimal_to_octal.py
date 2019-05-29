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
    octal_number = ''
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

            for x in range(len(reverse_split_hexadecimal)):
                decimal_number += int(reverse_split_hexadecimal[x]) * 16 ** x

            while decimal_number > 0:
                octal_number += str(decimal_number % 8)
                decimal_number = decimal_number // 8

            print(octal_number[::-1])

        else:
            reversed_hexadecimal = hexadecimal_number[::-1]

            # Converting to decimal
            for x in range(len(reversed_hexadecimal)):
                decimal_number += int(reversed_hexadecimal[x]) * 16 ** x

            while decimal_number > 0:
                octal_number += str(decimal_number % 8)
                decimal_number = decimal_number // 8

            print(octal_number[::-1])

    else:
        print('Invalid hexadecimal number')


if __name__ == '__main__':
    try:
        hexadecimal_to_octal('291')

    except (ValueError, NameError):
        print('Integers was expected')
