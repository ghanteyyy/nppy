def QuinaryToDecimal(quinary_number):
    '''Convert quinary number to decimal number

        You can convert quinary number to decimal by multiplying each quinary number with base of 5 with power starting from 0 increasing from left to right.
            For an instance, lets take quinary number be 123

                Step 1: Converting to decimal number
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38

                    And our required quinary number is 38 '''

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
        decimal = 0
        reversed_binary = str(quinary_number)[::-1]

        for index, value in enumerate(reversed_binary):
            decimal += int(value) * 5 ** index

        print(decimal)

    else:
        print('Invalid quinary number')


if __name__ == '__main__':
    try:
        QuinaryToDecimal(123)

    except (ValueError, NameError):
        print('Integers was expected')
