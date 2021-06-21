def solution(s):
    values = []

    if len(s) % 2 != 0:
        s += '_'

    for num in range(0, len(s), 2):
        values.append(s[num: num + 2])

    return values


res = solution('asdfads')
print(res)
