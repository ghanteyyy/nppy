def pattern_twenty_three(string):
    '''Pattern twenty_three

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

    for i in range(15):
        if i == 0:
            print(' {}'.format(string * 17))

        elif i in [3, 4, 5]:
            print('{}'.format(string * 4))

        elif i in [9, 10, 11]:
            print('{}'.format(string * 4).rjust(17))

        elif i in [1, 2, 6, 7, 8, 12, 13, 14]:
            print('{}'.format(string * 17))


if __name__ == '__main__':
    pattern_twenty_three('o')
