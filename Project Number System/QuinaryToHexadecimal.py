class QuinaryToHexadecimal:
    '''
    Convert quinary number into hexadecimal number

        You can convert quinary number, first by converting quinary number to decimal and then obtained decimal to hexadecimal number
            For an instance, lets take quinary number to be 123

            Step 1: Convert to quinary number to decimal
                    123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                        = 38 (Decimal)

            Step 2: Convert obtained decimal number to hexadecimal
                            16 | 38 | 6
                               -----
                                 2

                    And our required hexadecimal number is 26
    '''

    def IsQuinary(self, quinary_number):
        '''
        Checking if the given number is quinary
        '''

        while quinary_number > 0:
            remainder = quinary_number % 10
            quinary_number //= 10

            if remainder not in range(5):
                return False

        return True

    def toHexadecimal(self, quinary_number):
        '''
        Converting the given quinary number to hexadecimal
        '''

        if self.IsQuinary(quinary_number):
            decimal_number = 0
            hexadecimal_number = ''
            hex_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}

            for power, num in enumerate(str(quinary_number)[::-1]):
                decimal_number += int(num) * 5 ** power

            while decimal_number > 0:
                remainder = str(decimal_number % 16)

                if remainder in hex_value:
                    remainder = hex_value[remainder]

                decimal_number //= 16
                hexadecimal_number += remainder

            return hexadecimal_number[::-1]

        else:
            raise ValueError('Invalid Quinary Number')


if __name__ == '__main__':
    print(QuinaryToHexadecimal().toHexadecimal(123))
