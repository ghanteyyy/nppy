def order(sentence):
    if not sentence:
        return sentence

    res = []
    split = sentence.split()

    for i in range(1, len(split) + 1):
        for s in split:
            if str(i) in s:
                res.append(s)

    return ' '.join(res)


print(order("is2 Thi1s T4est 3a"))                             # "Thi1s is2 3a T4est")
print(order("4of Fo1r pe6ople g3ood th5e the2"))               # "Fo1r the2 g3ood 4of th5e pe6ople")
print(order(""))                                               # ""
