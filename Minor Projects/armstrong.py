def armstrong(integer):
    '''Check if given integer is armstrong or not

        Armstrong series is the series obtained by adding the cube of each integer in the given number.
            Example: 153 can be obtained by 1 ** 3 + 5 ** 3 + 3 ** 3 '''

    def method_one():
        convert_to_string = str(integer)

        if convert_to_string.isdigit():
            sum_of_cube = 0

            for x in convert_to_string:   # Looping to each value stored in 'b' variable
                sum_of_cube += int(x) ** 3   # Converting 'x' to integer value and Cubing 'x' and adding each cube value to sum_of_cube variable

            if int(convert_to_string) == sum_of_cube:   # Checking if the value stored in sum_of_cube variable is equal to the value a
                print('{} is armstrong'.format(convert_to_string))  # Then printing its armstrong

            else:
                print('{} is not armstrong'.format(convert_to_string))   # Then printing its not armstrong

        else:
            print('Please input valid integer')

    def method_two():
        sum_of_cube = sum([int(x) ** 3 for x in str(integer)])

        if integer == sum_of_cube:
            print('{} is armstrong'.format(str(integer)))

        else:
            print('{} is not armstrong'.format(str(integer)))

    print('Method One')
    method_one()

    print('\nMethod Two')
    method_two()


if __name__ == '__main__':
    try:
        armstrong(153)

    except (ValueError, NameError):
        print('Integer value was expected')
