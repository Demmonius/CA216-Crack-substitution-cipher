# Simple Substitution Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)
# * Forked by Jared Wiese

import os, re, copy, pprint, makeWordPatterns
from functools import partial
from multiprocessing import Pool, Lock, Value, Process

import simpleSubCipher

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main()  # create the wordPatterns.py file
import wordPatterns

from string import ascii_uppercase as LETTERS

THREADS_TO_USE = 5

nonLettersOrSpacePattern = re.compile('[^A-Z\s]')


def getBlankcipherLetterMapping():
    # Returns a dictionary value that is a blank cipherLetter mapping.
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    newletterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in newletterMapping[cipherword[i]]:
            newletterMapping[cipherword[i]].append(candidate[i])
    letterMapping = newletterMapping
    return letterMapping


def intersectMappings(mapA, mapB):
    intersectedMapping = getBlankcipherLetterMapping()
    for letter in LETTERS:
        if not mapA[letter]:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif not mapB[letter]:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            [intersectedMapping[letter].append(mappedLetter) for mappedLetter in mapA[letter] if
             mappedLetter in mapB[letter]]

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        loopAgain = False

        solvedLetters = []
        [solvedLetters.append(letterMapping[cipherLetter][0]) for cipherLetter in LETTERS if
         len(letterMapping[cipherLetter]) == 1]

        for cipherLetter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherLetter]) != 1 and s in letterMapping[cipherLetter]:
                    letterMapping[cipherLetter].remove(s)
                    if len(letterMapping[cipherLetter]) == 1:
                        loopAgain = True
    return letterMapping


def hackSimpleSub(cipherText):
    intersectedMap = getBlankcipherLetterMapping()
    cipherwordList = nonLettersOrSpacePattern.sub('', cipherText.upper()).split()
    for cipherword in cipherwordList:
        newMap = getBlankcipherLetterMapping()

        wordPattern = makeWordPatterns.getWordPattern(cipherword)
        if wordPattern not in wordPatterns.allPatterns:
            continue

        # Add the letters of each candidate to the mapping.
        for candidate in wordPatterns.allPatterns[wordPattern]:
            newMap = addLettersToMapping(newMap, cipherword, candidate)

        intersectedMap = intersectMappings(intersectedMap, newMap)

    # Remove any solved letters from the other lists.
    return removeSolvedLettersFromMapping(intersectedMap)


def decryptWithcipherLetterMapping(cipherText, letterMapping):
    key = ['x'] * len(LETTERS)
    for cipherLetter in LETTERS:
        if len(letterMapping[cipherLetter]) == 1:
            # If there's only one letter, add it to the key.
            keyIndex = LETTERS.find(letterMapping[cipherLetter][0])
            key[keyIndex] = cipherLetter
        else:
            cipherText = cipherText.replace(cipherLetter.lower(), '_')
            cipherText = cipherText.replace(cipherLetter.upper(), '_')
    key = ''.join(key)

    decryptedMessage = simpleSubCipher.decryptMessage(key, cipherText)

    return decryptedMessage
