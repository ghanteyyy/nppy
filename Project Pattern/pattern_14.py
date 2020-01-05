def pattern_fourteen(strings):
    '''Pattern fourteen

            K
             A
              T
               H
                M
                 A
                  N
                   D
                    U
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    def method_one(strings):
        for x in range(len(strings)):
            print('{}{}'.format(' ' * x, strings[x]))

    def method_two(strings):
        for x in range(len(strings)):
            print(strings[x].rjust(x + 1))

    print('Method One\n')
    method_one(strings)

    print('\n\nMethod Two\n')
    method_two(strings)


if __name__ == '__main__':
    try:
        pattern_fourteen('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
