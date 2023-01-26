import collections


class CountLetter:
    def __init__(self, strings):
        self.strings = strings

    def method_one(self):
        '''
        Using for loop
        '''

        dic = {}

        for string in self.strings:
            if string in dic:
                dic[string] += 1     # If a character exists in dic then increasing its count by 1.

            else:
                dic[string] = 1      # Else assigning its count to 1.

        keys = [key for key in dic.keys()]   # Sorting keys of dic alphabetically so that we can print keys and values in order.
        keys.sort()

        for key in keys:
            print('{} : {}'.format(key, dic[key]))

    def method_two(self):
        '''
        Using built-in module "collections"
        '''

        dic = collections.Counter(self.strings)

        keys = [key for key in dic.keys()]  # Sorting keys of dic alphabetically so that we can print keys and values in order.
        keys.sort()

        for key in keys:
            print('{} : {}'.format(key, dic[key]))


if __name__ == '__main__':
    count = CountLetter('pneumonoultramicroscopicsilicovolcanoconiosis')

    print('Method One')
    count.method_one()

    print('\nMethod Two')
    count.method_two()
