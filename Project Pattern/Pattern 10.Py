class Pattern_Ten:
    '''
                        K
                      K A
                    K A T
                  K A T H
                K A T H M
              K A T H M A
            K A T H M A N
          K A T H M A N D
        K A T H M A N D U
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('Method One')

        for x in range(1, self.length + 1):
            string = ' '.join(self.strings[:x])
            print(string.rjust((self.length * 2) - 1))

    def method_two(self):
        print('\nMethod Two')

        x = 1

        while x != self.length + 1:
            string = ' '.join(self.strings[:x])
            print(string.rjust((self.length * 2) - 1))

            x += 1


if __name__ == '__main__':
    pattern_ten = Pattern_Ten()

    pattern_ten.method_one()
    pattern_ten.method_two()
