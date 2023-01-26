class Pattern_Twenty_Six:
    '''
          ***
         *   *
         *
         * ***
         *   *
         *   *
          ***
    '''

    def __init__(self, strings='*'):
        if not isinstance(strings, str):
            strings = str(strings)

        for i in range(7):
            if i in [0, 6]:
                print(f' {strings * 3}')

            elif i in [1, 4, 5]:
                print(f'{strings}   {strings}')

            elif i == 3:
                print(f'{strings} {strings * 3}')

            else:
                print(strings)


if __name__ == '__main__':
    Pattern_Twenty_Six()
