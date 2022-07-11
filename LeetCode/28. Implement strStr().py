class Solution(object):
    def strStr(self, haystack, needle):
        """
        :type haystack: str
        :type needle: str
        :rtype: int
        """

        index = 0
        hay_length = len(haystack)
        needleLength = len(needle)

        if needleLength == 0:
            return 0

        while index <= hay_length:
            if haystack[index: index + needleLength] == needle:
                return index

            index += 1

        return -1


x = Solution()
print(x.strStr('hello', 'll'))
print(x.strStr('aaaaaa', 'baa'))
print(x.strStr('', ''))
print(x.strStr('mississippi', 'issip'))
