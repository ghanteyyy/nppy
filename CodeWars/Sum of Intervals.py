def sum_of_intervals(intervals):
    interval = {i for x in intervals for i in range(x[0], x[1])}
    return len(interval)


print(sum_of_intervals([(1, 5)]))
print(sum_of_intervals([(1, 5), (6, 10)]))
print(sum_of_intervals([(1, 5), (1, 5)]))
print(sum_of_intervals([(1, 4), (7, 10), (3, 5)]))
