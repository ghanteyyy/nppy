class Solution(object):
    def another_solution(self, s):
        withoutSpace = [x for x in s.split() if x][-1]
        return len(withoutSpace)

    def lengthOfLastWord(self, s):
        """
        :type s: str
        :rtype: int
        """

        split = s.split()
        splitLength = len(split) - 1

        while True:
            x = split[splitLength]

            if x:
                return len(x)

            splitLength -= 1

x = Solution()
print(x.lengthOfLastWord('Hello World'))
