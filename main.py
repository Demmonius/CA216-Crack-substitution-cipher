import argparse
import string
import pprint

import makeWordPatterns
from cryptoAnalysis.utils import getOccurences
from simpleSubCipher import LETTERS
from simpleSubHacker import hackSimpleSub, decryptWithcipherLetterMapping

translator = str.maketrans('', '', string.punctuation.replace("_", ""))


def findWord(text, index, character=' '):
    first = index
    while text[first] != character and first != 0:
        first -= 1
    last = index
    while text[last] != character and last != len(text) - 1:
        last += 1
    return text[first:last].replace(character, "")


def applyPossibilities(originalText, decryptedMessage, letterMapping, dictionary):
    for index in [i for i, ltr in enumerate(decryptedMessage) if ltr == "_"]:
        possibilities = letterMapping[originalText[index].upper()]
        if len(possibilities) == 1:
            newWord = decryptedMessage[:index] + possibilities[0] + decryptedMessage[
                                                                    index + 1:]  # Only change the '_' we are expected
            decryptedMessage = decryptedMessage.replace(decryptedMessage, newWord)

    for index in [i for i, ltr in enumerate(decryptedMessage) if ltr == "_"]:
        word = findWord(decryptedMessage, index)
        for letter in LETTERS:
            computedWord = word.upper().replace("_", letter)
            if computedWord in dictionary:
                decryptedMessage = decryptedMessage.replace(word, computedWord.lower())
    print("TEXT AFTER POSSIBILITIES")
    print(decryptedMessage)


def findPossibilities(originalText, decryptedMessage, letterMapping):
    dictionaryFile = open('dictionary.txt')
    dictionary = dictionaryFile.read().split('\n')
    dictionaryFile.close()
    dictionaryFile = open('possibilitiesDictionary.txt')
    dictionary += dictionaryFile.read().split('\n')
    dictionaryFile.close()

    print("--------------------")
    for line, originalLine in zip(decryptedMessage.split("\n"), originalText.split("\n")):
        for word, originalWord in zip(line.split(), originalLine.split()):
            word = word.translate(translator)
            originalWord = originalWord.translate(translator)
            if "_" in word and word.count("_") == 1:
                for letterMap in letterMapping[originalWord[word.find("_")].upper()][::]:
                    if not any([word.replace("_", letterMap).upper().startswith(dictWord) for dictWord in dictionary]):
                        letterMapping[originalWord[word.find("_")].upper()].remove(letterMap)

    print("Letter mapping use possibilities only")

    # Ré-éléminer lettres restantes car pas possible de dupliqué
    pprint.pprint(letterMapping)
    print()

    print('Hacked Message: ')
    print(decryptedMessage)
    applyPossibilities(originalText, decryptedMessage, letterMapping, dictionary)


def useDictionary(text):
    # Determine the possible valid cipherText translations.
    print('Hacking...')
    letterMapping = hackSimpleSub(text)
    # Display the results to the user.
    print('Original Cipher Text: ')
    print(text)
    print()

    print("Letters map:")
    pprint.pprint(letterMapping)
    print()

    decryptedMessage = decryptWithcipherLetterMapping(text, letterMapping)
    findPossibilities(text, decryptedMessage, letterMapping)
    # print(decryptedMessage)


def main(text):
    # getOccurences(text.lower())
    useDictionary(text.lower())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crack cipher text')
    parser.add_argument('-f', '--file', type=str, help='a file to crack')
    parser.add_argument('-t', '--text', type=str, help='decrypt by raw text')

    args = parser.parse_args()
    if not any(vars(parser.parse_args()).values()):
        parser.error('No arguments provided.')
    text = args.text
    if args.file:
        f = open(args.file, "r")
        text = f.read()
    main(text)
