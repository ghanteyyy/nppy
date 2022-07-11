import string
import random


class RandomPasswordGenerator:
    '''Generate Random Password'''

    def __init__(self, length=8):
        self.length = length
        self.strings = string.printable[:62]
        self.len_strings = len(self.strings) - 1

    def method_one(self):
        '''Using random.randint for getting random indexes of self.strings and slicing using that indexes'''

        password = ''

        for _ in range(self.length):
            random_index = random.randint(0, self.len_strings)
            password += self.strings[random_index]

        return password

    def method_two(self):
        '''Using random.choice for getting the random letter from self.strings and joining them'''

        password = ''

        for _ in range(self.length):
            random_word = random.choice(self.strings)
            password += random_word

        return password

    def method_three(self):
        '''Using List Comprehension at method_one'''

        password = [self.strings[random.randint(0, self.len_strings)] for _ in range(self.length)]

        return ''.join(password)

    def method_four(self):
        '''Using List Comprehension at method_two'''

        password = [random.choice(self.strings) for _ in range(self.length)]

        return ''.join(password)


if __name__ == '__main__':
    random_password = RandomPasswordGenerator()

    print('Method One')
    print(random_password.method_one())

    print('\nMethod Two')
    print(random_password.method_two())

    print('\nMethod Three')
    print(random_password.method_three())

    print('\nMethod Four')
    print(random_password.method_four())
