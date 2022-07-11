class Pattern_Fourteen:
    '''Pattern fourteen

        K
         A
          T
           H
            M
             A
              N
               D
                U
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('\nMethod One')

        for x in range(self.length):
            print(f'{" " * x}{self.strings[x]}')

    def method_two(self):
        print('\nMethod Two')

        for x in range(self.length):
            print(self.strings[x].rjust(x + 1))

    def method_three(self):
        print('\nMethod Three')

        x = 0

        while x != self.length:
            print(f'{" " * x}{self.strings[x]}')

            x += 1

    def method_four(self):
        print('\nMethod Four')

        x = 0

        while x != self.length:
            print(self.strings[x].rjust(x + 1))

            x += 1


if __name__ == '__main__':
    pattern_fourteen = Pattern_Fourteen()

    pattern_fourteen.method_one()
    pattern_fourteen.method_two()
    pattern_fourteen.method_three()
    pattern_fourteen.method_four()
