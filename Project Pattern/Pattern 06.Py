class Pattern_Six:
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
          * * * * * * * * * *
    '''

    def __init__(self, strings='*', steps=10):
        self.steps = steps

        if isinstance(strings, str):
            self.strings = strings

        else:  # If provided 'strings' is integer then converting it to string
            self.strings = str(strings)

    def method_one(self):
        print('Method One')

        for i in range(1, self.steps + 1):
            joining_strings = ' '.join(self.strings * i).center(self.steps * 4)  # Joining the multiplied character 'a' with spaces and placing them to the center
            print(joining_strings.rstrip())   # Stripping spaces of right side

    def method_two(self):
        print('\nMethod Two')

        i = 1

        while i != self.steps + 1:
            joining_strings = ' '.join(self.strings * i).center(self.steps * 4)  # Joining the multiplied character 'a' with spaces and placing them to the center
            print(joining_strings.rstrip())   # Stripping spaces of right side

            i += 1


if __name__ == '__main__':
    pattern_six = Pattern_Six()

    pattern_six.method_one()
    pattern_six.method_two()
