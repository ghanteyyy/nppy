def calculate_years(principal, interest, tax, desired):
    years = 0

    while principal < desired:
        acquired_interest = principal * interest
        interest_without_tax = acquired_interest - acquired_interest * tax
        principal += interest_without_tax

        years += 1

    return years


print(calculate_years(1000, 0.05, 0.18, 1100))
print(calculate_years(1000, 0.05, 0.18, 1000))
print(calculate_years(1000, 0.01625, 0.18, 1200))
