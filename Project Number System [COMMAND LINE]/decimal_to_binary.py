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

                Required binary number is 1111011 (writing in reverse) '''

    binary_number = ''

    # Converting into binary number
    while decimal_number > 0:
        temp_binary = decimal_number % 2
        binary_number += str(temp_binary)
        decimal_number = decimal_number // 2

    print(binary_number[::-1])


if __name__ == '__main__':
    try:
        decimal_to_binary(123)

    except (ValueError, NameError):
        print('Integers was expected')
