class HexadecimalToBinary:
    def __init__(self):
        self.HexValue = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

    def IsHexadecimal(self, hexadecimal_number):
        '''
        Checking if the given number is hexadecimal
        '''

        for num in hexadecimal_number:
            if num not in '0123456789ABCDEF':
                return False

        return True

    def toBinary(self, hexadecimal_number):
        '''
        Convert hexadecimal number to binary number

            To convert hexadecimal to binary, you need to first convert hexadecimal to decimal and obtained decimal to binary
                Step 1: Convert hexadecimal to decimal
                        123 = 1 * 16^2 + 2 * 16^1 + 3 * 16^0
                            = 291 (decimal number)

                Step 2: Convert the obtained decimal to binary
                        2 | 291 | 1
                           ------
                        2 | 145 | 1
                           ------
                        2 |  72 | 0
                           ------
                        2 |  36 | 0
                           ------
                        2 |  18 | 0
                           ------
                        2 |  9  | 1
                           ------
                        2 |  4  | 0
                           ------
                        2 |  2  | 0
                           ------
                             1

                Required binary number is 100100011 (taking remainder in reverse order)
        '''

        hexadecimal_number = str(hexadecimal_number)

        if self.IsHexadecimal(hexadecimal_number):
            binary_number = ''
            decimal_number = 0
            self.HexValue = {'A': '10', 'B': '11', 'C': '12', 'D': '13', 'E': '14', 'F': '15'}

            for power, num in enumerate(hexadecimal_number[::-1]):
                if num in self.HexValue:
                    num = self.HexValue[num]

                decimal_number += int(num) * 16 ** power

            while decimal_number > 0:
                binary_number += str(decimal_number % 2)
                decimal_number //= 2

            return binary_number[::-1]

        else:
            raise ValueError('Invalid Hexadecimal Number')

    def AlternativeMethod(self, hexadecimal_number):
        '''
        1. Loop to each hexadecimal number
        2. Convert each hexadecimal number to binary
        3. If obtained binary length is not 4 then reverse it and insert '0's to
           make its length 4
        4. If obtained binary length is equal to 4 then reversing it
        5. Remove leading '0' from the obtained binary
        '''

        binary_number = ''
        hexadecimal_number = str(hexadecimal_number)

        if self.IsHexadecimal(hexadecimal_number):
            for num in hexadecimal_number:
                if num in self.HexValue:
                    num = self.HexValue[num]

                num = int(num)
                tempBinary = ''

                while num > 0:
                    tempBinary += str(num % 2)
                    num //= 2

                binary_number += tempBinary[::-1].zfill(4)

            return binary_number.lstrip('0')

        else:
            raise ValueError('Invalid Hexadecimal Number')


if __name__ == '__main__':
    print(HexadecimalToBinary().toBinary('123'))
    print(HexadecimalToBinary().AlternativeMethod('123'))
