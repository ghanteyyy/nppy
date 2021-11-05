def BinaryToQuinary(binary_number):
    '''Convert binary number to quinary number

        To convert quinary to binary we need to:
            Step 1: Convert given binary to decimal

                For instance, lets take binary_number as 1111011 then,
                    Converting 1111011 to decimal, we get:
                        1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                                = 123 (decimal number)

            Step 2: Convert the obtained decimal number to quinary number

                        =  5 | 123 | 3  >>> Remainder
                             ------
                          5 |  24 | 4  >>> Remainder
                            ------
                              4

                    Write remainder going from down to up i.e 443

                    Required quinary number is 443 '''

    # Checking if the given number is acutally binary
    def is_binary():
        count = 0

        for binn in str(binary_number):
            if int(binn) > 1:
                count += 1

        if count == 0:
            return True

        else:
            return False

    if is_binary():
        quinary_number = ''
        decimal_number = 0
        reversed_binary = str(binary_number)[::-1]

        # Converting binary to decimal
        for i in range(len(reversed_binary)):
            decimal_number += int(reversed_binary[i]) * 2 ** i

        # Converting obtained decimal to quinary
        while decimal_number > 0:
            test_quinary_number = decimal_number % 5
            quinary_number += str(test_quinary_number)
            decimal_number = decimal_number // 5

        print(quinary_number[::-1])

    else:
        print('Invalid binary')


if __name__ == '__main__':
    try:
        BinaryToQuinary(1111011)

    except (ValueError, NameError):
        print('Integers was expected')
