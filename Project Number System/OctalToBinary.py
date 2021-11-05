def OctalToBinary(octal_number):
    '''
        For an instance, lets take an octal number 6292

            To calculate you need to:
                Step 1: Convert the given octal number to decimal.
                            6242 = 6 * 8^3 + 2 * 8^2 + 4 * 8^1 + 2 * 8^0
                                 = 3234

                Step 2: Convert the obtained decimal to binary
                                    2 | 3234 | 0  <<< Remainder
                                      -------
                                   2 | 1617 | 1  <<< Remainder
                                     -------
                                  2 |  808 | 0  <<< Remainder
                                    -------
                                 2 |  404 | 0  <<< Remainder
                                   -------
                                2 |  202 | 0  <<< Remainder
                                  -------
                               2 |  101 | 1  <<< Remainder
                                 -------
                              2 |  50  | 0  <<< Remainder
                                -------
                             2 |  25  | 1  <<< Remainder
                               -------
                            2 |  12  | 0  <<< Remainder
                              -------
                           2 |   6  | 0  <<< Remainder
                             -------
                          2 |   3  | 1  <<< Remainder
                            -------
                                1       <<< Remainder


                        And our required binary is 110010100010

            -----------------------------------------------------------------------------------------------------------------

                ALTERNATIVE WAY!
                    Step 1: Split the octal number
                                6       2       4       2

                    Step 2: Now convert each splitted number to binary.
                                2 | 6 | 0        2 | 2 | 0      2 | 4 | 0       2 | 2 | 0
                                  ----             ----           ----            ----
                               2 | 3 | 1            1          2 | 2 | 0           1
                                 ----                            ----
                                  1                               1

                            Here,
                                6    = 110

                                2    = 10   (Here lenght of the remainder is less than 3 so add extra one 0 at its front)
                                     = 010  (After adding extra one 0)

                                4    = 100

                                2    = 10   (Here lenght of the remainder is less than 3 so add extra one 0 at its front)
                                     = 010  (After adding extra one 0)

                            Now, combine all obtained binary number we get,
                                        110010100010
    '''

    def is_octal():
        global check

        count = 0
        check = []

        for oct_num in str(octal_number):
            if int(oct_num) >= 8:
                count += 1
                check.append(str(oct_num))

        if count == 0:
            return True

        else:
            return False

    if is_octal():
        binary = ''
        decimal = 0
        reversed_octal = str(octal_number)[::-1]

        # Converting into decimal
        for x in range(len(str(octal_number))):
            test_decimal = int(reversed_octal[x]) * 8 ** x
            decimal += test_decimal

        # Converting into obtained decimal to binary
        while decimal > 0:
            test_binary = decimal % 2
            binary += str(test_binary)
            decimal = decimal // 2

        print(binary[::-1])

    else:
        print('Invalid octal number')


'''
    ALTERNATIVE WAY!
        [CODE]
            def OctalToBinary(octal_number):
                def is_octal():
                    global check

                    count = 0
                    check = []

                    for oct_num in str(octal_number):
                        if oct_num > 7:
                            count += 1
                            check.append(str(oct_num))

                    if count == 1:
                        return True

                    else:
                        return False

                # Converting into binary
                if is_octal():
                    binary = ''
                    test_binary = ''
                    splitted_octal = list(str(octal_number))

                    for split_octal in splitted_octal:
                        int_oct = int(split_octal)

                        while int_oct > 0:
                            test_binary += str(int_oct % 2)
                            int_oct = int_oct // 2

                            if len(test_binary) > 3:
                                binary += test_binary[::-1]

                            else:
                                binary += test_binary[::-1].zfill(3)

                            test_binary = ''

                            print(binary)

                else:
                    if len(check) == 1:
                        print('{} is not octal'.format(', '.join(check)))

                    else:
                        print('{} are not octal'.format(', '.join(check)))


            if __name__ == '__main__':
                OctalToBinary(octal_number)

'''


if __name__ == '__main__':
    try:
        OctalToBinary(6242)

    except (ValueError, NameError):
        print('Integers was expected')
