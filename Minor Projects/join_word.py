def join_word(string, joining_keyword):
    """Join your word with your joining keyword
        Example:
                word = PYTHON
                joining_keyword = -

                then you get
                    P-Y-T-H-O-N
    """

    def method_one(string, joining_keyword):
        join_word = ""

        for x in range(0, len(string)):
            join_word += string[x] + joining_keyword

        print(join_word[:-1])

    def method_two(string, joining_keyword):
        join = (joining_keyword).join(string)

        print(join)

    print("Method One")
    method_one(string, joining_keyword)

    print("\nMethod Two")
    method_two(string, joining_keyword)


if __name__ == "__main__":
    try:
        join_word("python", "-")

    except (ValueError, NameError):
        print("String value was expected")
