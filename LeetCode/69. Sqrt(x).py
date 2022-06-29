class Solution:
    def mySqrt(self, x: int):
        '''
        Used newton-raphson method algorithm
            Formula for newton-raphson method
                x(n+1) = (1/2) * (x(n) + (num / x(n)))
                    when x(n) is the previous obtained root
                         x(n+1) if the present obtained root

                    To get exact root the previous root and present root
                    upto 5 decimal places (you can check for more decimal
                    places but 5 would be enough)

            For example, if we need to find the root of 8 then
                num = 8
                x(n) = 1  [Suppose previous root is 1]

                Then, From the above formula
                    First Step:
                        x(n+1) = (1/2) * (1 + (8 / 1))
                                = 4.5

                    Second Step:
                        Here, x(n) becomes x(n + 1)
                            i.e. x(n) = 4.5

                            x(n+1) = (1/2) * (4.5 + (8 / 4.5))
                                        = 3.13889

                    Same process is continued till the value of x(n) and x(n+1)
                    are equal upto 5 decimal places (or more as per required)
        '''

        previous_root = 1

        while True:
            present_root = round(((1 / 2) * (previous_root + (x / previous_root))), 5)

            if previous_root == present_root:
                return int(previous_root)

            previous_root = present_root


x = Solution()
print(x.mySqrt(8))
