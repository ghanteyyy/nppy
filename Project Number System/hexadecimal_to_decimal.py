def hexadecimal_to_decimal(hexadecimal_number):
    '''Convert hexadecimal number to decimal number

        To convert hexadecimal to decimal you need to:
            Multipy each number by base 16 with its own power increase from left to right(first power is 0)
                123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                    = 291
    '''

    decimal_number = 0
    hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

    def is_hexadecimal():
        # Check if the given digits are hexadecimal number

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
            split_hexadecimal = str(hexadecimal_number)   # Converting to string

            for index, split_hexa_decimal in enumerate(split_hexadecimal):  # Converting A, B, C, D, E, F, G to numeric values
                if split_hexa_decimal.upper() in hex_value:
                    split_hexadecimal[index] = hex_value[split_hexa_decimal.upper()]

            reverse_split_hexadecimal = split_hexadecimal[::-1]  # Reversing the obtained numeric values

            for index, value in enumerate(reverse_split_hexadecimal):  # Converting to decimal number
                decimal_number += int(value) * 16 ** index

        else:
            reversed_hexadecimal = hexadecimal_number[::-1]

            # Converting to decimal
            for index, value in enumerate(reversed_hexadecimal):
                decimal_number += int(value) * 16 ** index

        print(decimal_number)

    else:
        print('Invalid hexadecimal number')


if __name__ == '__main__':
    try:
        hexadecimal_to_decimal('123')

    except (ValueError, NameError):
        print('Integers was expected')
