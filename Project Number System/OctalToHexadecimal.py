class OctalToHexadecimal:
    '''
    Convert octal number to hexadecimal number

        To convert octal number to hexadecimal you need to first convert the octal number to decimal and obtained decimal to hexadecimal
            For an instance, lets take an octal number 276
                Step 1: Convert octal number(276) to decimal
                        276 = 2 * 8^2 + 7 * 8^1 + 6 * 8^0
                            = 190 (decimal number)

                Step 2: Then, convert obtained decimal number to octal
                                16 | 190 | 14 (E)   >>> Remainder
                                   ------
                                16 |  11 | 11 (B)    >>> Remainder
                                   ------
                                      0

                            And our required hexadecimal is BE (taking remainder in reverse(i.e from down to up))
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

    def toHexadecimal(self, octal_number):
        '''
        Converting the given octal number to hexadecimal
        '''

        if self.IsOctal(octal_number):
            decimal_number = 0
            hexadecimal_number = ''
            hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

            for power, num in enumerate(str(octal_number)[::-1]):
                decimal_number += int(num) * 8 ** power

            while decimal_number > 0:
                remainder = str(decimal_number % 16)

                if remainder in hex_value:
                    remainder = hex_value[remainder]

                decimal_number //= 16
                hexadecimal_number += remainder

            return hexadecimal_number[::-1]

        else:
            raise ValueError('Invalid Octal Number')


if __name__ == '__main__':
    print(OctalToHexadecimal().toHexadecimal(276))
