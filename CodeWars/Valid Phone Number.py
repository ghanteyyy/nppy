def validPhoneNumber(phoneNumber):
    left_bracket_index = phoneNumber.index('(')
    right_bracket_index = phoneNumber.index(')')

    if phoneNumber[0] != '(':
        return False

    if '-' not in phoneNumber:
        return False

    split = phoneNumber[right_bracket_index + 2:].split('-')

    if not split[0].isdigit() or not split[1].isdigit():
        return False

    if not phoneNumber[left_bracket_index + 1: right_bracket_index].isdigit():
        return False

    if phoneNumber[right_bracket_index + 1] != ' ':
        return False

    return True


print(validPhoneNumber("(123) 456-7890"))   # True
print(validPhoneNumber('(098) 123 4567'))   # False
