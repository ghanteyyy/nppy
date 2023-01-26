'''
Using names.txt (right click and 'Save Link/Target As...'), a 46K text
file containing over five-thousand first names, begin by sorting it into
alphabetical order. Then working out the alphabetical value for each name,
multiply this value by its alphabetical position in the list to obtain a
name score.

For example, when the list is sorted into alphabetical order, COLIN, which
is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list.
So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?
'''

import string

total_sum = 0
alphabets = {}
capwords = string.ascii_uppercase

for index, value in enumerate(capwords):
    alphabets.update({capwords[index]: index + 1})

with open('p022_names.txt', 'r') as names:
    lines = [name.strip('"') for name in names.read().strip('\n').split(',')]
    lines.sort()

    for line in lines:
        total_sum += sum([alphabets[li] for li in line]) * (lines.index(line) + 1)

    print(total_sum)
