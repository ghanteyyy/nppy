def BinaryToDecimal(binary_number):
    '''Convert binary number to decimal number

        To convert binary to decimal you need to:
            Multipy each number by base 2 with its own power increase from left to right(first power is 0)
                1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                       = 123

            Required decimal number is 123
    '''

    def is_binary():
        '''Check if the given number is binary'''
        count = 0

        for binn in str(binary_number):
            if int(binn) > 1:
                count += 1

        if count == 0:
            return True

        else:
            return False

    if is_binary():
        decimal_number = 0
        reversed_binary = str(binary_number)[::-1]

        # Converting to decimal
        for bin_num in range(len(str(binary_number))):
            decimal_number += int(reversed_binary[bin_num]) * 2 ** bin_num

        print(int(decimal_number))

    else:
        print('Invalid binary number')


if __name__ == '__main__':
    try:
        BinaryToDecimal(1111011)

    except (ValueError, NameError):
        print('Integers was expected')
