class HexadecimalToDecimal:
    '''
    Convert hexadecimal number to decimal number

        To convert hexadecimal to decimal you need to:
            Multiply each number by base 16 with its own power increase from left to right(first power is 0)
                123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                    = 291
    '''

    def IsHexadecimal(self, hexadecimal_number):
        '''
        Checking if the given number is hexadecimal
        '''

        for num in hexadecimal_number:
            if num not in '0123456789ABCDEF':
                return False

        return True

    def toDecimal(self, hexadecimal_number):
        '''
        Converting given hexadecimal number to decimal
        '''

        hexadecimal_number = str(hexadecimal_number)

        if self.IsHexadecimal(hexadecimal_number):
            decimal_number = 0
            power = len(hexadecimal_number) - 1
            hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

            for num in hexadecimal_number:
                if num in hex_value:
                    num = hex_value[num]

                decimal_number += int(num) * 16 ** power
                power -= 1

            return decimal_number

        else:
            raise ValueError('Invalid Hexadecimal Number')


if __name__ == '__main__':
    print(HexadecimalToDecimal().toDecimal('123'))
