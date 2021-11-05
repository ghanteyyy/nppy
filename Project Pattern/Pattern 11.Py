class Pattern_Elevan:
    '''Pattern elevan

        K A T H M A N D U
        A T H M A N D U
        T H M A N D U
        H M A N D U
        M A N D U
        A N D U
        N D U
        D U
        U
    '''

    def __init__(self, strings='KATHMANDU'):
        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

        self.length = len(self.strings)

    def method_one(self):
        print('Method One')

        for x in range(self.length):
            get_string = ' '.join(self.strings[x:])
            print(get_string)

    def method_two(self):
        print('\nMethod Two')

        x = 0

        while x != self.length:
            get_string = ' '.join(self.strings[x:])
            print(get_string)

            x += 1


if __name__ == '__main__':
    pattern_elevan = Pattern_Elevan()

    pattern_elevan.method_one()
    pattern_elevan.method_two()
