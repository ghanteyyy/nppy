def pattern_six(strings, steps):
    '''Pattern six

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
    '''

    if not str(strings).isalpha():
        strings = str(strings)

    for i in range(1, steps + 1):
        multiplying_strings = strings * i  # Multiplying the given string with 'i' to get the same character
        joining_strings = ' '.join(multiplying_strings).center(steps * 4)  # Joining the multiplied character 'a' with spaces and placing them to the center
        print(joining_strings.rstrip())   # Stripping spaces of right side


if __name__ == '__main__':
    try:
        pattern_six('*', 10)

    except NameError:
        print('String and Integer was expected')
