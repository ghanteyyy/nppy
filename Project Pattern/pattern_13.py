def pattern_thirteen(strings):
    '''Pattern thirteen

            U
            D
            N
            A
            M
            H
            T
            A
            K
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    def method_one(strings):
        reversed_string = str(strings)[::-1]  # If provided is integer then converting to string

        for x in range(len(reversed_string)):
            get_string = reversed_string[x]
            print(get_string)

    def method_two(strings):
        reverse = strings[::-1]
        join = '\n'.join(reverse)
        print(join)

    print('Method One')
    method_one(strings)

    print('\nMethod Two')
    method_two(strings)


if __name__ == '__main__':
    try:
        pattern_thirteen('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
