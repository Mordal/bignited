from io import StringIO
import unittest
from unittest.mock import patch
from anagrams import *

class TestAnagrams(unittest.TestCase):

    def test_getAllAnagrams_emptyDict(self):
        # Test with an empty dictionary
        self.assertEqual(getAllAnagrams({}), {})
        
    def test_getAllAnagrams_noAnagrams(self):
        # Test with a dictionary containing no anagrams
        allAnagrams = {'abc': ['abc'], 'def': ['def'], 'xyz': ['zyx']}
        self.assertEqual(getAllAnagrams(allAnagrams), {})

    def test_getAllAnagrams_oneAnagram(self):
        # Test with a dictionary containing one anagram
        allAnagrams = {'act': ['cat', 'act', 'tac']}
        expected = {'act': ['cat', 'act', 'tac']}
        self.assertEqual(getAllAnagrams(allAnagrams), expected)

    def test_getAllAnagrams_FiltersOutSingleItemList(self):
        # Test with a dictionary containing one anagram and one single item list
        allAnagrams = {'act': ['cat', 'act', 'tac'], 'eel': ['lee']}
        expected = {'act': ['cat', 'act', 'tac']}
        self.assertEqual(getAllAnagrams(allAnagrams), expected)

    def test_getAllAnagrams_WithMultipleAnagrams(self):
        # Test with a dictionary containing multiple anagrams and multiple single item lists
        allAnagrams = {'act': ['cat', 'act', 'tac'], 'singel1': ['singel1'],'singel2': ['singel2'], 'singel3': ['singel3'], 'eel': ['eel', 'lee'], 'eelr': ['leer', 'reel'], 'ops': ['sop', 'ops'], 'elst': ['lets', 'lest', 'stel', 'elts'], 'dgo': ['dog', 'god'], 'ast': ['tas', 'sat', 'ast'], 'aet': ['tea', 'ate', 'eat'], 'ers': ['res', 'ser', 'ers'], 'dei': ['die', 'ide']}
        expected = {'act': ['cat', 'act', 'tac'], 'eel': ['eel', 'lee'], 'eelr': ['leer', 'reel'], 'ops': ['sop', 'ops'], 'elst': ['lets', 'lest', 'stel', 'elts'], 'dgo': ['dog', 'god'], 'ast': ['tas', 'sat', 'ast'], 'aet': ['tea', 'ate', 'eat'], 'ers': ['res', 'ser', 'ers'], 'dei': ['die', 'ide']}
        self.assertEqual(getAllAnagrams(allAnagrams), expected)

    def test_removeDoubleWords(self):
        wordListWithDoubles = ['apple', 'banana', 'cherry', 'apple', 'banana']
        wordListWithoutDoubles = ['apple', 'banana', 'cherry']
        self.assertEqual(removeDoubleWords(wordListWithDoubles), wordListWithoutDoubles)

    def test_createSortedWord(self):
        word = 'apple'
        sortedWord = 'aelpp'
        self.assertEqual(createSortedWord(word), sortedWord)

    def test_getAllWords(self):
        fileName = 'test_wordlist.txt'
        with open(fileName, 'w') as f:
            f.write('apple\nbanana\ncherry\ncherry\ncherry\n')
        allWords = ['apple', 'banana', 'cherry']
        self.assertEqual(getAllWords(fileName), allWords)
        import os
        os.remove(fileName)

    def test_printAnagramsByAmount(self):
        allAnagrams = {
            'ast': ['tas', 'sat', 'ast'],
            'act': ['cat', 'act', 'tac'],
            'aelpp': ['apple', 'pepla'],
            'cehrry': ['cherry', 'rhycer']        
        }
        expectedOutput = "['apple', 'pepla']\n['cherry', 'rhycer']\n['tas', 'sat', 'ast']\n['cat', 'act', 'tac']\n------------------------------------------\n10 WORDS FORMED AN ANAGRAM\n"
        with patch('sys.stdout', new_callable=StringIO) as fake_output:
            printAnagramsByAmount(allAnagrams)
            self.assertEqual(fake_output.getvalue(), expectedOutput)

if __name__ == '__main__':
    unittest.main()