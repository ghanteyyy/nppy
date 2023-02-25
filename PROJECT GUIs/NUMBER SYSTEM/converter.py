class NumberSystemConversion:
    def __init__(self, display_answer, PlayErrorAudio):
        self.display_answer = display_answer
        self.PlayErrorAudio = PlayErrorAudio
        self.hex_to_num = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
        self.num_to_hex = {v: k for k, v in self.hex_to_num.items()}

    def is_valid_number_system(self, nums, check, name):
        '''
        Check if the given number is valid with resect to the number system from converting
        '''

        check = [True if num in check else False for num in nums]

        if all(check):
            return True

        self.PlayErrorAudio()
        self.display_answer(f'Invalid {name} Number')

        return False

    def binary_to_decimal(self, binary_number):
        '''
        Convert binary number to decimal number

        1111011 = 1 * 2^6 + 1 * 2^5 + 1 * 2^4 + 1 * 2^3 + 0 * 2^2 + 1 * 2^1 + 1 * 2^0
                = 123
        '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = 0
            ReversedBinary = binary_number[::-1]
            BinaryLength = len(binary_number) - 1

            while BinaryLength != -1:
                decimal_num += int(ReversedBinary[BinaryLength]) * 2 ** BinaryLength
                BinaryLength -= 1

            return str(decimal_num)

    def binary_to_octal(self, binary_number):
        '''
        Convert binary number to octal number

        To convert binary to octal you need to:
            1. Convert binary number to decimal number via "self.binary_to_decimal" method
            2. Convert obtained decimal number from step 1 to octal via
               "decimal_to_octal" method
        '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = self.binary_to_decimal(binary_number)
            octal_num = self.decimal_to_octal(decimal_num)

            return str(octal_num)

    def binary_to_hexadecimal(self, binary_number):
        '''
        Convert binary number to hexadecimal number

        To convert binary to hexadecimal you need to:
            1. Convert binary number to decimal number via "self.binary_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to hexadecimal
               via "decimal_to_hexadecimal" method
        '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = self.binary_to_decimal(binary_number)
            decimal_to_hexadecimal = self.decimal_to_hexadecimal(decimal_num)

            return str(decimal_to_hexadecimal)

    def binary_to_quinary(self, binary_number):
        '''
        Convert binary number to quinary number

        To convert binary to quinary you need to:
            1. Convert binary number to decimal number via "self.binary_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to quinary via
               "decimal_to_quinary" method
        '''

        if self.is_valid_number_system(binary_number, '01', 'Binary'):
            decimal_num = self.binary_to_decimal(binary_number)
            quinary_num = self.decimal_to_quinary(decimal_num)

            return str(quinary_num)

    def decimal_to_binary(self, decimal_number):
        '''
        Convert decimal number to binary number

                2 | 123 | 1     >>> Remainder
                  -------
                2 | 61  | 1     >>> Remainder
                  -------
                2 | 30  | 0     >>> Remainder
                  -------
                2 | 15  | 1     >>> Remainder
                  -------
                2 |  7  | 1     >>> Remainder
                  -------
                2 |  3  | 1     >>> Remainder
                  -------
                     1

                And writing the remainder in reverse way i.e 1111011
        '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            binary_num = ''

            while decimal_num != 0:
                remainder = str(decimal_num % 2)
                binary_num += remainder
                decimal_num //= 2

            return str(binary_num[::-1])

    def decimal_to_octal(self, decimal_number):
        '''
        Convert decimal number to octal number

                8 | 123 | 3     >>> Remainder
                  -------
                8 |  15 | 7     >>> Remainder
                  -------
                     1          >>> Remainder

                 And writing the remainder in reverse way i.e 173
        '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            octal_num = ''

            while decimal_num != 0:
                remainder = str(decimal_num % 8)
                octal_num += remainder
                decimal_num //= 8

            return str(octal_num[::-1])

    def decimal_to_hexadecimal(self, decimal_number):
        '''
        Convert decimal number to hexadecimal number

                16| 123 | 11 (B)   >>> Remainder
                  -------
                    7              >>> Remainder

                And writing the remainder in reverse way i.e 7B
        '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            hexadecimal_num = ''

            while decimal_num != 0:
                remainder = decimal_num % 16

                if remainder >= 10:
                    hexadecimal_num += self.num_to_hex[remainder]

                else:
                    hexadecimal_num += str(remainder)

                decimal_num //= 16

            return str(hexadecimal_num[::-1])

    def decimal_to_quinary(self, decimal_number):
        '''
        Convert decimal number to quinary number

            To calculate decimal_number to quinary you need to:
                    5 | 123 | 3    >>> Remainder
                      -------
                    5 | 24  | 4    >>> Remainder
                      -------
                        4          >>> Remainder

                    And writing the remainder in reverse way i.e 443
        '''

        if self.is_valid_number_system(decimal_number, '0123456789', 'Decimal'):
            decimal_num = int(decimal_number)
            quinary_num = ''

            while decimal_num != 0:
                remainder = str(decimal_num % 5)
                quinary_num += remainder
                decimal_num //= 5

            return str(quinary_num[::-1])

    def octal_to_binary(self, octal_number):
        '''
        Convert octal number system to binary number system

        To convert octal to binary you need to:
            1. Convert octal number to decimal number via "self.octal_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to binary via
               "decimal_to_binary" method
        '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            octal_to_decimal = self.octal_to_decimal(octal_number)
            binary_num = self.decimal_to_binary(octal_to_decimal)

            return binary_num

    def octal_to_decimal(self, octal_number):
        '''
        Convert octal number to decimal number

            173 = 1 * 8^2 + 7 * 8^1 + 3 * 8^0
                = 123
        '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            decimal_num = 0
            ReversedOctal = octal_number[::-1]
            OctalLength = len(octal_number) - 1

            while OctalLength != -1:
                decimal_num += int(ReversedOctal[OctalLength]) * 8 ** OctalLength
                OctalLength -= 1

            return str(decimal_num)

    def octal_to_hexadecimal(self, octal_number):
        '''
        Convert octal number to hexadecimal number

        To convert octal to hexadecimal you need to:
            1. Convert octal number to decimal number via "self.octal_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to hexadecimal
               via "decimal_to_hexadecimal" method
        '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            decimal_num = self.octal_to_decimal(octal_number)
            hexadecimal_num = self.decimal_to_hexadecimal(decimal_num)

            return str(hexadecimal_num)

    def octal_to_quinary(self, octal_number):
        '''
        Convert octal number to quinary number

        To convert octal to quinary you need to:
            1. Convert octal number to decimal number via "self.octal_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to quinary via
               "decimal_to_quinary" method
        '''

        if self.is_valid_number_system(octal_number, '01234567', 'Octal'):
            decimal_num = self.octal_to_decimal(octal_number)
            quinary_num = self.decimal_to_quinary(decimal_num)

            return str(quinary_num)

    def hexadecimal_to_binary(self, hexadecimal_number):
        '''
        Convert hexadecimal number to binary number

           To convert hexadecimal to binary you need to:
                1. Convert hexadecimal number to decimal number via "self.hexadecimal_to_decimal" method
                2. Convert obtained decimal number obtained from step 1 to binary via
                   "decimal_to_binary" method
        '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = self.hexadecimal_to_decimal(hexadecimal_number)
            binary_num = self.decimal_to_binary(decimal_num)

            return str(binary_num)

    def hexadecimal_to_decimal(self, hexadecimal_number):
        '''
        Convert hexadecimal number to decimal number

            7B = 7 * 16^2 + 11 * 16^0       here B == 11
               = 123
        '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = 0
            ReversedHexaDecimal = hexadecimal_number[::-1]
            HexaDecimalLength = len(hexadecimal_number) - 1

            while HexaDecimalLength != -1:
                each_hexa = ReversedHexaDecimal[HexaDecimalLength]

                if each_hexa in self.hex_to_num:
                    each_hexa = self.hex_to_num[each_hexa]

                decimal_num += int(each_hexa) * 16 ** HexaDecimalLength
                HexaDecimalLength -= 1

            return str(decimal_num)

    def hexadecimal_to_octal(self, hexadecimal_number):
        '''
        Convert hexadecimal number to octal number

        To convert hexadecimal to octal you need to:
            1. Convert hexadecimal number to decimal number via "self.hexadecimal_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to octal via
               "decimal_to_octal" method
        '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = self.hexadecimal_to_decimal(hexadecimal_number)
            octal_num = self.decimal_to_octal(decimal_num)

            return str(octal_num)

    def hexadecimal_to_quinary(self, hexadecimal_number):
        '''
        Convert hexadecimal number to quinary number

        To convert hexadecimal to quinary you need to:
            1. Convert hexadecimal number to decimal number via "self.hexadecimal_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to quinary via
               "decimal_to_quinary" method
        '''

        if self.is_valid_number_system(hexadecimal_number, '0123456789ABCDEF', 'Hexadecimal'):
            decimal_num = self.hexadecimal_to_decimal(hexadecimal_number)
            quinary_num = self.decimal_to_quinary(decimal_num)

            return str(quinary_num)

    def quinary_to_binary(self, quinary_number):
        '''
        Convert quinary number to binary number

        To convert quinary to binary you need to:
            1. Convert quinary number to decimal number via "self.quinary_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to binary via
               "decimal_to_binary" method
        '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = self.quinary_to_decimal(quinary_number)
            binary_num = self.decimal_to_binary(decimal_num)

            return str(binary_num)

    def quinary_to_decimal(self, quinary_number):
        '''
        Convert quinary number to decimal number

            443 = 4 * 5^2 + 4 * 5^1 + 3 * 5^0
                = 123
        '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = 0
            ReversedQuinary = quinary_number[::-1]
            QuinaryLength = len(quinary_number) - 1

            while QuinaryLength != -1:
                decimal_num += int(ReversedQuinary[QuinaryLength]) * 5 ** QuinaryLength
                QuinaryLength -= 1

            return str(decimal_num)

    def quinary_to_octal(self, quinary_number):
        '''
        Convert quinary number to octal number

        To convert quinary to octal you need to:
            1. Convert quinary number to decimal number via "self.quinary_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to octal via
               "decimal_to_octal" method
        '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = self.quinary_to_decimal(quinary_number)
            octal_num = self.decimal_to_octal(decimal_num)

        return str(octal_num)

    def quinary_to_hexadecimal(self, quinary_number):
        '''
        Convert quinary number into hexadecimal number

        To convert quinary to hexadecimal you need to:
            1. Convert quinary number to decimal number via "self.quinary_to_decimal" method
            2. Convert obtained decimal number obtained from step 1 to hexadecimal
               via "decimal_to_hexadecimal" method
        '''

        if self.is_valid_number_system(quinary_number, '01234', 'Quinary'):
            decimal_num = self.quinary_to_decimal(quinary_number)
            hexadecimal_num = self.decimal_to_hexadecimal(decimal_num)

            return str(hexadecimal_num)
