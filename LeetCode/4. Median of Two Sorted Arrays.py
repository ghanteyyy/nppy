class Solution:
    def findMedianSortedArrays(self, nums1, nums2) -> float:
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """

        nums = nums1 + nums2
        nums.sort()

        mid = len(nums) / 2
        _init_mid = int(mid)

        if mid == _init_mid:
            mid = _init_mid - 1
            return (nums[mid] + nums[mid + 1]) / 2.0

        return nums[_init_mid]
