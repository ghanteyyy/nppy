class Pattern_Twenty_Two:
    ''' 
              ***
             *   *
             *   *
             *****
             *   *
             *   *
             *   *
    '''

    def __init__(self, strings='*'):
        if not isinstance(strings, str):
            strings = str(strings)

        for i in range(7):
            if i == 0:
                print(f' {strings * 3}')

            elif i == 3:
                print(f'{strings * 5}')

            else:
                print(f'{strings}   {strings}')


if __name__ == '__main__':
    Pattern_Twenty_Two()
