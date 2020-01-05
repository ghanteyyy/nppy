def pattern_fifteen(steps):
    ''' Pattern fifteen

            1
            1 2
            1 2 3
            1 2 3 4
            1 2 3 4 5
            1 2 3 4 5 6
            1 2 3 4 5 6 7
            1 2 3 4 5 6 7 8
            1 2 3 4 5 6 7 8 9
    '''

    get_range = [str(i) for i in range(1, steps + 1)]   # Getting range of number in string

    for i in range(1, len(get_range)):
        join = ' '.join(get_range[:i])   # Slicing value and joining them with spaces between them
        print(join)


if __name__ == '__main__':
    try:
        pattern_fifteen(10)

    except NameError:
        print('Integer was expected')
