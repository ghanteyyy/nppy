def first_non_repeating_letter(string):
    counter = dict()

    for s in string:
        if s.lower() in counter:
            counter[s.lower()] += 1

        else:
            counter[s.lower()] = 1

    only_once = [k for k, v in counter.items() if v == 1]

    if not only_once:
        return ''

    for s in string:
        if s.lower() == only_once[0]:
            return s


print(first_non_repeating_letter('a'))
print(first_non_repeating_letter('stress'))
print(first_non_repeating_letter('moonmen'))

print(first_non_repeating_letter(''))

print(first_non_repeating_letter('abba'))
print(first_non_repeating_letter('aa'))

print(first_non_repeating_letter('~><#~><'))
print(first_non_repeating_letter('hello world, eh?'))

print(first_non_repeating_letter('sTreSS'))
print(first_non_repeating_letter('Go hang a salami, I\'m a lasagna hog!'))
