class Pattern_Twenty_Eight:
    '''
          *       *
          *       *
          * *   * *
          *   *   *
          *       *
          *       *
          *       *
    '''

    def __init__(self, strings='*'):
        if not isinstance(strings, str):
            strings = str(strings)

        for i in range(7):
            if i in [0, 1, 4, 5, 6]:
                print(f'{strings}       {strings}')

            elif i == 2:
                print(f'{strings} {strings}   {strings} {strings}')

            else:
                print(f'{strings}   {strings}   {strings}')


if __name__ == '__main__':
    Pattern_Twenty_Eight()
