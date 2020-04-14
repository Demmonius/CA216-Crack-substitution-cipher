import threading

import makeWordPatterns
import wordPatterns
from simpleSubHacker import getBlankcipherLetterMapping, addLettersToMapping, intersectMappings

intersectedMap = getBlankcipherLetterMapping()

class WordMappingMaker(threading.Thread):
    def __init__(self, cipherwordList, lock):
        super().__init__()
        self.cipherwordList = cipherwordList
        self.lock = lock

    def run(self):
        for cipherword in self.cipherwordList:
            newMap = getBlankcipherLetterMapping()

            wordPattern = makeWordPatterns.getWordPattern(cipherword)
            if wordPattern not in wordPatterns.allPatterns:
                continue

            # Add the letters of each candidate to the mapping.
            for candidate in wordPatterns.allPatterns[wordPattern]:
                newMap = addLettersToMapping(newMap, cipherword, candidate)
            with self.lock:
                intersectedMap = intersectMappings(intersectedMap, newMap)