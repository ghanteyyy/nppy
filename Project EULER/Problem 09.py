'''
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
                        a^2 + b^2 = c^2

For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.'''


'''
To find pythagorean triplet I have used Euclid formula:
    a = m ^ 2 - n ^ 2
    b = 2 * m * n
    c = m ^ 2 + n ^ 2

    where, m and n are two natural numbers
           m is always greater than n
'''


# When m & n > 22 then value of c alone exceeds 1000 so values of m &
# n must be below 23
for m in range(4, 23):
    for n in range(4, 23):
        a = m ** 2 - n ** 2
        b = 2 * m * n
        c = m ** 2 + n ** 2

        if a + b + c == 1000:
            print(a * b * c)
