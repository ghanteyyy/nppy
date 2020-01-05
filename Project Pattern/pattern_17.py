def pattern_seventeen(steps):
    ''' Pattern seventeen

                1 2 3 4 5 6 7 8 9
                1 2 3 4 5 6 7 8
                1 2 3 4 5 6 7
                1 2 3 4 5 6
                1 2 3 4 5
                1 2 3 4
                1 2 3
                1 2
                1
        '''

    get_range = [str(i) for i in range(1, steps + 1)]   # Getting range of number in string

    for gr in range(len(get_range), 0, -1):
        join = ' '.join(get_range[:gr])   # Slicing values and joining them with spaces
        print(join)


if __name__ == '__main__':
    try:
        pattern_seventeen(9)

    except NameError:
        print('Integer was expected')
