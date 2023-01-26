class Pattern_Twenty_Three:
    '''
         ooooooooooooooooo
        ooooooooooooooooo
        ooooooooooooooooo
        oooo
        oooo
        oooo
        ooooooooooooooooo
        ooooooooooooooooo
        ooooooooooooooooo
                     oooo
                     oooo
                     oooo
        ooooooooooooooooo
        ooooooooooooooooo
        ooooooooooooooooo
    '''

    def __init__(self, strings='o'):
        if not isinstance(strings, str):
            strings = str(strings)

        for i in range(15):
            if i == 0:
                print(f' {strings * 17}')

            elif i in [3, 4, 5]:
                print(f'{strings * 4}')

            elif i in [9, 10, 11]:
                print(f'{(strings * 4).rjust(17)}')

            elif i in [1, 2, 6, 7, 8, 12, 13, 14]:
                print(f'{strings * 17}')


if __name__ == '__main__':
    Pattern_Twenty_Three()
