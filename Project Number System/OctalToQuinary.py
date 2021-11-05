def OctalToQuinary(octal_number):
    '''Convert octal number to quinary number

        You can covert octal_number to binary by converting the given octal_number to decimal and then obtained decimal to quinary
            For an instance, lets take an octal number to be 123

                Step 1: Covert octal number to decimal number
                        123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                            = 83 (decimal number)

                Step 2: Convert the obtained decimal number to quinary number
                            5 | 83 | 3
                              -----
                           5 | 16 | 1
                             -----
                               3

                REQUIRED QUINARY NUMBER is 313 (taking remainder in reverse order)
    '''

    try:
        decimal_number = 0
        quinary_number = ''
        reversed_octal_number = str(octal_number)[::-1]

        def is_octal():
            count = 0

            for oct_num in str(octal_number):
                if int(oct_num) >= 8:
                    count += 1

            if count == 0:
                return True

            else:
                return False

        if is_octal():
            # Converting to decimal
            for x in range(len(reversed_octal_number)):
                decimal_number += int(reversed_octal_number[x]) * 8 ** x

            # Converting obtained decimal to quinary
            while decimal_number > 0:
                test_quinary = decimal_number % 5   # Getting remainder
                quinary_number += str(test_quinary)
                decimal_number = decimal_number // 5

            print(quinary_number[::-1])

        else:
            print('Invalid quinary number')

    except ValueError:
        print('Octal number must be less than 8')


if __name__ == '__main__':
    try:
        OctalToQuinary(123)

    except (ValueError, NameError):
        print('Integers was expected')
