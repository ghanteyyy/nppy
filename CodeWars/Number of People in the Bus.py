def number(bus_stops):
    diff = 0

    for x, y in bus_stops:
        diff += x - y

    return diff


print(number([[10, 0], [3, 5], [5, 8]]))                               # 5
print(number([[3, 0], [9, 1], [4, 10], [12, 2], [6, 1], [7, 10]]))     # 17
print(number([[3, 0], [9, 1], [4, 8], [12, 2], [6, 1], [7, 8]]))       # 21
