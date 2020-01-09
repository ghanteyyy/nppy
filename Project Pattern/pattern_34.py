def pattern_thirty_four(strings, steps):
    '''Pattern thirty_four

             *
            * *
           * * *
          * * * *
         * * * * *
        * * * * * *
        * * * * * *
        * * * * * *
         * * * * *
          * * * *
           * * *
            * *
             *
    '''

    for i in range(1, steps + 1):
        multiplying_strings = strings * i  # Multiplying the given string with 'i' to get the same character
        joining_strings = ' '.join(multiplying_strings).center(steps * 4)  # Joining the multiplied character 'a' with spaces and placing them to the center
        print(joining_strings.rstrip())   # Stripping spaces of right side

    for i in range(steps + 1, 0, -1):
        multiplying_strings = strings * i  # Multiplying the given string with 'i' to get the same character
        joining_strings = ' '.join(multiplying_strings).center(steps * 4)  # Joining the multiplied character 'a' with spaces and placing them to the center
        print(joining_strings.rstrip())   # Stripping spaces of right side


if __name__ == '__main__':
    pattern_thirty_four('*', 6)
