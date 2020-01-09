def pattern_twenty_five(string):
    '''Pattern twenty_five

         ****
         *   *
         *   *
         *   *
         *   *
         *   *
         ****
    '''

    for i in range(7):
        if i in [0, 6]:
            print('{}'.format(string * 4))

        else:
            print('{0}   {0}'.format(string))


if __name__ == '__main__':
    pattern_twenty_five('*')
