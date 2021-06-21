def validBraces(string):
    brackets = []
    bracket_maps = {')': '(', '}': '{', ']': '['}

    for s in string:
        if s in '([{':
            brackets.append(s)

        else:
            try:
                last_value = brackets[-1]

                if last_value == bracket_maps[s]:
                    brackets.pop()

            except IndexError:
                return False

    return not brackets


if __name__ == '__main__':
    print(validBraces('(((())))))'))
    print(validBraces('(((({{'))
    print(validBraces("[(])"))
    print(validBraces('(())'))
