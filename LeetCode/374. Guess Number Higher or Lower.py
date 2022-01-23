# The guess API is already defined for you.
# @param num, your guess
# @return -1 if my number is lower, 1 if my number is higher, otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        low = 1
        high = n

        while low <= high:
            mid = (low + high) // 2

            if guess(mid) == 0:  # guess function is called automatically when ran in leetcode
                return mid

            elif guess(mid) == 1:
                low = mid - 1

            else:
                high = mid + 1
