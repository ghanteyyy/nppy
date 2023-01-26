class DecimalToQuinary:
    '''
    Convert decimal number to quinary number

        For an instance, lets take decimal_number as 123 then,

        To calculate decimal_number to quinary you need to:
                        5 | 123 | 3
                          ------
                        5 | 24  | 4
                          ------
                            4

        Required quinary number is 443
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

    def toQuinary(self, decimal_number):
        '''
        Converting the given decimal number to quinary
        '''

        if self.IsDecimal(decimal_number):
            quinary_number = ''

            while decimal_number > 0:
                quinary_number += str(decimal_number % 5)
                decimal_number = decimal_number // 5

            return quinary_number[::-1]

        else:
            raise ValueError('Invalid Decimal Number')


if __name__ == '__main__':
    print(DecimalToQuinary().toQuinary(123))
