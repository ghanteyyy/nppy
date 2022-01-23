class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        index = 0

        for i in range(len(nums)):
            if nums[i] != nums[index]:
                index += 1
                nums[index] = nums[i]

        return nums[:index + 1]


x = Solution()
print(x.removeDuplicates([0,0,1,1,1,2,2,3,3,4]))
print(x.removeDuplicates([1,1,2]))
print(x.removeDuplicates([]))
