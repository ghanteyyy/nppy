class Pattern_Thirty_Four:
    '''
             *
            * *
           * * *
          * * * *
         * * * * *
        * * * * * *
        * * * * * *
        * * * * * *
         * * * * *
          * * * *
           * * *
            * *
             *
    '''

    def __init__(self, strings='*', steps=6):
        self.steps = 6

        if isinstance(strings, str):
            self.strings = strings

        else:
            self.strings = str(strings)

        self._loop(1, steps + 1, 1)
        self._loop(steps + 1, 0, -1)

    def _loop(self, start, end, jump):
        for i in range(start, end, jump):
            multiplying_strings = self.strings * i  # Multiplying the given string with 'i' to get the same character
            joining_strings = ' '.join(multiplying_strings).center(self.steps * 4)  # Joining the multiplied character 'a' with spaces and placing them to the center
            print(joining_strings.rstrip())   # Stripping spaces of right side


if __name__ == '__main__':
    Pattern_Thirty_Four()
