def pattern_twenty_seven(string):
    '''Pattern twenty_seven
         *
         *
         *
         *
         *
         *
         *****
    '''

    for i in range(7):
        if i == 6:
            print(string * 5)

        else:
            print(string)


if __name__ == '__main__':
    pattern_twenty_seven('*')
