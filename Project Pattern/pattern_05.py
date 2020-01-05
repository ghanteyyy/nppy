def pattern_five(strings):
    '''Pattern five

                K
               K A
              K A T
             K A T H
            K A T H M
           K A T H M A
          K A T H M A N
         K A T H M A N D
        K A T H M A N D U
    '''

    if not str(strings).isalpha():
        strings = str(strings)  # If provided is integer then converting to string

    for i in range(1, len(strings) + 1):
        slicing_string = ' '.join(strings[:i])
        getting_space = ' ' * (len(strings) - i)
        print('{}{}'.format(getting_space, slicing_string))


if __name__ == '__main__':
    try:
        pattern_five('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
