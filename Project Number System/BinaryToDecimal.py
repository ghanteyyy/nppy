class BinaryToDecimal:
    '''
    Convert binary number to decimal number

    To convert binary to decimal you need to:
        Multiply each number by base 2 with its own power increase from left to right(first power is 0)
            1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                    = 123

        Required decimal number is 123
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

    def toDecimal(self, binary_number):
        '''
        Converting the given binary number to decimal
        '''

        if self.IsBinary(binary_number):
            decimal_number = 0
            reversed_binary = str(binary_number)[::-1]

            # Converting to decimal
            for bin_num in range(len(str(binary_number))):
                decimal_number += int(reversed_binary[bin_num]) * 2 ** bin_num

            return int(decimal_number)

        else:
            raise ValueError('Invalid Binary Number')


if __name__ == '__main__':
    print(BinaryToDecimal().toDecimal(1111011))
