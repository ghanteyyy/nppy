def into_hex(nums):
    _hex = ''
    dec_to_hex = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

    while nums != 0:
        rem = nums % 16
        nums = nums // 16

        if rem >= 10:
            rem = dec_to_hex[rem]

        _hex += str(rem)

    if len(_hex) == 1:
        _hex += '0'

    return _hex[::-1]


def check_if_in_range(num):
    if num < 0:
        return 0

    elif num > 255:
        return 255

    return num


def rgb(r, g, b):
    hex_value = ''

    for x in (r, g, b):
        y = check_if_in_range(x)

        if y == 0:
            hex_value += '00'

        else:
            hex_value += into_hex(y)

    return hex_value


hex_values = [(0, 0, 0), (1, 2, 3), (255, 255, 255), (254, 253, 252), (-20, 275, 125)]

for r, g, b in hex_values:
    print(rgb(r, g, b))
