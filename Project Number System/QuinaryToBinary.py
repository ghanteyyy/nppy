class QuinaryToBinary:
    '''
    Convert quinary number to binary number

        You can convert quinary number to binary, first by converting quinary
        number to decimal and obtained decimal to binary number

        For an instance, lets take quinary number be 123

            Step 1: Convert quinary number to decimal
                    123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                        = 38 (Decimal)

            Step 2: Convert obtained decimal number to binary
                            2 | 38 | 0
                              ------
                            2 | 19 | 1
                              ------
                            2 |  9 | 1
                              ------
                            2 |  4 | 0
                              ------
                            2 |  2 | 0
                              ------
                                1

                And our required binary number is 100110 (taken remainder in reverse way)
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

    def toBinary(self, quinary_number):
        '''
        Converting the given quinary number to binary
        '''

        if self.IsQuinary(quinary_number):
            binary_number = ''
            decimal_number = 0

            for index, value in enumerate(str(quinary_number)[::-1]):
                decimal_number += int(value) * 5 ** index

            while decimal_number > 0:
                binary_number += str(decimal_number % 2)
                decimal_number = decimal_number // 2

            return binary_number[::-1]

        else:
            raise ValueError('Invalid Binary Number')


if __name__ == '__main__':
    print(QuinaryToBinary().toBinary(123))
