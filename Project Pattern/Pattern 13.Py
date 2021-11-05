class Pattern_Thirteen:
    '''Pattern thirteen

        U
        D
        N
        A
        M
        H
        T
        A
        K
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('Method One')

        reversed_string = self.strings[::-1]  # If provided is integer then converting to string

        for x in range(len(reversed_string)):
            print(reversed_string[x])

    def method_two(self):
        print('\nMethod Two')

        reverse = self.strings[::-1]
        print('\n'.join(reverse))

    def method_three(self):
        print('\nMethod Three')

        x = self.length - 1

        while x != -1:
            print(self.strings[x])

            x -= 1

    def method_four(self):
        print('\nMethod Four')

        for x in range(self.length - 1, -1, -1):
            print(self.strings[x])

    def method_five(self):
        print('\nMethod Five')

        for x in range(1, self.length + 1):
            print(self.strings[-x])


if __name__ == '__main__':
    pattern_thirteen = Pattern_Thirteen()

    pattern_thirteen.method_one()
    pattern_thirteen.method_two()
    pattern_thirteen.method_three()
    pattern_thirteen.method_four()
    pattern_thirteen.method_five()
