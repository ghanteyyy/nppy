class OctalToDecimal:
    '''
    Convert octal number to decimal number

        To convert octal to decimal you need to:
            Multiply each number by base 8 with its own power increase from left to right(first power is 0)
                123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                    =  83
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

    def toDecimal(self, octal_number):
        '''
        Converting the given octal number to decimal
        '''

        decimal_number = 0

        if self.IsOctal(octal_number):
            for power, num in enumerate(str(octal_number)[::-1]):
                decimal_number += int(num) * 8 ** power

            return decimal_number

        else:
            raise ValueError('Invalid Octal Number')


if __name__ == '__main__':
    print(OctalToDecimal().toDecimal(123))
