class add_series_of_numbers:
    '''Add given integer entered in series

        If user inputs 123456789 then the scripts adds all the integerbers.
              = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9
              = 45    '''

    def __init__(self, integer=123):
        self.integer = str(integer)

    def method_one(self):
        '''Using for loop while appending each integer in a list and adding each integer of a list to get sum'''

        sums = 0
        lists = []

        for integer in self.integer:
            lists.append(int(integer))

        for adding in lists:
            sums += adding

        return f'Sum of {self.integer} = {sums}'

    def method_two(self):
        '''Using for loop and getting the sum directly without appending to any list'''

        sums = 0

        for integer in self.integer:
            sums += int(integer)

        return f'Sum of {self.integer} = {sums}'

    def method_three(self):
        '''Using list comphrension'''

        sums = sum([int(integer) for integer in self.integer])

        return f'Sum of {self.integer} = {sums}'

    def method_four(self):
        '''Using for loop and built-in function : sum : to add those integers'''

        lists = []

        for integer in self.integer:
            lists.append(int(integer))

        sums = sum(lists)

        return f'Sum of {self.integer} = {sums}'


if __name__ == '__main__':
    add = add_series_of_numbers()

    print('\nMethod One')
    print(add.method_one(), end='\n\n')

    print('Method Two')
    print(add.method_two(), end='\n\n')

    print('Method Three')
    print(add.method_three(), end='\n\n')

    print('Method Four')
    print(add.method_four())
