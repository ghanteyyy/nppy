def pattern_eighten(steps):
    ''' Pattern Eighteen
            9 8 7 6 5 4 3 2 1
            9 8 7 6 5 4 3 2
            9 8 7 6 5 4 3
            9 8 7 6 5 4
            9 8 7 6 5
            9 8 7 6
            9 8 7
            9 8
            9 '''

    get_range = [str(i) for i in range(1, steps + 1)][::-1]

    for i in range(len(get_range), 0, -1):
        join = ' '.join(get_range[:i])
        print(join)


if __name__ == '__main__':
    try:
        pattern_eighten(9)

    except NameError:
        print('Integer was expected')
