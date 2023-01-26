class Pattern_Twenty_Seven:
    '''
         *
         *
         *
         *
         *
         *
         *****
    '''

    def __init__(self, strings='*', steps=10):
        strings = str(strings)

        for i in range(1, steps + 1):
            if i == steps:
                print(strings * steps)

            else:
                print(strings)


if __name__ == '__main__':
    Pattern_Twenty_Seven()
