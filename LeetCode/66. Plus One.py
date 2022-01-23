class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """

        if not digits:
            return digits

        sums = 0
        output = []
        ledDigits = len(digits)
        tenth = 10 ** (ledDigits - 1)

        for i in range(ledDigits):
            sums += digits[i] * tenth
            tenth //= 10

        sums += 1

        while sums > 0:
            rem = sums % 10
            sums //= 10
            output.append(rem)

        return output[::-1]


x = Solution()
print(x.plusOne([1, 2, 3]))
print(x.plusOne([1]))
print(x.plusOne([]))
