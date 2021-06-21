import string


def get_thirteenth_letter(msg, string):
    index = string.index(msg) + 13

    if index >= 26:
        index = index - 26

    return string[index]


def rot13(message):
    encode = ''

    for m in message:
        if m in string.ascii_lowercase:
            encode += get_thirteenth_letter(m, string.ascii_lowercase)

        elif m in string.ascii_uppercase:
            encode += get_thirteenth_letter(m, string.ascii_uppercase)

        else:
            encode += m

    return encode


res1 = rot13('test')
res2 = rot13('Test')

print(res1)
print(res2)
