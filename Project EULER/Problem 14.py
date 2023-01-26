'''
The following iterative sequence is defined for the set of positive
integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following
sequence:

13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1
It can be seen that this sequence (starting at 13 and finishing at 1)
contains 10 terms. Although it has not been proved yet (Collatz Problem),
it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
'''

memo = dict()
max_sequence_count = 0
longest_sequence_num = 0

for i in range(1, 1000001):
    n = i
    temp_memo = []
    temp_memo.append(i)

    while n != 1:
        if n in memo:
            temp_memo.extend(memo[n][1:])
            n = 1

        else:
            if n % 2 == 0:
                n = n / 2

            else:
                n = 3 * n + 1

            temp_memo.append(int(n))

    memo[i] = temp_memo
    temp_len = len(temp_memo)

    if temp_len > max_sequence_count:
        max_sequence_count = temp_len
        longest_sequence_num = i

print(longest_sequence_num)
