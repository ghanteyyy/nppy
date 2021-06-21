def decrypt(encrypted_text, n):
    if n <= 0:
        return encrypted_text

    decrypted_text = ''
    even_place_text = encrypted_text[:len(encrypted_text) // 2]
    odd_place_text = encrypted_text[len(encrypted_text) // 2:]

    for index, value in enumerate(odd_place_text):
        try:
            decrypted_text += value + even_place_text[index]

        except IndexError:
            decrypted_text += value

    return decrypt(decrypted_text, n - 1)


def encrypt(text, n):
    if n <= 0:
        return text

    encoded_string = ''
    encoded_string += text[1::2] + text[::2]

    return encrypt(encoded_string, n - 1)


encryption = encrypt('This is a test!', 211)
decryption = decrypt(encryption, 211)
