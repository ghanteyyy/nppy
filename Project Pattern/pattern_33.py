def pattern_thirty_three():
    '''Pattern thirty_three

        1       1
        12     21
        123   321
        1234 4321
        123454321
    '''

    num = '12345'

    for i in range(5):
        slice = num[0: i + 1]

        if i < 4:
            print(f'{slice.ljust(8 - i)}{slice[::-1]}')

        else:
            print(f'{slice.ljust(8 - i)}{slice[:-1][::-1]}')


if __name__ == '__main__':
    pattern_thirty_three()
