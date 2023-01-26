class QuinaryToDecimal:
    '''
    Convert quinary number to decimal number

        You can convert quinary number to decimal by multiplying each quinary number with base of 5 with power starting from 0 increasing from left to right.
            For an instance, lets take quinary number be 123

                Step 1: Converting to decimal number
                        123 = 1 * 5^2 + 2 * 5^1 + 3 * 5^0
                            = 38

                    And our required quinary number is 38
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

    def toDecimal(self, quinary_number):
        '''
        Converting the given quinary number to decimal
        '''

        if self.IsQuinary(quinary_number):
            decimal_number = 0

            for power, num in enumerate(str(quinary_number)[::-1]):
                decimal_number += int(num) * 5 ** power

            return decimal_number

        else:
            return('Invalid Quinary Number')


if __name__ == '__main__':
    print(QuinaryToDecimal().toDecimal(123))
