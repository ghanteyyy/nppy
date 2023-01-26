'''
If the numbers 1 to 5 are written out in words: one, two, three, four,
five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written
out in words, how many letters would be used?


NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and
      forty-two) contains 23 letters and 115 (one hundred and fifteen) contains
      20 letters. The use of "and" when writing out numbers is in compliance with British usage.
'''

place_value = []

ones_place = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine'
}

en_place = {
    11: 'elevan',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen'
}

ty_place = {
    10: 'ten',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
}

for i in range(1, 1001):
    num = str(i)

    if len(num) == 1:
        place_value.append(ones_place[i])

    elif len(num) == 2:
        if num[-1] == '0':
            place_value.append(ty_place[int(num)])

        elif num[0] == '1':
            place_value.append(en_place[int(num)])

        else:
            place_value.append(ty_place[int(num[0] + '0')] + ones_place[int(num[-1])])

    elif len(num) == 3:
        if num[1] == '0' and num[-1] == '0':
            place_value.append(ones_place[int(num[0])] + 'hundred')

        elif num[-1] == '0':
            place_value.append(ones_place[int(num[0])] + 'hundredand' + ty_place[int(num[1] + '0')])

        elif num[1] == '0':
            place_value.append(ones_place[int(num[0])] + 'hundredand' + ones_place[int(num[-1])])

        else:
            if int(num[1:]) in range(11, 20):
                place_value.append(ones_place[int(num[0])] + 'hundredand' + en_place[int(num[1:])])

            else:
                place_value.append(ones_place[int(num[0])] + 'hundredand' + ty_place[int(num[1] + '0')] + ones_place[int(num[-1])])

    else:
        place_value.append('Onethousand')


sums = len(''.join(place_value))
print(sums)
