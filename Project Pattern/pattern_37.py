def pattern_thirty_seven():
    '''Pattern thirty_seven

        1 2 3 4 5
        2     5
        3   5
        4 5
        5
    '''

    num = '12345'

    for i in range(1, 6):
        if i == 1:
            print(' '.join(num))

        elif i in range(2, 5):
            space = -2 * i + 9  # using -2*n + 9 for getting required space where n = 1, 2, 3, .... and here n = i
            output = num[i - 1] + ' ' * space + '5'
            print(output)

        else:
            print('5')


if __name__ == '__main__':
    pattern_thirty_seven()
