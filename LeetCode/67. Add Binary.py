class Solution:
    def addBinary(self, a: str, b: str) -> str:
        carry = 0
        answer = ''

        # Getting the maximum length of a or b
        max_len = max(len(a), len(b))

        # Making a, b of same length
        a = a.zfill(max_len)
        b = b.zfill(max_len)

        max_len = max_len - 1

        while max_len >= 0:
            _sum = int(a[max_len]) + int(b[max_len])

            if _sum == 2:  # 1 + 1
                if carry == 0:
                    answer += '0'

                else:
                    answer += '1'

                carry = 1

            elif _sum == 1:  # 1 + 0 or 0 + 1
                if carry == 0:
                    answer += '1'

                else:
                    answer += '0'
                    carry = 1

            elif _sum == 0:  # 0 + 0
                if carry == 0:
                    answer += '0'

                else:
                    answer += '1'
                    carry = 0

            max_len -= 1

        if carry > 0:
            # Adding carry after adding all binary numbers if present
            answer += str(carry)

        return answer[::-1]  # Reversing the answer to get the final answer


x = Solution()
print(x.addBinary('100', '110010'))
