class Solution:
    def generate(self, numRows: int):
        res = [[1]]

        for i in range(numRows - 1):
            temp = []
            last_len = len(res[-1]) - 1

            for j in range(last_len):
                n = j + 1
                _sum = res[last_len][j] + res[last_len][n]

                temp.append(_sum)

                if n == last_len:
                    break

            final = [res[last_len][0]] + temp + [res[last_len][0]]  # Combing required values to one list
            res.append(final)

        return res


x = Solution()
print(x.generate(5) == [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]])
