def remove_vowels(strings):
    '''Remove vowels from the word given by the user'''

    try:
        if not str(strings).isalpha():  # If the given value is integer
            strings = str(strings)

        new_word = ''

        for letter in strings:
            if letter not in 'aeiou':
                new_word += letter  # Joining only consonant letters

        print(new_word)

    except (ValueError, NameError):
        print('String value was expected')


if __name__ == '__main__':
    remove_vowels('santosh')
