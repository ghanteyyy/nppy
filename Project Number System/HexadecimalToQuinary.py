class HexadecimalToQuinary:
    '''
    Convert hexadecimal number to quinary number

        To convert hexadecimal to quinary you need to first convert hexadecimal number to decimal and obtained decimal to quinary
            For an instance, lets take hexadecimal number as 123
                Step 1: Convert the hexadecimal number to decimal
                            123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                                = 291 (decimal number)

                Step 2: Now, convert obtained decimal to quinary
                            5 | 291 | 1
                              ------
                            5 |  58 | 3
                              ------
                            5 |  11 | 1
                              ------
                                2

                    And our required quinary number is 2131 (taken in reverse order)
    '''

    def IsHexadecimal(self, hexadecimal_number):
        '''
        Checking if the given number is hexadecimal
        '''

        for num in hexadecimal_number:
            if num not in '0123456789ABCDEF':
                return False

        return True

    def toQuinary(self, hexadecimal_number):
        '''
        Converting the given hexadecimal number to quinary
        '''

        hexadecimal_number = str(hexadecimal_number)

        if self.IsHexadecimal(hexadecimal_number):
            quinary_number = ''
            decimal_number = 0
            hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

            for power, num in enumerate(hexadecimal_number[::-1]):
                if num in hex_value:
                    num = hex_value[num]

                decimal_number += int(num) * 16 ** power

            while decimal_number > 0:
                quinary_number += str(decimal_number % 5)
                decimal_number //= 5

            return quinary_number[::-1]

        else:
            raise ValueError('Invalid Hexadecimal Number')


if __name__ == '__main__':
    print(HexadecimalToQuinary().toQuinary('123'))
