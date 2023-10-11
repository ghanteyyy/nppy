class Solution:
    def sumOfSquares(self, n):
        sums = 0

        while n != 0:
            sums += (n % 10) ** 2
            n //= 10

        return sums

    def isHappy(self, n: int) -> bool:
        for i in range(1000):
            sums = self.sumOfSquares(n)

            if sums == 1:
                return True

            n = sums

        return False
