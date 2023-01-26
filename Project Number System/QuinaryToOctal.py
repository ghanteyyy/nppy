class QuinaryToOctal:
    '''
    Convert quinary number to octal number

        You can convert quinary number to octal, first by converting quinary
        number to decimal and obtained decimal number to quinary number

        For an instance, lets take binary number be 123
            Step 1: Convert to decimal
                    123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                        = 38 (Decimal)

            Step 2: Convert to octal from the obtained decimal
                                8 | 38 | 6
                                  -----
                                    4

                    And our required octal number is 46 (taken in a reverse way)
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

    def toOctal(self, quinary_number):
        '''
        Converting the given quinary number to octal
        '''

        if self.IsQuinary(quinary_number):
            octal_number = ''
            decimal_number = 0

            for index, value in enumerate(str(quinary_number)[::-1]):
                decimal_number += int(value) * 5 ** index

            while decimal_number > 0:
                octal_number += str(decimal_number % 8)
                decimal_number = decimal_number // 8

            return octal_number[::-1]

        else:
            raise ValueError('Invalid Quinary Number')


if __name__ == '__main__':
    print(QuinaryToOctal().toOctal(123))
