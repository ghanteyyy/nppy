def DecimalToHexadecimal(decimal_number):
    '''Convert decimal number to hexadecimal number

            To convert decimal number to hexadecimal, you need to:
                    For instance, lets take decimal number as 123

                    Divide decimal number until remainder becomes 0
                                            16| 123 | 11 (B)  >>> Remainder
                                                ------
                                                    7   >>> Remainder

                    Required hexadecimal number is 7B '''

    hexadecimal = ''

    hexa_decimal_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}

    # Converting intto hexadecimal number
    while decimal_number > 0:
        test_hexadecimal = decimal_number % 16

        if test_hexadecimal > 9:
            hexadecimal += hexa_decimal_value[str(test_hexadecimal)]

        else:
            hexadecimal += str(test_hexadecimal)

        decimal_number = decimal_number // 16

    print(hexadecimal[::-1])


if __name__ == '__main__':
    try:
        DecimalToHexadecimal(123)

    except (ValueError, NameError):
        print('Integers was expected')
