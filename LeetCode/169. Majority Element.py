class Solution:
    def majorityElement(self, nums) -> int:
        res = 0
        count = dict()
        number_of_count = 0

        for num in nums:
            if num in count:
                count[num] += 1

            else:
                count[num] = 1

        for key, value in count.items():
            if value > number_of_count:
                res = key
                number_of_count = value

        return res


x = Solution()
print(x.majorityElement([2,2,1,1,1,2,2]))
