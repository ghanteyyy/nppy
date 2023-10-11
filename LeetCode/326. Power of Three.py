class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        if n <= 0:
            return False

        for i in range(int(n ** (1/3)) + 1):
            pwr = int(3 ** i)

            if pwr == n:
                return True

            elif pwr > n:
                return False

        return False
