'''A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,

                        a^2 + b^2 = c^2
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.'''


found = False


for m in range(1, 101):
    for n in range(1, 101):
        if found is False:
            # a, b, c are the squares of side of the triangles
            a = m ** 2 - n ** 2
            b = 2 * m * n
            c = m ** 2 + n ** 2

            if a + b + c == 1000:
                print(a * b * c)
                found = True

            m += 4
            n += 4
