class BinaryToHexadecimal:
    def IsBinary(self, binary_number):
        '''Check if the given number is binary'''

        while binary_number > 0:
            remainder = binary_number % 10
            binary_number //= 10

            if remainder not in [0, 1]:
                return False

        return True

    def toHexaDecimal(self, binary_number):
        '''Convert binary number to hexadecimal number

            Binary number = 1111011

            To convert it to hexadecimal number:
                Step 1: Split each four value from backward like
                        111                         1011

                Step 2: Here, in first part the length is less than 4 so adding extra 0 at its front and 111 becomes 0111
                Step 3: Now using 8,4,2,1 rule in each splitted value so,
                            First,
                                0111 = 0 * 8 + 1 * 4 + 1 * 2 + 1 * 1
                                    = 7

                            Second,
                                1011 = 1 * 8 + 0 * 4 + 1 * 2 + 1 * 1
                                    = 11 (B)

                                    In Hexadecimal,
                                        10 = A
                                        11 = B
                                        12 = C
                                        13 = D
                                        14 = E
                                        15 = F

                Step 4: Append each value from first, second, and third which becomes to 7B
                Required hexadecimal number is 7B'''

        if self.IsBinary(binary_number):
            rule = [8, 4, 2, 1]
            tempHexadecimal = 0
            binary_number = str(binary_number)[::-1]
            hexa_decimal_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}

            listed_value = []
            hexadecimal_number = ''

            for i in range(len(binary_number) // 4 + 1):
                '''
                    Here, len(binary_number) = 8
                        Then, len(binary_number) // 4 + 1 = 2 + 1 = 4
                        So, range = (0, 1, 2, 3)'''

                sliced_binary = binary_number[:4]  # Storing three value from binary_number in each itreation
                binary_number = binary_number[4:]  # Overwriting binary_number variable excluding value stored in sliced_binary using slicing

                if len(sliced_binary) == 4:  # Checking if the length of value stored in sliced_binary variable
                    listed_value.append(sliced_binary[::-1])  # Then, appending listed_value list by reversing value stored in sliced_binary

                else:
                    listed_value.append(sliced_binary[::-1].zfill(4))
                    ''' If length of sliced_binary is less than 4 then:
                            1. First, reversing value of sliced_binary
                            2. Filling 0 to make three character value
                            3. At last we get, 01 whose length is less
                               than 4 then we reverse it so we get 10
                               and we fill that value '10' with '0'
                               using zfill(3) '010' so that the length
                               becomes 4'''

            listed_value = listed_value[::-1]  # Reversing the value of listed_value "list"

            for l in listed_value:  # looping to each value in listed_value list
                for x in range(len(l)):  # Then we get range value (0,1,2, 3) which is stored in temporary variable 'x' in each iteration. Here, range is generator (python 2.7)
                    tempHexadecimal += int(l[x]) * rule[x]  # Here, first slicing value from 'l' and rule with the value 'x' and converting value got from 'l' by slicing into integer

                if tempHexadecimal > 9:
                    tempHexadecimal = hexa_decimal_value[str(tempHexadecimal)]

                hexadecimal_number += str(tempHexadecimal)  # Converting integer value stored in tempHexadecimal to string and appending it to hexadecimal_number variable
                tempHexadecimal = 0  # Overwriting tempHexadecimal variable to '0' again

            return hexadecimal_number.strip('0')

        else:
            raise ValueError('Invalid Binary Number')

    def AlternativeMethod(self, binary_number):
        '''
            First, convert binary number i.e 1111011 to decimal by:
                1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                        = 123

            Second, convert obtained decimal number (319) to hexadecimal by:
                =  16| 123 |11 (B)  >>> Remainder
                      -----
                        7           >>> Remainder

                Write remainder going from down to up i.e 7B

                Required hexadecimal is 7B'''

        def BinaryToDecimal(binary_number):
            decimal_number = 0
            reversed_binary_number = str(binary_number)[::-1]

            for i in range(len(str(binary_number))):
                decimal = int(reversed_binary_number[i]) * 2 ** i
                decimal_number += decimal

            return decimal_number

        def toHexaDecimal():
            if self.IsBinary(binary_number):
                hexadecimal = ''
                decimal_number = BinaryToDecimal(binary_number)
                hexa_decimal_value = {'10': 'A', '11': 'B', '12': 'C', '13': 'D', '14': 'E', '15': 'F'}

                while int(decimal_number) > 0:
                    tempHexadecimal = int(decimal_number) % 16

                    if tempHexadecimal > 9:
                        hexadecimal += hexa_decimal_value[str(tempHexadecimal)]

                    else:
                        hexadecimal += str(tempHexadecimal)

                    decimal_number = int(decimal_number) // 16

                return hexadecimal[::-1]

            else:
                raise ValueError('Invalid Binary Number')

        return toHexaDecimal()


if __name__ == '__main__':
    print(BinaryToHexadecimal().toHexaDecimal(1111011))
    print(BinaryToHexadecimal().AlternativeMethod(1111011))
