class Solution:
    def minLen(self, strs):
        _min = strs[0]

        for _str in strs[1:]:
            if len(_str) < len(_min):
                _min = _str

        return _min

    def longestCommonPrefix(self, strs):
        substring = ''
        minimum = self.minLen(strs)

        for i in range(len(minimum) + 1):
            count = 0

            for _str in strs:
                if _str[:i] == minimum[:i]:
                    count += 1

            if count == len(strs):
                substring = _str[:i]

        return substring

sol = Solution()
res = sol.longestCommonPrefix(["flower","flow","flight"])
print(res)
res = sol.longestCommonPrefix(["dog","racecar","car"])
print(res)
res = sol.longestCommonPrefix(["a"])
print(res)
