from functools import lru_cache


class Fibonacci:
    ''' Fibonacci number is a series of numbers in which each number is the sum of the two preceding numbers.
                Eg: 1, 1, 2, 3, 5, 8, etc. '''

    def __init__(self):
        self.expensive_function_calls = {}

    def recursive_method(self, steps):
        '''Getting Fibonacci series using recursive method'''

        if steps <= 1:
            return steps

        else:
            return self.recursive_method(steps - 1) + self.recursive_method(steps - 2)

    def optimized_recursive_method(self, steps):
        '''Optimizing recursive method with a technique called Memoization.

           Memoization is an optimization technique used primarily to speed
           up computer programs by storing the results of expensive function
           calls and returning the cached result when the same inputs occur
           again'''

        if steps <= 1:
            self.expensive_function_calls[steps] = steps   # Storing function calls
            return self.expensive_function_calls[steps]

        if steps in self.expensive_function_calls:
            return self.expensive_function_calls[steps]

        else:
            series = self.optimized_recursive_method(steps - 1) + self.optimized_recursive_method(steps - 2)
            self.expensive_function_calls[steps] = series   # Storing function calls

            return self.expensive_function_calls[steps]

    @lru_cache(maxsize=None)
    def optimized_recursive_builtin_method(self, steps):
        '''Using built-in Memoization tools called lru_cached. So that we
           don't need to make our own(like in optimized_recursive_method).'''

        if steps < 2:
            return steps

        return self.optimized_recursive_method(steps - 1) + self.optimized_recursive_method(steps - 2)

    def space_optimized_method_1(self, first_value, second_value, steps):
        '''The simplest method to print the Fibonacci series where
           swapping is done in two lines'''

        for _ in range(steps):
            print(first_value)

            third_value = first_value + second_value
            first_value = second_value
            second_value = third_value

    def space_optimized_method_2(self, first_value, second_value, steps):
        '''The simplest method to print the Fibonacci series where
           swapping is done in a single line'''

        for _ in range(steps):
            print(first_value)

            first_value, second_value = second_value, first_value + second_value


if __name__ == '__main__':
    fibonacci = Fibonacci()

    print('\nRecursive Method:')
    for x in range(30):
        print(fibonacci.recursive_method(x))

    print('\nOptimized Recursive Method')
    for x in range(30):
        print(fibonacci.optimized_recursive_method(x))

    print('\nOptimized Recursive Method with built-in')
    for x in range(30):
        print(fibonacci.optimized_recursive_builtin_method(x))

    print('\nSpace Optimized Method 1')
    fibonacci.space_optimized_method_1(0, 1, 30)

    print('\nSpace Optimized Method 2')
    fibonacci.space_optimized_method_2(0, 1, 30)
