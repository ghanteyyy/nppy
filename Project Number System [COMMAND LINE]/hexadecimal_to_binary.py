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

    binary_number = ''
    decimal_number = 0
    hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

    hexadecimal_number = str(hexadecimal_number)

    def is_hexadecimal():
        count = 0

        if hexadecimal_number.isalpha() or hexadecimal_number.isalnum():
            for hexa_decimal in hexadecimal_number:
                if hexa_decimal.isalpha() and hexa_decimal.upper() not in list('ABCDEF'):
                    count += 1

        if count == 0:
            return True

        else:
            return False

    if is_hexadecimal():
        if hexadecimal_number.isalpha() or not hexadecimal_number.isdigit():
            split_hexadecimal = list(str(hexadecimal_number))

            for index, split_hexa_decimal in enumerate(split_hexadecimal):
                if split_hexa_decimal.upper() in hex_value:
                    split_hexadecimal[index] = hex_value[split_hexa_decimal.upper()]

            reverse_split_hexadecimal = split_hexadecimal[::-1]

            for index, value in enumerate(reverse_split_hexadecimal):
                decimal_number += int(reverse_split_hexadecimal[index]) * 16 ** index

            while decimal_number > 0:
                binary_number += str(decimal_number % 2)
                decimal_number = decimal_number // 2

        else:
            reversed_hexadecimal = hexadecimal_number[::-1]

            # Converting to decimal
            for x in range(len(reversed_hexadecimal)):
                decimal_number += int(reversed_hexadecimal[x]) * 16 ** x

            # Converting to binary
            while decimal_number > 0:
                binary_number += str(decimal_number % 2)
                decimal_number = decimal_number // 2

        print(binary_number[::-1])

    else:
        print('Invalid hexadecimal number')


if __name__ == '__main__':
    try:
        hexadecimal_to_binary('123')

    except (ValueError, NameError):
        print('Integers was expected')
