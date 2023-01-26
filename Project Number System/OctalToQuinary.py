class OctalToQuinary:
    '''
    Convert octal number to quinary number

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

    def toQuinary(self, octal_number):
        '''
        Converting the given octal number to quinary
        '''

        decimal_number = 0
        quinary_number = ''

        if self.IsOctal(octal_number):
            for power, num in enumerate(str(octal_number)[::-1]):
                decimal_number += int(num) * 8 ** power

            while decimal_number > 0:
                quinary_number += str(decimal_number % 5)
                decimal_number //= 5

            return quinary_number[::-1]

        else:
            raise ValueError('Invalid Quinary Number')


if __name__ == '__main__':
    print(OctalToQuinary().toQuinary(123))
