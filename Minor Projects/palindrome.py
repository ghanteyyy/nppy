def palindrome(strings):
    '''Checks if your given string is palindrome or not

        Palindrome is a string / number which is same as reversing the orginal string / number
    '''

    try:
        if strings.lower() == strings[::-1].lower():   # Checking if original value is same as reversing it
            print('{} is palindrome'.format(strings))

        else:
            print('{} is not palindrome'.format(strings))

    except (ValueError, NameError):
        print('String value was expected')


if __name__ == '__main__':
    palindrome('mom')
