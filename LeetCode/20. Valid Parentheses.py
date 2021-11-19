class Solution:
    def isValid(self, s: str) -> bool:
        brackets = []
        pairs = {')': '(', '}': '{', ']': '['}

        for x in s:
            if x in pairs.values():
                brackets.append(x)

            else:
                if not brackets or brackets.pop() != pairs[x]:
                    return False

        return not brackets and len(s) != 0


if __name__ == '__main__':
    print(Solution().isValid('['))
    print(Solution().isValid(''))
    print(Solution().isValid('('))
    print(Solution().isValid('()'))
    print(Solution().isValid(']'))
