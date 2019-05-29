import collections


def count_letter(strings):
    '''Count number of character of a give word or sentence'''

    if not str(strings).isalpha():
        strings = str(strings)

    def method_one(strings):
        dic = {}

        for string in strings:       # Looping through each value in strings
            if string in dic:        # Checking if that value is in dictionary dic
                dic[string] += 1     # If character exists in dic then adding 1 to the value with respective character

            else:
                dic[string] = 1      # If character not exists in dic then giving 1 as value of that respective character

        for k, v in dic.items():     # Looping to each value of key and value in dictionary "dic"
            print('{} : {}'.format(k, v))     # Printing key and value

    def method_two(strings):
        count = collections.Counter(strings)

        for k, v in count.items():
            print('{} : {}'.format(k, v))

    print('Method One')
    method_one(strings)

    print('\nMethod Two')
    method_two(strings)


if __name__ == '__main__':
    try:
        count_letter('pneumonoultramicroscopicsilicovolcanoconiosis')

    except (ValueError, NameError):
        print('String value was expected')
