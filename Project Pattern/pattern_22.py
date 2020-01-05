def pattern_twenty_two(string):
    ''' Pattern twenty_two

              ***
             *   *
             *   *
             *****
             *   *
             *   *
             *   *
    '''

    for i in range(7):
        if i == 0:
            print('{0}'.format(string * 3))

        elif i == 3:
            print('{}'.format(string * 5))

        else:
            print('{0}   {0}'.format(string))


if __name__ == '__main__':
    pattern_twenty_two('*')
