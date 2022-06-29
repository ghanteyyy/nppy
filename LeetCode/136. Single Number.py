class Solution:
    def singleNumber(self, nums) -> int:
        count = dict()

        for num in nums:
            if num in count:
                count[num] += 1

            else:
                count[num] = 1

        for key, value in count.items():
            if value == 1:
                return key


x = Solution()
print(x.singleNumber([4,1,2,1,2]))
