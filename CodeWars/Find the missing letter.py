def find_missing_letter(chars):
    prev_ord = False

    for char in chars:
        if prev_ord is False:
            prev_ord = True
            prev_ord = ord(char)

        else:
            present_ord = ord(char)

            if present_ord - prev_ord != 1:
                return chr(present_ord - 1)

            prev_ord = present_ord


print(find_missing_letter(['a', 'b', 'c', 'd', 'f']))   # e
print(find_missing_letter(['O', 'Q', 'R', 'S']))        # P
