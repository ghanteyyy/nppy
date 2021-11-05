class Palindrome:
    '''Checks if your given string is palindrome or not

        Palindrome is a string / number which is same as reversing the orginal string / number
    '''

    def __init__(self, string):
        self.string = string.lower()

    def reverse_string(self):
        '''Reversing the given string

           See reverse.py to know other ways to reverse the given string'''

        return self.string[::-1]

    def is_palindrome(self):
        '''Checking if the given string is palindrome'''

        reversed_string = self.reverse_string()

        if self.string == reversed_string:
            print(f'{self.string} is palindrome')

        else:
            print(f'{self.string} is not palindrome')


if __name__ == '__main__':
    palin = Palindrome('mom')
    palin.is_palindrome()
