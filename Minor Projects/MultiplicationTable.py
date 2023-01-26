class MultiplicationTable:
    '''
    Prints the multiplication table of a given number till given upto
    '''

    def __init__(self, number=9, upto=20):
        self.upto = upto
        self.number = number

    def get_multiples(self):
        '''
        Printing the multiplication table
        '''

        for num in range(1, self.upto + 1):
            print(f'{self.number} x {num} = {self.number * num}')


if __name__ == '__main__':
    multiples = MultiplicationTable()
    multiples.get_multiples()
