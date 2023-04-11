class Solution:
    def TurnIntoNumber(self, string, maps):
        num = 0

        for s in string:
            num = num * 10 + maps[s]

        return num

    def multiply(self, num1: str, num2: str) -> str:
        maps = {str(i): i for i in range(10)}

        num1 = self.TurnIntoNumber(num1, maps)
        num2 = self.TurnIntoNumber(num2, maps)

        return str(num1 * num2)
