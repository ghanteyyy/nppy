class Pattern_Thirty:
    '''
         ****
         *   *
         *   *
         ****
         *
         *
         *
    '''

    def __init__(self, strings='*'):
        for i in range(7):
            if i in [0, 3]:
                print(f'{strings * 4}')

            elif i in [1, 2]:
                print(f'{strings}   {strings}')

            else:
                print(strings)


if __name__ == '__main__':
    Pattern_Thirty()
