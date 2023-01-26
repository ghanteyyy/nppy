'''
If p is the perimeter of a right angle triangle with integral length
sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximized?
'''

counter = {}
total_perimeter = 1000
highest_count, result = 0, 0

for p in range(1, total_perimeter // 3):
    for b in range(p, 500):
        h = (p ** 2 + b ** 2) ** 0.5
        sums = int(p + b + h)

        if int(h) == h and sums <= total_perimeter:
            # Counting the number of repetitions of sum of p, b and h
            if sums in counter:
                counter[sums] += 1

            else:
                counter[sums] = 1

# Getting value whose number of repetitions is the highest
for val, count in counter.items():
    if count > highest_count:
        result = val
        highest_count = count

print(result)
