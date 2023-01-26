class Pattern_Twenty_Five:
    '''
         ****
         *   *
         *   *
         *   *
         *   *
         *   *
         ****
    '''

    def __init__(self, strings='*'):
        if not isinstance(strings, str):
            strings = str(strings)

        for i in range(7):
            if i in [0, 6]:
                print(f'{strings * 4}')

            else:
                print(f'{strings}   {strings}')


if __name__ == '__main__':
    Pattern_Twenty_Five()
