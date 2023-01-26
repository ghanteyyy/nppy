'''
The nth term of the sequence of triangle numbers is given by,
tn = ½n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its
alphabetical position and adding these values we form a word value.
For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If
the word value is a triangle number then we shall call the word a
triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text
file containing nearly two-thousand common English words, how many are
triangle words?
'''

import string

total_triangle_coded_nums = 0


def is_triangle_coded_num(n):
	n = (-1 + (1 + 8 * n) ** 0.5) / 2
	return n - int(n) == 0


uppercase = string.ascii_uppercase

with open('p042_words.txt', 'r') as f:
    contents = f.read().split(',')

    for content in contents:
        temp_num = 0

        for cont in content[1:-1]:  # Adding corresponding alphabetical position
            temp_num += uppercase.index(cont) + 1

        if is_triangle_coded_num(temp_num):  # Checking if the added value is triangle coded number
            total_triangle_coded_nums += 1

print(total_triangle_coded_nums)
