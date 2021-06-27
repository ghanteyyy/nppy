def break_chocolate(n, m):
    breaks = (n * m) - 1

    if breaks < 0:
        return 0

    return breaks


print(break_chocolate(5, 5))  # 24
print(break_chocolate(7, 4))  # 27
print(break_chocolate(1, 1))  # 0
print(break_chocolate(0, 0))  # 0
print(break_chocolate(6, 1))  # 5
