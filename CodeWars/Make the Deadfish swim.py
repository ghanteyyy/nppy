def parse(data):
    value = 0
    outputs = []

    for d in data:
        if d == 'i':
            value += 1

        elif d == 'd':
            value -= 1

        elif d == 's':
            value = value ** 2

        elif d == 'o':
            outputs.append(value)

    return outputs


print(parse("ooo"))                # [0,0,0]
print(parse("ioioio"))             # [1,2,3]
print(parse("idoiido"))            # [0,1]
print(parse("isoisoiso"))          # [1,4,25]
print(parse("codewars"))           # [0]
