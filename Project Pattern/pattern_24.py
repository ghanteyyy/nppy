def pattern_twenty_four(string):
    '''Pattern twenty_four
             *****
             *
             *
             ****
             *
             *
             *****
     '''

    for i in range(7):
        if i in [0, 3, 6]:
            print('{}'.format(string * 5))

        else:
            print(string)


if __name__ == '__main__':
    pattern_twenty_four('*')
