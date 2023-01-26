class Pattern_Twenty_Four:
    '''
        *****
        *
        *
        ****
        *
        *
        *****
     '''

    def __init__(self, strings='*'):
        if not isinstance(strings, str):
            strings = str(strings)

        for i in range(7):
            if i in [0, 3, 6]:
                print(f'{strings * 5}')

            else:
                print(strings)


if __name__ == '__main__':
    Pattern_Twenty_Four()
