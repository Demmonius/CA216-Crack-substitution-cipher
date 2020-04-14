from string import ascii_uppercase as LETTERS


def decryptMessage(key, message):
    translated = ''

    # loop through each symbol in the message
    for symbol in message:
        if symbol.upper() in key:
            symIndex = key.find(symbol.upper())
            if symbol.isupper():
                translated += LETTERS[symIndex].upper()
            else:
                translated += LETTERS[symIndex].lower()
        else:
            translated += symbol

    return translated
