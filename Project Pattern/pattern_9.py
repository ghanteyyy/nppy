def pattern_nine(strings):
    '''Pattern three

        If you input "KATHMANDU" then you get

                         K
                         A
                         T
                         H
                         M
                         A
                         N
                         D
                         U

        or SIMILAR
    '''

    def method_one(strings):
        if not str(strings).isalpha():
            strings = str(strings)

        for string in strings:
            print(string)

    def method_two(strings):
        join_word = '\n'.join(strings)
        print(join_word)

    print('Method One')
    method_one(strings)

    print('\nMethod Two')
    method_two(strings)


if __name__ == '__main__':
    try:
        pattern_nine('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
