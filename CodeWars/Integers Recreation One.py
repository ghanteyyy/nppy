def list_squared(m, n):
    answers = []

    for i in range(m, n + 1):
        factors = set()

        # Getting factors
        for j in range(1, int(i ** 0.5) + 1):
            if i % j == 0:
                factors.add(j)
                factors.add(i // j)

        # Getting sum of squared of the obtained factors
        squared_factors = sum(map(lambda x: x ** 2, factors))

        # Getting the squared root of the sum of squared of factors
        square_root = int(squared_factors ** 0.5)

        # Checking if the sum of squared of factors is actually a perfect square
        if square_root ** 2 == squared_factors:
            answers.append([i, squared_factors])

    return answers


print(list_squared(1, 250))     # [[1, 1], [42, 2500], [246, 84100]])
print(list_squared(42, 250))    # [[42, 2500], [246, 84100]])
print(list_squared(250, 500))   # [[287, 84100]])
