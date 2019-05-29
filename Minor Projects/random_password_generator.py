import string
import random


def random_password(length_of_password):
    '''Generate random password of given length'''

    try:
        password = ''

        for number in range(length_of_password):
            random_number = random.randint(0, 61)  # Getting random number
            password += string.printable[random_number]  # Slicing letter with random number

        print(password)

    except (ValueError, NameError):
        print('String value was expected')

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    random_password(10)
