class JoinWord:
    '''
    Join your word with your joining keyword
        Example:
                word = PYTHON
                delimiter = -

                then you get
                    P-Y-T-H-O-N
    '''

    def __init__(self, string, delimiter):
        self.string = string
        self.delimiter = delimiter

    def method_one(self):
        '''
        Using for loop
        '''

        join_word = ""

        for x in range(len(self.string)):
            if x != len(self.string) - 1:
                join_word += self.string[x] + self.delimiter

            else:
                join_word += self.string[x]

        print(join_word)

    def method_two(self):
        '''
        Using built-in function "join"
        '''

        join = (self.delimiter).join(self.string)

        print(join)


if __name__ == "__main__":
    join = JoinWord('PYTHON', '-')

    print("Method One")
    join.method_one()

    print("\nMethod Two")
    join.method_two()
