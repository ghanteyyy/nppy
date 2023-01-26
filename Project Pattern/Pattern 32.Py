class Pattern_Thirty_Two:
    '''
            *
            * *
            * * *
            * * * *
            * * * * *
            * * * * * *
            * * * * * * *
            *
            * *
            * * *
            * * * *
            * * * * *
            * * * * * *
            * * * * * * *
            * * * * * * * *
            * * * * * * * * *
            *
            *
            *
    '''

    def __init__(self, strings='*', steps=20):
        for i in range(1, int(steps // 2) - 2):
            print(f'{strings} ' * i)

        for j in range(1, int(steps // 2)):
            print(f'{strings} ' * j)

        for k in range(1, 4):
            print(f'{strings} ')


if __name__ == '__main__':
    Pattern_Thirty_Two()
