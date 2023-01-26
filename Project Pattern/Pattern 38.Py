class Pattern_Thirty_Eight:
    '''
             1
            1 2
           1   3
          1     4
         1 2 3 4 5
    '''

    def __init__(self):
        num = '12345'

        for i in range(5):
            if i in range(1, 4):
                space = ' ' * (2 * i - 1)
                temp = num[:i + 1]

                output = space.join(temp[0] + temp[-1])
                print(output.center(30))

            elif i == 4:
                output = ' '.join(num)
                print(output.center(30))

            else:
                print('1'.center(30))


if __name__ == '__main__':
    Pattern_Thirty_Eight()
