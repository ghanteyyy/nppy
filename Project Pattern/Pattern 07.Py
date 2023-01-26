class Pattern_Seven:
    '''
        *
         * *
          * * *
           * * * *
            * * * * *
             * * * * * *
              * * * * * * *
               * * * * * * * *
                * * * * * * * * *
    '''

    def __init__(self, strings='*', steps=10):
        self.steps = steps

        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

    def method_one(self):
        print('Method One')

        for i in range(1, self.steps):
            joining_word = ' '.join(self.strings * i)
            print(joining_word.center(len(joining_word) * 2).rstrip(' '))

    def method_two(self):
        print('\nMethod Two')

        steps = 1

        while steps != self.steps:
            joining_word = ' '.join(self.strings * steps)
            print(joining_word.center(len(joining_word) * 2).rstrip(' '))

            steps += 1


if __name__ == '__main__':
    pattern_seven = Pattern_Seven()

    pattern_seven.method_one()
    pattern_seven.method_two()
