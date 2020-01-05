def pattern_twenty_eight(string):
    '''Pattern twenty_eight

          *       *
          *       *
          * *   * *
          *   *   *
          *       *
          *       *
          *       *
    '''

    for i in range(7):
        if i in [0, 1, 4, 5, 6]:
            print('{0}       {0}'.format(string))

        elif i == 2:
            print('{0} {0}   {0} {0}'.format(string))

        else:
            print('{0}   {0}   {0}'.format(string))


if __name__ == '__main__':
    pattern_twenty_eight('*')
