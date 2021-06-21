def move_zeros(array):
    return [arr for arr in array if arr != 0] + [arr for arr in array if arr == 0]


res = move_zeros([1, 0, 1, 2, 0, 1, 3])  # returns [1, 1, 2, 1, 3, 0, 0]
print(res)
