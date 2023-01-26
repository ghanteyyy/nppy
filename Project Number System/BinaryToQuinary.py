class BinaryToQuinary:
    '''
    Convert binary number to quinary number

        To convert quinary to binary we need to:
            Step 1: Convert given binary to decimal

                For instance, lets take binary_number as 1111011 then,
                    Converting 1111011 to decimal, we get:
                        1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                                = 123 (decimal number)

            Step 2: Convert the obtained decimal number to quinary number

                        =  5 | 123 | 3
                             ------
                           5 |  24 | 4
                             ------
                               4

                    Write remainder going from down to up i.e 443

                    Required quinary number is 443
    '''

    def IsBinary(self, binary_number):
        '''
        Check if the given number is binary
        '''

        while binary_number > 0:
            remainder = binary_number % 10
            binary_number //= 10

            if remainder not in [0, 1]:
                return False

        return True

    def toQuinary(self, binary_number):
        '''
        Converting binary number to quinary
        '''

        if self.IsBinary(binary_number):
            decimal_number = 0
            quinary_number = ''

            for power, num in enumerate(str(binary_number)[::-1]):
                decimal_number += int(num) * 2 ** power

            while decimal_number > 0:
                tempQuinaryNumber = decimal_number % 5
                quinary_number += str(tempQuinaryNumber)
                decimal_number = decimal_number // 5

            return quinary_number[::-1]

        else:
            raise ValueError('Invalid Binary Number')


if __name__ == '__main__':
    print(BinaryToQuinary().toQuinary(1111011))
