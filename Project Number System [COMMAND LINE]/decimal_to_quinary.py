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

    quinary_number = ''

    # Converting into quinary
    while decimal_number > 0:
        test_quinary_number = decimal_number % 5
        quinary_number += str(test_quinary_number)
        decimal_number = decimal_number // 5

    print(quinary_number[::-1])


if __name__ == '__main__':
    try:
        decimal_to_quinary(123)

    except (ValueError, NameError):
        print('Integers was expected')
