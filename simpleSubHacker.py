# Simple Substitution Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)
# * Forked by Jared Wiese

import os, re, copy, pprint, simpleSubCipher, makeWordPatterns
from functools import partial
from multiprocessing import Pool, Lock, Value, Process

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main()  # create the wordPatterns.py file
import wordPatterns

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')


def getBlankcipherLetterMapping():
    # Returns a dictionary value that is a blank cipherLetter mapping.
    return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [], 'K': [], 'L': [],
            'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [], 'V': [], 'W': [], 'X': [],
            'Y': [], 'Z': []}


def addLettersToMapping(letterMapping, cipherword, candidate):
    # The letterMapping parameter is a "cipherLetter mapping" dictionary
    # value that the return value of this function starts as a copy of.
    # The cipherword parameter is a string value of the cipherText word.
    # The candidate parameter is a possible English word that the
    # cipherword could decrypt to.

    # This function adds the letters of the candidate as potential
    # decryption letters for the cipherLetters in the cipherLetter
    # mapping.
    newletterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherword)):
        if candidate[i] not in newletterMapping[cipherword[i]]:
            newletterMapping[cipherword[i]].append(candidate[i])
    letterMapping = newletterMapping
    return letterMapping


def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and then add only the
    # potential decryption letters if they exist in BOTH maps.
    intersectedMapping = getBlankcipherLetterMapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.deepcopy(mapA[letter])
        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)

    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    # Cipher letters in the mapping that map to only one letter are
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of letters for every other
    # letter. (This is why there is a loop that keeps reducing the map.)
    letterMapping = copy.deepcopy(letterMapping)
    loopAgain = True
    while loopAgain:
        # First assume that we will not loop again:
        loopAgain = False

        # solvedLetters will be a list of uppercase letters that have one
        # and only one possible mapping in letterMapping
        solvedLetters = []
        for cipherLetter in LETTERS:
            if len(letterMapping[cipherLetter]) == 1:
                solvedLetters.append(letterMapping[cipherLetter][0])

        # If a letter is solved, than it cannot possibly be a potential
        # decryption letter for a different cipherText letter, so we
        # should remove it from those other lists.
        for cipherLetter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[cipherLetter]) != 1 and s in letterMapping[cipherLetter]:
                    letterMapping[cipherLetter].remove(s)
                    if len(letterMapping[cipherLetter]) == 1:
                        # A new letter is now solved, so loop again.
                        loopAgain = True
    return letterMapping


def hackSimpleSub(cipherText):
    lock = Lock()
    with Pool() as ThreadPool:
        intersectedMap = getBlankcipherLetterMapping()
        cipherwordList = nonLettersOrSpacePattern.sub('', cipherText.upper()).split()
        for cipherword in cipherwordList:
            # Get a new cipherLetter mapping for each cipherText word.
            newMap = getBlankcipherLetterMapping()

            wordPattern = makeWordPatterns.getWordPattern(cipherword)
            if wordPattern not in wordPatterns.allPatterns:
                continue  # This word was not in our dictionary, so continue.

            # Add the letters of each candidate to the mapping.
            for candidate in wordPatterns.allPatterns[wordPattern]:
                newMap = addLettersToMapping(newMap, cipherword, candidate)

            intersectedMap = intersectMappings(intersectedMap, newMap)

    ThreadPool.close()
    ThreadPool.join()
    # Remove any solved letters from the other lists.
    return removeSolvedLettersFromMapping(intersectedMap)


def decryptWithcipherLetterMapping(cipherText, letterMapping):
    # Return a string of the cipherText decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with an _ underscore.

    # First create a simple sub key from the letterMapping mapping.
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

    # With the key we've created, decrypt the cipherText.
    decryptedMessage = simpleSubCipher.decryptMessage(key, cipherText)

    return decryptedMessage
