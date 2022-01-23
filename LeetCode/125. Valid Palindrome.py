class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        x = ''
        s = s.lower()

        for i in s:
            if i.isalnum():
                x += i

        return x == x[::-1], x


x = Solution()
print(x.isPalindrome('0P'))
