def get_mininum_value(values):
    val = values[0]

    for value in values[1:]:
        if value < val:
            val = value

    return val


def stray(arr):
    counter = {}

    # Count the number of repetitions of values
    for a in arr:
        if a in counter:
            counter[a] += counter[a]

        else:
            counter.update({a: 1})

    # Get the minimum repetition
    values = get_mininum_value(list(counter.values()))

    # Get the key having the minium repetition value
    for k, v in counter.items():
        if v == values:
            return k


print(stray([17, 17, 3, 17, 17, 17, 17]))
print(stray([1, 1, 2]))
