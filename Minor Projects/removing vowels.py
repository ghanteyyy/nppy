class Remove_Vowels:
    '''Remove vowels from the word given by the user'''

    def __init__(self, strings):
        self.strings = strings.lower()
        self.vowels = ['a', 'e', 'i', 'o', 'u']

    def method_one(self):
        '''Using for loop'''

        words_removed_vowels = ''

        for string in self.strings:
            if string not in self.vowels:
                words_removed_vowels += string

        return words_removed_vowels

    def method_two(self):
        '''Using list comphrension'''

        words_removed_vowels = [string for string in self.strings if string not in self.vowels]

        return ''.join(words_removed_vowels)


if __name__ == '__main__':
    remove_vowels = Remove_Vowels('The quick brown fox jumps over the lazy dog')

    print('Method One')
    print(remove_vowels.method_one())

    print('\nMethod Two')
    print(remove_vowels.method_two())
