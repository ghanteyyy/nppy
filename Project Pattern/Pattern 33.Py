class Pattern_Thirty_Three:
    '''
        1       1
        12     21
        123   321
        1234 4321
        123454321
    '''

    def __init__(self):
        num = '12345'

        for i in range(5):
            sliced = num[:i + 1]

            if i < 4:
                print(f'{sliced.ljust(8 - i)}{sliced[::-1]}')

            else:
                print(f'{sliced.ljust(8 - i)}{sliced[:-1][::-1]}')


if __name__ == '__main__':
    Pattern_Thirty_Three()
