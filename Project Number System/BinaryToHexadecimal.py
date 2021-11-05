def BinaryToHexadecimal(binary_number):
    '''Convert binary number to hexadecimal number

        Binary number = 1111011

        To convert it to hexadecimal number:
            Step 1: Split each four value from backward like
                    111                         1011

            Step 2: Here, in first part the length is less than 4 so adding extra 0 at its front and 111 becomes 0111

            Step 3: Now using 8,4,2,1 rule in each splitted value so,
                        first,
                            0111 = 0 * 8 + 1 * 4 + 1 * 2 + 1 * 1
                                 = 7

                        second,
                            1011 = 1 * 8 + 0 * 4 + 1 * 2 + 1 * 1
                                 = 11 (B)

                                In Hexadecimal,
                                    10 = A
                                    11 = B
                                    12 = C
                                    13 = D
                                    14 = E
                                    15 = F


            Step 4: Append each value from first, second, and third which becomes to 7B

                Required hexadecimal number is 7B

        ---------------------------------------------------------------------------------------------------------------

        ALTERNATIVE METHOD:
            First, convert binary number i.e 1111011 to decimal by:
                1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                        = 123

            Second, convert obtained decimal number (319) to hexadecimal by:
                =  16| 123 |11 (B)  >>> Remainder
                    -----
                      7            >>> Remainder

                Write remainder going from down to up i.e 7B

                Required hexadecimal is 7B
    '''

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
        binary_number = str(binary_number)[::-1]
        hexa_decimal_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}
        test_hexadecimal = 0
        rule = [8, 4, 2, 1]

        listed_value = []
        hexadecimal_number = ''

        for i in range(len(binary_number) // 4 + 1):
            '''
                Here, len(binary_number) = 8
                    Then, len(binary_number) // 4 + 1 = 2 + 1 = 4
                    So, range = (0, 1, 2, 3)
            '''

            sliced_binary = binary_number[:4]  # Storing three value from binary_number in each itreation
            binary_number = binary_number[4:]  # Overwriting binary_number variable excluding value stored in sliced_binary using slicing

            if len(sliced_binary) == 4:  # Checking if the length of value stored in sliced_binary variable
                listed_value.append(sliced_binary[::-1])  # Then, appending listed_value list by reversing value stored in sliced_binary

            else:
                listed_value.append(sliced_binary[::-1].zfill(4))
                '''If length of sliced_binary is less than 4 then:
                    First, reversing value of sliced_binary
                    Second, filling 0 to make three character value

                For instance,
                    At last we get, 01 whose length is less than 4
                        then we reverse it so we get 10
                        and we fill that value '10' with '0' using zfill(3) '010' so that the length becomes 4
                '''

        listed_value = listed_value[::-1]  # Reversing the value of listed_value "list"

        for l in listed_value:  # looping to each value in listed_value list
            for x in range(len(l)):  # Then we get range value (0,1,2, 3) which is stored in temporary variable 'x' in each iteration. Here, range is generator (python 2.7)
                test_hexadecimal += int(l[x]) * rule[x]  # Here, first slicing value from 'l' and rule with the value 'x' and converting value got from 'l' by slicing into integer

            if test_hexadecimal > 9:
                test_hexadecimal = hexa_decimal_value[str(test_hexadecimal)]

            hexadecimal_number += str(test_hexadecimal)  # Converting integer value stored in test_hexadecimal to string and appending it to hexadecimal_number variable
            test_hexadecimal = 0  # Overwriting test_hexadecimal variable to '0' again

        print(hexadecimal_number.strip('0'))

    else:
        print('Invalid binary number')


'''
ALTERNATIVE METHOD:
    [CODE]
        def BinaryToHexadecimal(binary_number):
            # First, check if the given number is binary
            def is_binary():
                global check

                count = 0
                check = []

                for binn in str(binary_number):
                    if int(binn) > 1:
                        count += 1
                        check.append(binn)

                if count == 0:
                    return True

                else:
                    return False

            # Second, convert given binary number to decimal
            def binary_to_decimal(binary_number):
                global decimal_number

                decimal_number = 0
                reversed_binary_number = str(binary_number)[::-1]

                for i in range(len(str(binary_number))):
                    decimal = int(reversed_binary_number[i]) * 2 ** i
                    decimal_number += decimal

            # Third, convert obtained decimal number to hexadecimal number
            def decimal_to_hexadecimal(decimal_number):
                global hexadecimal

                hexa_decimal_value = {'10': 'A',
                                      '11': 'B',
                                      '12': 'C',
                                      '13': 'D',
                                      '14': 'E',
                                      '15': 'F'}

                hexadecimal = ''

                while int(decimal_number) > 0:
                    test_hexadecimal = int(decimal_number) % 16

                    if test_hexadecimal > 9:
                        hexadecimal += hexa_decimal_value[str(test_hexadecimal)]

                    else:
                        hexadecimal += str(test_hexadecimal)

                    decimal_number = int(decimal_number) // 16

                print(hexadecimal[::-1])  # printing reverse of value stored in hexadecimal

            # Calling functions
            if is_binary():
                binary_to_decimal(binary_number)
                decimal_to_hexadecimal(decimal_number)

            else:
                if len(check) == 1:
                    print('{} is not binary'.format(', '.joint(check)))

                else:
                    print('{} are not binary'.format(', '.joint(check)))


        if __name__ == '__main__':
            BinaryToHexadecimal(1111011)
'''


if __name__ == '__main__':
    try:
        BinaryToHexadecimal(1111011)

    except (ValueError, NameError):
        print('Integers was expected')
