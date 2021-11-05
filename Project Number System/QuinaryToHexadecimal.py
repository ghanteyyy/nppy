def QuinaryToHexadecimal(quinary_number):
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

    decimal = 0
    hexadecimal = ''
    reversed_quinary = str(quinary_number)[::-1]
    hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

    def is_quinary():
        count = 0

        for quinary in str(quinary_number):
            if int(quinary) >= 5:
                count += 1

        if count == 0:
            return True

        else:
            return False

    if is_quinary():
        for x in range(len(reversed_quinary)):
            decimal += int(reversed_quinary[x]) * 5 ** x

        while decimal > 0:
            hex_num = decimal % 16

            if hex_num in hex_value:
                hexadecimal += hex_value[hex_num]

            else:
                hexadecimal += str(hex_num)

            decimal = decimal // 16

        print(hexadecimal[::-1])

    else:
        print('Invalid quinary number')


if __name__ == '__main__':
    try:
        QuinaryToHexadecimal(123)

    except (ValueError, NameError):
        print('Integers was expected')
