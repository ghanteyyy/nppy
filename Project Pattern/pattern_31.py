def pattern_thirty_one(string):
    '''Pattern thirty_one
         ****
         *   *
         *   *
         ****
         * *
         *  *
         *   *
    '''
    j = 1

    for i in range(7):
        if i in [0, 3]:
            print('{}'.format(string * 4))

        elif i in [1, 2]:
            print('{0}   {0}'.format(string))

        elif i in range(4, 7):
            print('{0}{1}{0}'.format(string, ' ' * j))
            j += 1


if __name__ == '__main__':
    pattern_thirty_one('*')
