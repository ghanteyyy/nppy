def octal_to_decimal(octal_number):
    '''Convert octal number to decimal number

        To convert octal to decimal you need to:
            Multipy each number by base 8 with its own power increase from left to right(first power is 0)
                123 = 1 * 8^2 + 2 * 8^1 + 3 * 8^0
                    =  83 '''

    def is_octal():
        global check

        count = 0

        for oct_num in str(octal_number):
            if int(oct_num) >= 8:
                count += 1

        if count == 0:
            return True

        else:
            return False

    if is_octal():
        decimal = 0
        reversed_octal = str(octal_number)[::-1]

        for x in range(len(reversed_octal)):
            decimal += int(reversed_octal[x]) * 8 ** x

        print(decimal)

    else:
        print('Invalid octal number')


if __name__ == '__main__':
    try:
        octal_to_decimal(123)

    except (ValueError, NameError):
        print('Integers was expected')
