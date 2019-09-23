import string
import random


def random_password(length_of_password):
    '''Generate random password of given length'''

    try:
        password = ''

        for number in range(length_of_password):
            password += random.choice(string.ascii_letters + string.digits)

        print(password)

    except (ValueError, NameError):
        print('String value was expected')

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    random_password(10)
