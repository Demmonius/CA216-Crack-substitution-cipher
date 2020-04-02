import string


def getOccurences(text):
    singleOccurence = {}
    doubleOccurence = {}
    lettersOccurence = {}
    for word in text.replace('\n', '').split(" "):
        for letter in word:
            if letter not in string.punctuation:
                lettersOccurence[letter] = lettersOccurence[letter] + 1 if letter in lettersOccurence else 1
        if len(word) == 1:
            singleOccurence[word] = singleOccurence[word] + 1 if word in singleOccurence else 1
        elif len(word) == 2:
            doubleOccurence[word] = doubleOccurence[word] + 1 if word in doubleOccurence else 1

    print(singleOccurence)
    print(doubleOccurence)
    print(lettersOccurence)
    return [
        singleOccurence,
        doubleOccurence,
        lettersOccurence
    ]
