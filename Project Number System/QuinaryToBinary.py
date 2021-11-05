def QuinaryToBinary(quinary_number):
    '''Convert quinary number to binary number

        You can convert quinary number to binary, first by converting quinary number to decimal and obtained decimal to binary number
            For an instance, lets take quinary number be 123

                Step 1: Convert quinary number to decimal
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38 (Decimal)

                Step 2: Convert obtained decimal number to binary
                              2 | 38 | 0
                                -----
                             2 | 19 | 1
                               -----
                            2 |  9 | 1
                              -----
                           2 |  4 | 0
                             -----
                          2 |  2 | 0
                            -----
                              1


                        And our required binary number is 100110 (taken remainder in reverse way)
    '''

    quinary_number = str(quinary_number)

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
        binary = ''
        decimal_number = 0
        reversed_quinary = str(quinary_number)[::-1]

        for index, value in enumerate(reversed_quinary):
            decimal_number += int(value) * 5 ** index

        while decimal_number > 0:
            binary += str(decimal_number % 2)
            decimal_number = decimal_number // 2

        print(binary[::-1])


if __name__ == '__main__':
    try:
        QuinaryToBinary(123)

    except (ValueError, NameError):
        print('Integers was expected')
