class OctalToBinary:
    '''
    Convert octal number to binary number

        For an instance, lets take an octal number 6292
            To calculate you need to:
                Step 1: Convert the given octal number to decimal.
                            6242 = 6 * 8^3 + 2 * 8^2 + 4 * 8^1 + 2 * 8^0
                                 = 3234
                Step 2: Convert the obtained decimal to binary
                            2 | 3234 | 0
                               -------
                            2 | 1617 | 1
                               -------
                            2 |  808 | 0
                               -------
                            2 |  404 | 0
                               -------
                            2 |  202 | 0
                               -------
                            2 |  101 | 1
                               -------
                            2 |  50  | 0
                               -------
                            2 |  25  | 1
                               -------
                            2 |  12  | 0
                               -------
                            2 |   6  | 0
                               -------
                            2 |   3  | 1
                               -------
                                  1

                    And our required binary is 110010100010
    '''

    def IsOctal(self, octal_number):
        '''
        Checking if the given number is octal
        '''

        while octal_number > 0:
            remainder = octal_number % 10
            octal_number //= 10

            if remainder not in range(8):
                return False

        return True

    def toBinary(self, octal_number):
        '''
        Converting given octal number to binary
        '''

        if self.IsOctal(octal_number):
            binary_number = ''
            decimal_number = 0

            for power, num in enumerate(str(octal_number)[::-1]):
                decimal_number += int(num) * 8 ** power

            while decimal_number > 0:
                binary_number += str(decimal_number % 2)
                decimal_number = decimal_number // 2

            return binary_number[::-1]

        else:
            raise ValueError('Invalid Octal Number')

    def AlternativeMethod(self, octal_number):
        '''
        Step 1: Split the octal number
                    6       2       4       2

        Step 2: Now convert each splitted number to binary.
                    2 | 6 | 0        2 | 2 | 0      2 | 4 | 0       2 | 2 | 0
                      -----            -----          -----           -----
                    2 | 3 | 1            1          2 | 2 | 0           1
                      -----                           -----
                        1                               1

                Here,
                    6   = 110

                    2   = 10   (Here length of the remainder is less than 3 so add extra one 0 at its front)
                        = 010  (After adding extra one 0)

                    4   = 100

                    2   = 10   (Here length of the remainder is less than 3 so add extra one 0 at its front)
                        = 010  (After adding extra one 0)

                Now, combine all obtained binary number we get,
                            110010100010
        '''

        binary_number = ''

        if self.IsOctal(octal_number):
            for num in str(octal_number):
                num = int(num)
                tempBinary = ''

                while num > 0:
                    tempBinary += str(num % 2)
                    num //= 2

                binary_number += tempBinary[::-1].zfill(3)

            return binary_number.lstrip('0')

        else:
            raise ValueError('Invalid Octal Number')


if __name__ == '__main__':
    print(OctalToBinary().toBinary(6242))
    print(OctalToBinary().AlternativeMethod(6242))
