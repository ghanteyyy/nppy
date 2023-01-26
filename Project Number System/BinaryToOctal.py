class BinaryToOctal:
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

    def toOctal(self, binary_number):
        '''
        Convert binary number to octal number

            Binary number = 1111011

            To convert it to octal number:
                Step 1: Split each three value from backward like
                        1           111            011

                Step 2: Here, we have all splitted value having length 3 except one i.e 1 so adding extra two '0's in the front of 1
                        001 to make its length 3

                        Then finally we have,
                            001               111               011

                Step 3: Now using 4,2,1 rule so,
                            first,
                                001 = 0 * 4 + 0 * 2 + 1 * 1
                                    = 1
                            second,
                                111 = 1 * 4 + 1 * 2 + 1 * 1
                                    = 7
                            third,
                                011 = 0 * 4 + 1 * 2 + 1 * 1
                                    = 3

                Step 4: Append each value from first, second, and third which becomes to 173

                Required octal number is 173
        '''

        if self.IsBinary(binary_number):
            binary_number = str(binary_number)[::-1]

            tempOctal = 0
            OctalNumber = ''
            binaryGroup = []
            rule = [4, 2, 1]

            for i in range(len(binary_number) // 3 + 1):
                '''
                    Here, len(binary_number) = 8
                        Then, len(binary_number) // 3 + 1 = 2 + 1 = 3
                        So, range = (0, 1, 2)'''

                sliced_binary = binary_number[:3]
                binary_number = binary_number[3:]

                if len(sliced_binary) == 3:
                    binaryGroup.append(sliced_binary[::-1])

                else:
                    binaryGroup.append(sliced_binary[::-1].zfill(3))
                    '''
                    If length of sliced_binary is less than 3 then:
                        First, reversing value of sliced_binary
                        Second, filling 0 to make three character value

                        For instance,
                            At last we get, 01 whose length is less than 3 then we reverse it so we
                            get 10 and we fill that value '10' with '0' using zfill(3) '010' so that
                            the length becomes 3
                    '''

            binaryGroup = binaryGroup[::-1]

            for group in binaryGroup:
                for x in range(len(group)):
                    tempOctal += int(group[x]) * rule[x]

                OctalNumber += str(tempOctal)
                tempOctal = 0

            return int(OctalNumber.strip('0'))

        else:
            raise ValueError('Invalid Binary Number')

    def AlternativeMethod(self, binary_number):
        '''
        First, split binary number to between three digits like
                    001            111             011

        Second, use 4, 2, 1 rule to convert each splitted value to decimal number
            001 = 0 * 4 + 0 * 2 + 1 * 1
                = 1

            111 = 1 * 4 + 1 * 2 + 1 * 1
                = 7

            011 = 0 * 4 + 1 * 2 + 1 * 1
                = 3

        Hence, append all value and we get final result 173 (octal number)
        '''

        def BinaryToDecimal():
            decimal_number = 0
            reversed_binary_number = str(binary_number)[::-1]

            for i in range(len(str(binary_number))):
                decimal_number += int(reversed_binary_number[i]) * 2 ** i

            return decimal_number

        def DecimalToOctal():
            if self.IsBinary(binary_number):
                OctalNumber = ''
                DecimalNumber = BinaryToDecimal()

                while DecimalNumber > 0:
                    octal = DecimalNumber % 8
                    OctalNumber += str(octal)
                    DecimalNumber = DecimalNumber // 8

                return OctalNumber[::-1]

            else:
                raise ValueError('Invalid Binary Number')

        return DecimalToOctal()


if __name__ == '__main__':
    print(BinaryToOctal().toOctal(1111011))
    print(BinaryToOctal().AlternativeMethod(1111011))
