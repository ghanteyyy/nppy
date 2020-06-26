def add_number(numbers):
    '''Add given number in series

    If user inputs 123456789 then the scripts adds all the numbers.
          = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9
          = 45    '''

    def method_one(numbers):
        Sum = 0
        lists = []   # Empty list
        number = str(numbers)

        for num in number:    # Looping for each value stored in number variable to temporaily variable num
            integer_value = int(num)      # Converting string value (num is in string type) to integer value
            lists.append(integer_value)   # And appending that integer value 'n' to the empty list "lists"

        for adding in lists:  # Looping to each value in lists
            Sum += adding     # Adding that each value

        print('The sum of {} is {}'.format(number, Sum))

    def method_two(numbers):
        sums = sum([int(num) for num in str(numbers)])

        print('Sum of {} is {}'.format(numbers, sums))

    print('Method One')
    method_one(123)

    print('\nMethod Two')
    method_two(123)


if __name__ == '__main__':
    try:
        add_number(123)

    except (ValueError, NameError):
        print('Integer value was expected')
