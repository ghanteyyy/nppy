def pattern_thirty_one(string, steps):
    '''Pattern thirty_two

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

    for i in range(1, int(steps // 2) - 2):
        print(f'{string} ' * i)

    for j in range(1, int(steps // 2)):
        print(f'{string} ' * j)

    for k in range(1, 4):
        print(f'{string} ')


if __name__ == '__main__':
    pattern_thirty_one('|||||', 20)
