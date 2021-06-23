def stray(arr):
    counter = {}

    # Count the number of repetitions of values
    for a in arr:
        if a in counter:
            counter[a] += counter[a]

        else:
            counter.update({a: 1})

    # Get the key having the minium repetition value
    for k, v in counter.items():
        if v == 1:
            return k


print(stray([17, 17, 3, 17, 17, 17, 17]))
print(stray([1, 1, 2]))
