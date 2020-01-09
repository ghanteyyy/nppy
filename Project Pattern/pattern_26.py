def pattern_twenty_six(string):
    '''Pattern twenty_six

          ***
         *   *
         *
         * ***
         *   *
         *   *
          ***
    '''

    for i in range(7):
        if i in [0, 6]:
            print(' {}'.format(string * 3))

        elif i in [1, 4, 5]:
            print('{0}   {0}'.format(string))

        elif i == 3:
            print('{} {}'.format(string, string * 3))

        else:
            print(string)


if __name__ == '__main__':
    pattern_twenty_six('*')
