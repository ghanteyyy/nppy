class DecimalToOctal:
    '''
    Convert decimal number to octal number

        To convert decimal to octal you need to divide decimal number by 0:
            For an instance, lets take decimal number as 98
                            8 | 123 | 3
                              ------
                            8 |  15 | 7
                              ------
                                1

            And writing the remainder in reverse way i.e 173
    '''

    def IsDecimal(self, decimal_number):
        '''
        Checking if the given number is decimal
        '''

        while decimal_number > 0:
            remainder = decimal_number % 10
            decimal_number //= 10

            if remainder not in range(10):
                return False

        return True

    def toOctal(self, decimal_number):
        '''
        Converting the decimal number to octal
        '''

        if self.IsDecimal(decimal_number):
            octal_number = ''

            while decimal_number > 0:
                temp_octal = decimal_number % 8
                octal_number += str(temp_octal)
                decimal_number = decimal_number // 8

            return octal_number[::-1]

        else:
            raise ValueError('Invalid Decimal Number')


if __name__ == '__main__':
    print(DecimalToOctal().toOctal(123))
