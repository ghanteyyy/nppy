'''
Starting with the number 1 and moving to the right in a clockwise
direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001
spiral formed in the same way?
'''


def move_right(x, y):
    return x, y + 1


def move_down(x, y):
    return x + 1, y


def move_left(x, y):
    return x, y - 1


def move_up(x, y):
    return x - 1, y


def GetSpiralNumbers(n):
    count = 1
    total_moves = 1
    x, y = (n // 2, n // 2)

    nums =[['' for _ in range(n)] for _ in range(n)]
    moves = [move_right, move_down, move_left, move_up]

    nums[x][y] = count

    for _ in range(n):
        for _ in range(2):
            for _ in range(total_moves):
                count += 1
                x, y = moves[0](x, y)

                if x == n or y == n:
                    return nums

                nums[x][y] = count

            moves = moves[1:] + [moves[0]]  # Cycling moves

        total_moves += 1


def GetSum(n, array):
    row = 0
    sums = 0
    mid = n // 2

    for i in range(n):
        if i == mid:
            sums += array[row][i]

        elif i < mid:
            sums += array[row][i] + array[row][n - i - 1]

        else:
            sums += array[row][n - i - 1] + array[row][i]

        row += 1

    return sums


n = 1001
SpiralNumbers = GetSpiralNumbers(n)

sums = GetSum(n, SpiralNumbers)
print(sums)
