class Pattern_Thirty_One:
    '''
         ****
         *   *
         *   *
         ****
         * *
         *  *
         *   *
    '''

    def __init__(self, strings='*'):
        if not isinstance(strings, str):
            strings = str(strings)
        j = 1

        for i in range(7):
            if i in [0, 3]:
                print(f'{strings * 4}')

            elif i in [1, 2]:
                print(f'{strings}   {strings}')

            elif i in range(4, 7):
                print(f'{strings}{" " * j}{strings}')
                j += 1


if __name__ == '__main__':
    Pattern_Thirty_One()
