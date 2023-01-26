class DecimalToHexadecimal:
    '''
    Convert decimal number to hexadecimal number
        To convert decimal number to hexadecimal, you need to:
            For instance, lets take decimal number as 123
                Divide decimal number until remainder becomes 0
                                        16 | 123 | 11 (B)
                                           ------
                                              7

                Required hexadecimal number is 7B
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

    def toHexadecimal(self, decimal_number):
        '''
        Converting decimal number to hexadecimal
        '''

        if self.IsDecimal(decimal_number):
            hexadecimal = ''
            hex_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}

            while decimal_number > 0:
                remainder = str(decimal_number % 16)

                if remainder in hex_value:
                    hexadecimal += hex_value[remainder]

                else:
                    hexadecimal += remainder

                decimal_number = decimal_number // 16

            return hexadecimal[::-1]

        else:
            raise ValueError('Invalid Decimal Number')


if __name__ == '__main__':
    print(DecimalToHexadecimal().toHexadecimal(123))
