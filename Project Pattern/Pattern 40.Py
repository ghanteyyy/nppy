class Pattern_Forty:
    '''
                     * * * * * * * * * *
                    * * * * * * * * *
                   * * * * * * * *
                  * * * * * * *
                 * * * * * *
                * * * * *
               * * * *
              * * *
             * *
            *
    '''

    def __init__(self, strings='*', steps=10):
        self.steps = steps

        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

    def method_one(self):
        print('Method One')

        for i in range(self.steps + 1, 0, -1):
            joining_word = ' '.join(self.strings * i)
            print(joining_word.center(len(joining_word) * 2).rstrip(' '))

    def method_two(self):
        print('\nMethod Two')

        steps = self.steps

        while steps:
            joining_word = ' '.join(self.strings * steps)
            print(joining_word.center(len(joining_word) * 2).rstrip(' '))

            steps -= 1


if __name__ == '__main__':
    pattern_forty = Pattern_Forty()

    pattern_forty.method_one()
    pattern_forty.method_two()
