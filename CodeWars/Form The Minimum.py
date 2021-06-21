def min_value(digits):
    no_duplicates = []

    # Removing duplicates
    for digit in digits:
        if digit not in no_duplicates:
            no_duplicates.append(digit)

    # Sorting
    length = len(no_duplicates)

    for i in range(length):
        for j in range(i + 1, length):
            if no_duplicates[j] < no_duplicates[i]:
                no_duplicates[i], no_duplicates[j] = no_duplicates[j], no_duplicates[i]

    # Concatenate
    return int(''.join([str(digit) for digit in no_duplicates]))


print(min_value([1, 3, 1]))
print(min_value([4, 7, 5, 7]))
print(min_value([4, 8, 1, 4]))
