def quinary_to_octal(quinary_number):
    '''Convert quinary number to octal number

        You can convert quinary number to octal, first by converting quinary number to decimal and obtained decimal number to quinary number
            For an instance, lets take binary number be 123

                Step 1: Convert to deicmal
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38 (Decimal)

                Step 2: Convert to octal from the obtained decimal
                                    8 | 38 | 6
                                      -----
                                        4

                            And our required octal number is 46 (taken in a reverse way)
    '''

    def is_octal():
        count = 0

        for quinary in str(quinary_number):
            if int(quinary) >= 5:
                count += 1

        if count == 0:
            return True

        else:
            return False

    if is_octal():
        decimal = 0
        octal_number = ''
        reversed_quinary = str(quinary_number)[::-1]

        for index, value in enumerate(reversed_quinary):
            decimal += int(value) * 5 ** index

        while decimal > 0:
            octal_number += str(decimal % 8)
            decimal = decimal // 8

        print(octal_number[::-1])

    else:
        print('Invalid quinary Number')


if __name__ == '__main__':
    try:
        quinary_to_octal(123)

    except (ValueError, NameError):
        print('Integers was expected')
