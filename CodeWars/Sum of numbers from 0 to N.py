def show_sequence(n):
    if n < 0:
        return f'{n}<0'

    if n == 0:
        return '0=0'

    nums = [str(i) for i in range(0, n + 1)]
    sums = str(sum(range(0, n + 1)))

    return '+'.join(nums) + ' = ' + sums


print(show_sequence(6))     # 0+1+2+3+4+5+6 = 21
print(show_sequence(7))     # 0+1+2+3+4+5+6+7 = 28
print(show_sequence(0))     # 0=0
print(show_sequence(-1))    # -1<0
print(show_sequence(-10))   # -10<0
