def reverse(strings):
    '''Reversing the string'''

    try:
        if not str(strings).isalpha():  # If given value is interger
            strings = str(strings)

        def method_one(strings):
            reversing = ''

            for i in range(len(strings) - 1, -1, -1):
                reversing += strings[i]

            print(reversing)

        def method_two(strings):
            reverse_list = reversed(strings)
            join_reverse = ''.join(reverse_list)
            print(join_reverse)

            ''' Here, first reverse the given string with "reversed" function which returns list
               and joins the reversed list using "join" function.'''

        def method_three(strings):
            reversing = strings[::-1]
            print(reversing)

        print('Method One')
        method_one(strings)

        print('\nMethod Two')
        method_two(strings)

        print('\nMethod Three')
        method_three(strings)

    except (ValueError, NameError):
        print('String Value was expected')


if __name__ == '__main__':
    reverse('Python')
