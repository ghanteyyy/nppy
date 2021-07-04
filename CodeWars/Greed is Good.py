def score(dice):
    thrice_nums = {1: 1000, 2: 200, 3: 300,
                   4: 400, 5: 500, 6: 600}

    one_nums = {1: 100, 5: 50}

    sums = 0
    counts = {}

    for d in dice:
        if d in counts:
            counts[d] += 1

        else:
            counts[d] = 1

    for k, v in counts.items():
        if v >= 3:
            v -= 3
            sums += thrice_nums[k]

        if v in [1, 2]:
            if k in one_nums:
                sums += v * one_nums[k]

    return sums


print(score([2, 3, 4, 6, 2]))  # 0
print(score([4, 4, 4, 3, 3]))  # 400
print(score([2, 4, 4, 5, 4]))  # 450
print(score([1, 1, 1, 1, 3]))  # 1100
