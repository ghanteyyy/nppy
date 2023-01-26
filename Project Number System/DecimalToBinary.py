class DecimalToBinary:
    '''
    Convert decimal number to binary number

        To convert decimal to binary you need to divide the decimal number by 2 and write the remainder in reverse way
            For an instance, lets take decimal number as 33, then the calculation is as follow:
                    2 | 123 | 1
                      ------
                    2 | 61  | 1
                      ------
                    2 | 30  | 0
                        -----
                    2 | 15  | 1
                        -----
                    2 |  7  | 1
                      ------
                    2 |  3  | 1
                      ------
                        1

            Required binary number is 1111011 (writing in reverse)
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

    def toBinary(self, decimal_number):
        '''
        Converting the decimal number into binary
        '''

        if self.IsDecimal(decimal_number):
            binary_number = ''

            while decimal_number > 0:
                temp_binary = decimal_number % 2
                binary_number += str(temp_binary)
                decimal_number = decimal_number // 2

            return binary_number[::-1]

        else:
            raise ValueError('Invalid Decimal Number')


if __name__ == '__main__':
    print(DecimalToBinary().toBinary(123))

