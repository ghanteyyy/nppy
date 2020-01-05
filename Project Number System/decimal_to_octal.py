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

    octal_number = ''

    # Converting into octal
    while decimal_number > 0:
        temp_octal = decimal_number % 8
        octal_number += str(temp_octal)
        decimal_number = decimal_number // 8

    print(octal_number[::-1])


if __name__ == '__main__':
    try:
        decimal_to_octal(123)

    except (ValueError, NameError):
        print('Integers was expected')
