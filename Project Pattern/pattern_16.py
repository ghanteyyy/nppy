def pattern_sixteen(steps):
    ''' Pattern Sixtenn

            9
            9 8
            9 8 7
            9 8 7 6
            9 8 7 6 5
            9 8 7 6 5 4
            9 8 7 6 5 4 3
            9 8 7 6 5 4 3 2
            9 8 7 6 5 4 3 2 1 '''

    get_range = [str(i) for i in range(1, steps + 1)][::-1]  # Getting range of number in string and reverse it

    for gr in range(1, len(get_range) + 1):
        join = ' '.join(get_range[:gr])  # Slicing values
        print(join)


if __name__ == '__main__':
    try:
        pattern_sixteen(9)

    except NameError:
        print('Integer was expected')
