class Armstrong():
    '''Check if given integer is armstrong or not

        Armstrong series is the series obtained by adding the cube of each integer in the given number.
            Example: 153 can be obtained by 1 ** 3 + 5 ** 3 + 3 ** 3 '''

    def __init__(self, integer=153):
        self.integer = str(integer)

    def method_one(self):
        '''Using for loop'''

        sum_of_cube = 0

        for x in self.integer:
            sum_of_cube += int(x) ** 3

        if int(self.integer) == sum_of_cube:
            return f'{self.integer} is armstrong\n'

        else:
            return f'{self.integer} is not armstrong\n'

    def method_two(self):
        '''Using list comprehension'''

        sum_of_cube = sum([int(x) ** 3 for x in str(self.integer)])

        if int(self.integer) == sum_of_cube:
            return f'{self.integer} is armstrong'

        else:
            return f'{self.integer} is not armstrong'


if __name__ == '__main__':
    armstrong = Armstrong()

    print('\nMethod One')
    print(armstrong.method_one())

    print('Method Two')
    print(armstrong.method_two())
