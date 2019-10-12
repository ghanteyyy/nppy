def pattern_twenty_two(string):
    ''' Pattern twenty_one

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
            print('{0}'.format(string * 3).center(20))

        elif i == 3:
            print('{}'.format(string * 5).center(20))

        else:
            print('{0}   {0}'.format(string).center(20))


if __name__ == '__main__':
    pattern_twenty_two('*')
