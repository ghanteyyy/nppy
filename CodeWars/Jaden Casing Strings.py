def to_jaden_case(string):
    answer = ''
    split = string.split()

    for i, s in enumerate(split):
        answer += s[0].title() + s[1:] + ' '

    return answer.strip()


print(to_jaden_case("How can mirrors be real if our eyes aren't real"))  # How Can Mirrors Be Real If Our Eyes Aren't Real
