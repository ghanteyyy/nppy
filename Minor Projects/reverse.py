class Reverse:
    def __init__(self, strings):
        self.strings = strings
        self.length = len(self.strings) - 1

    def method_one(self):
        '''Using for loop'''

        reverse = ''

        for i in range(self.length, -1, -1):
            reverse += self.strings[i]

        return reverse

    def method_two(self):
        '''Using while loop'''

        reverse = ''
        length = self.length

        while length >= 0:
            reverse += self.strings[length]
            length -= 1

        return reverse

    def method_three(self):
        '''Using slicing method'''

        return self.strings[::-1]

    def method_four(self):
        '''Using built-in function reversed'''

        reverse = reversed(self.strings)

        return ''.join(reverse)

    def method_five(self):
        '''Using in-place algorithm

           Defination:
                In-place means that the algorithm does not use extra space for
                manipulating the input but may require a small though nonconstant
                extra space for its operation.'''

        strings = list(self.strings)

        for i in range((self.length + 1) // 2):
            strings[i], strings[self.length - i] = strings[self.length - i], strings[i]

        return ''.join(strings)

    def method_six(self):
        '''List Comphrension of method one'''

        reverse = [self.strings[i] for i in range(self.length, -1, -1)]

        return ''.join(reverse)


if __name__ == '__main__':
    reverse = Reverse('PYTHON')

    print('\nMethod One')
    print(reverse.method_one())

    print('\nMethod Two')
    print(reverse.method_two())

    print('\nMethod Three')
    print(reverse.method_three())

    print('\nMethod Four')
    print(reverse.method_four())

    print('\nMethod Five')
    print(reverse.method_five())

    print('\nMethod Six')
    print(reverse.method_six())
