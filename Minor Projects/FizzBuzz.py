class FizzBuzz:
    '''
    Game Rules:
        1. For multiples of 3 print "Fizz"
        2. For multiples of 5 print "Buzz"
        3. For multiples of both 3 and 5 print "FizzBuzz
    '''

    def __init__(self, nums):
        self.nums = nums

    def is_divisible_by_three_or_five(self, num, by):
        '''
        Checking if the num is divided by 5 or 3 which is given in "by" except for 0
        '''

        if num % by == 0 and num > 0:
            return True

        return False

    def main(self):
        '''
        Checking all number within the range of self.nums
        '''

        for num in range(self.nums):
            if self.is_divisible_by_three_or_five(num, 3) and self.is_divisible_by_three_or_five(num, 5):
                print(f'{num}: FizzBuzz')

            elif self.is_divisible_by_three_or_five(num, 3):
                print(f'{num} Fizz')

            elif self.is_divisible_by_three_or_five(num, 5):
                print(f'{num}: Buzz')

            else:
                print(num)


if __name__ == '__main__':
    fizz_buzz = FizzBuzz(100)
    fizz_buzz.main()
