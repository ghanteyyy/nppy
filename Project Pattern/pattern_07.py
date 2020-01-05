def pattern_seven(strings, steps):
    '''Pattern seven

           *
             * *
               * * *
                 * * * *
                   * * * * *
                     * * * * * *
                       * * * * * * *
                         * * * * * * * *
                           * * * * * * * * *
                             * * * * * * * * * *
                               * * * * * * * * * * *
                                 * * * * * * * * * * * *
                                   * * * * * * * * * * * * *
                                     * * * * * * * * * * * * * *
    '''

    if not str(strings).isalpha():
        strings = str(strings)

    for i in range(1, steps):
        multiplying_word = strings * i
        joining_word = ' '.join(multiplying_word)
        print(joining_word.center(len(joining_word) * 2).rstrip(' '))


if __name__ == '__main__':
    try:
        pattern_seven('*', 10)

    except NameError:
        print('String and Integer was expected')
