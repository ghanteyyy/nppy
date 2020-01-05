def pattern_thirty(string):
    '''Pattern thirty
         ****
         *   *
         *   *
         ****
         *
         *
         *
    '''

    for i in range(7):
        if i in [0, 3]:
            print('{}'.format(string * 4))

        elif i in [1, 2]:
            print('{0}   {0}'.format(string))

        else:
            print(string)


if __name__ == '__main__':
    pattern_thirty('*')
