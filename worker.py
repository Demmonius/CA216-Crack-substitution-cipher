import threading
from typing import Optional

import makeWordPatterns
import wordPatterns
from simpleSubHacker import addLettersToMapping, getBlankcipherLetterMapping, intersectMappings


class WordComputing(threading.Thread):
    def __init__(self, cipherword):
        super().__init__()

        self.result = getBlankcipherLetterMapping()
        self.cipherWord = cipherword
        self.intersectedMap = getBlankcipherLetterMapping()

        self._stop_event = threading.Event()

    def run(self) -> None:

        wordPattern = makeWordPatterns.getWordPattern(self.cipherWord)
        if wordPattern not in wordPatterns.allPatterns:
            return

        # Add the letters of each candidate to the mapping.
        for candidate in wordPatterns.allPatterns[wordPattern]:
            self.result = addLettersToMapping(self.result, self.cipherword, candidate)

    def join(self, timeout: Optional[float] = None) -> None:
        self._stop_event.set()
        super().join(self, timeout)

    def getResult(self):
        return self.result