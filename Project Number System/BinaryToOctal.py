def BinaryToOctal(binary_number):
    '''Convert binary number to octal number

        Binary number = 1111011

        To convert it to octal number:
            Step 1: Split each three value from backward like
                    1           111            011

            Step 2: Here, we have all splited value having length 3 except one i.e 1 so adding extra two '0's in the front of 1
                    001 to make its length 3

                    Then finally we have,
                        001               111               011

            Step 3: Now using 4,2,1 rule so,
                        first,
                            001 = 0 * 4 + 0 * 2 + 1 * 1
                                = 1
                        second,
                            111 = 1 * 4 + 1 * 2 + 1 * 1
                                = 7
                        third,
                            011 = 0 * 4 + 1 * 2 + 1 * 1
                                = 3

            Step 4: Append each value from first, second, and third which becomes to 173

            Required octal number is 173

        -----------------------------------------------------------------------------------------------------------------------------

        Altenative Way

        First, split binary number to between three digits like
                   001            111             011

        Second, use 4, 2, 1 rule to convert each splitted value to decimal number
                    001 = 0 * 4 + 0 * 2 + 1 * 1
                        = 1

                    111 = 1 * 4 + 1 * 2 + 1 * 1
                        = 7

                    011 = 0 * 4 + 1 * 2 + 1 * 1
                        = 3

                Hence, append all value and we get final result 173 (octal number) '''

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

        test_octal = 0
        rule = [4, 2, 1]

        listed_value = []
        octal_number = ''

        for i in range(len(binary_number) // 3 + 1):
            '''
                Here, len(binary_number) = 8
                    Then, len(binary_number) // 3 + 1 = 2 + 1 = 3
                    So, range = (0, 1, 2)
            '''

            sliced_binary = binary_number[:3]  # Storing three value from binary_number in each itreation
            binary_number = binary_number[3:]  # Overwriting binary_number variable excluding value stored in sliced_binary using slicing

            if len(sliced_binary) == 3:  # Checking if the length of value stored in sliced_binary variable
                listed_value.append(sliced_binary[::-1])  # Then, appending listed_value list by reversing value stored in sliced_binary

            else:
                listed_value.append(sliced_binary[::-1].zfill(3))
                '''If length of sliced_binary is less than 3 then:
                    First, reversing value of sliced_binary
                    Second, filling 0 to make three character value

                For instance,
                    At last we get, 01 whose length is less than 3
                        then we reverse it so we get 10
                        and we fill that value '10' with '0' using zfill(3) '010' so that the length becomes 3
                '''

        listed_value = listed_value[::-1]  # Reversing the value of listed_value "list"

        for l in listed_value:  # looping to each value in listed_value list
            for x in range(len(l)):  # Then we get range value (0,1,2) which is stored in temporary variable 'x' in each iteration. Here, range is generator (python 2.7)
                test_octal += int(l[x]) * rule[x]  # Here, first slicing value from 'l' and rule with the value 'x' and converting value got from l by slicing into integer

            octal_number += str(test_octal)  # Converting integer value stored in test_octal to string and appending it to octal_number variable
            test_octal = 0  # Overwriting test_octal variable to '0' again

        print(octal_number.strip('0'))

    else:
        print('Invalid binary number')


'''
Alternative Method:
    [CODE]
        def BinaryToOctal(binary_number):
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

            # Third, convert obtained decimal number to Octal number
            def decimal_to_octal(decimal_number):
                octal_number = ''

                while int(decimal_number) > 0:
                    octal = int(decimal_number) % 8
                    octal_number += str(octal)
                    decimal_number = int(decimal_number) // 8

                print(octal_number[::-1]) # printing reverse of value stored in octal_number

            # Calling functions
            if is_binary():
                binary_to_decimal(binary_number)
                decimal_to_octal(decimal_number)

            else:
                if len(check) == 1:
                    print('{} is not binary'.format(', '.join(check)))

                else:
                    print('{} are not binary'.format(', '.join(check)))


        if __name__ == '__main__':
            BinaryToOctal(1111011)
'''


if __name__ == '__main__':
    try:
        BinaryToOctal(1111011)

    except (ValueError, NameError):
        print('Integers was expected')
