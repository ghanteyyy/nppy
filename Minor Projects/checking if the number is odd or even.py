def odd_or_even(number):
    '''Check if the number is odd or even'''

    try:
        if number % 2 == 0:  # Checking if the remainder got by dividing with 2 is equal to ZERO
            print('{} is even'.format(number))   # If that is equal to ZERO then printing then even

        else:
            print('{} is odd'.format(number))   # If that's not the case then printing odd

    except (ValueError, NameError):
        print('Integer value was expected')


if __name__ == '__main__':
    odd_or_even(9)
