class Solution:
    def getRow(self, rowIndex: int):
        if rowIndex == 0:
            return [1]

        elif rowIndex == 1:
            return [1, 1]

        res = [1, 1]

        for i in range(2, rowIndex + 1):
            temp = []

            for j in range(len(res) - 1):
                temp.append(res[j] + res[j + 1])

            res = [res[0]] + temp + [res[0]]

        return res


x = Solution()
print(x.getRow(4))
