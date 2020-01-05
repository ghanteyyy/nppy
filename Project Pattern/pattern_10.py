def pattern_ten(strings):
    '''Pattern ten

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

    for x in range(1, len(strings) + 1):
        string = ' '.join(strings[:x])
        print(string.rjust((len(strings) * 2) - 1))


if __name__ == '__main__':
    try:
        pattern_ten('KATHMANDU')

    except NameError:
        print('String or Integer was expected')
