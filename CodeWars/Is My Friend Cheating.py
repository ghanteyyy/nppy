def remov_nb(n):
    answers = []
    sums = (n * (n + 1)) / 2

    for a in range(1, n + 1):
        b = int((sums - a) // (a + 1))

        if b < n and a * b + a + b == sums and (a, b) not in answers:
            answers.append((a, b))

    return answers if answers else []


print(remov_nb(26))
print(remov_nb(100))
print(remov_nb(101))
