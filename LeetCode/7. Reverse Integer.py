class Solution:
    def check_bit(self, x):
        maxInt32 = -2147483647
        return x < maxInt32 or x > abs(maxInt32)

    def reverse(self, x: int) -> int:
        if self.check_bit(x):
            return 0

        reverse = 0
        less_than_zero = False

        if x < 0:
            x = abs(x)
            less_than_zero = True

        while x != 0:
            rem = x % 10
            x //= 10
            reverse = reverse * 10 + rem

        reverse = int(reverse)

        if less_than_zero:
            reverse = -reverse

        if self.check_bit(reverse):
            return 0

        return reverse


        # Another Method
        str_x = str(x)

        if x < 0:
            res = '-' + str_x[-1:0:-1]

        else:
            res = str_x[::-1]

        res = int(res)

        if self.check_bit(res):
            return 0

        return res
