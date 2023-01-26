class HexadecimalToOctal:
    '''
    Convert hexadecimal number to octal number

        To calculate hexadecimal to octal you need to first convert hexadecimal to decimal and obtained decimal to octal
            For an instance, lets take hexadecimal number as 123
                Step 1: Converting to decimal number
                        123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                            = 291 (decimal number)

                Step 2: Convert obtained decimal number to octal number
                                8 | 291 | 3
                                  ------
                                8 |  36 | 4
                                  ------
                                     4

                    And our required octal number is 443 (taken in reverse order)
    '''

    def IsHexadecimal(self, hexadecimal_number):
        '''
        Checking if the given number is hexadecimal
        '''

        for num in hexadecimal_number:
            if num not in '0123456789ABCDEF':
                return False

        return True

    def toOctal(self, hexadecimal_number):
        '''
        Converting if the given hexadecimal number to octal
        '''

        hexadecimal_number = str(hexadecimal_number)
        hex_value = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

        if self.IsHexadecimal(hexadecimal_number):
            octal_number = ''
            decimal_number = 0

            for power, num in enumerate(hexadecimal_number[::-1]):
                if num in hex_value:
                    num = hex_value[num]

                decimal_number += int(num) * 16 ** power

            while decimal_number > 0:
                octal_number += str(decimal_number % 8)
                decimal_number //= 8

            return octal_number[::-1]

        else:
            raise ValueError('Invalid Hexadecimal Number')


if __name__ == '__main__':
    print(HexadecimalToOctal().toOctal('123'))
