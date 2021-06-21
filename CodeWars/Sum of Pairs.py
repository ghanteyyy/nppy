def sum_pairs(ints, s):
    hash_tables = set()

    for val in ints:
        if s - val in hash_tables:
            return [s - val, val]

        hash_tables.add(val)


l1 = [1, 4, 8, 7, 3, 15]
l2 = [1, -2, 3, 0, -6, 1]
l3 = [20, -13, 40]
l4 = [1, 2, 3, 4, 1, 0]
l5 = [10, 5, 2, 3, 7, 5]
l6 = [4, -2, 3, 3, 4]
l7 = [0, 2, 0]
l8 = [5, 9, 13, -3]


print(sum_pairs(l1, 8))    # == [1, 7]
print(sum_pairs(l2, -6))   # == [0, -6]
print(sum_pairs(l3, -7))   # == None, "No Match: %s should return None for sum = -7" % l3)
print(sum_pairs(l4, 2))    # == [1, 1], "First Match From Left: %s should return [1, 1] for sum = 2 " % l4)
print(sum_pairs(l5, 10))   # == [3, 7], "First Match From Left REDUX!: %s should return [3, 7] for sum = 10 " % l5)
print(sum_pairs(l6, 8))    # == [4, 4], "Duplicates: %s should return [4, 4] for sum = 8" % l6)
print(sum_pairs(l7, 0))    # == [0, 0], "Zeroes: %s should return [0, 0] for sum = 0" % l7)
print(sum_pairs(l8, 10))   # == [13, -3], "Subtraction: %s should return [13, -3] for sum = 10" % l8)
