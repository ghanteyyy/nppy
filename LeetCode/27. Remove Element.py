class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """

        for i in range(len(nums) - 1):
            if nums[i] == val:
                findex = i + 1

                while True:
                    if nums[i] != nums[findex]:
                        nums[i], nums[findex] = nums[findex], nums[i]
                        break

                    if findex >= len(nums) - 1:
                        break

                    findex += 1

        for j in range(len(nums) - 1, -1, -1):
            if nums[j] != val:
                j += 1
                break

        return len(nums[:j])


x = Solution()
print(x.removeElement([0, 1, 2, 2, 3, 0, 4, 2], 2))
print(x.removeElement([3, 2, 2, 3], 3))
print(x.removeElement([2], 3))
print(x.removeElement([1], 1))
print(x.removeElement([4, 5], 4))
