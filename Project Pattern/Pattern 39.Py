class Pattern_Thirty_Nine:
    '''
                1
              2 3 2
            3 4 5 4 3
          4 5 6 7 6 5 4
        5 6 7 8 9 8 7 6 5
    '''

    def __init__(self):
        num = '123456789'

        for i in range(5):
            if i == 0:
                print('1'.center(30))

            else:
                temp = num[i: i * 2 + 1]
                output = temp + temp[:i][::-1]
                print(' '.join(output).center(30))


if __name__ == '__main__':
    Pattern_Thirty_Nine()
