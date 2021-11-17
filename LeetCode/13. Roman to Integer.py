class Solution:
    def romanToInt(self, s: str) -> int:
        sums = 0
        pairs = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
        pairs_len = len(s)

        for i in range(pairs_len):
            curr_val = pairs[s[i]]

            if i + 1 < pairs_len and curr_val < pairs[s[i + 1]]:
                sums -= curr_val

            else:
                sums += curr_val

        return sums


print(Solution().romanToInt('MCMXCIV'))
