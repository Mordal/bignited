from pathlib import Path
from collections import defaultdict


def readFile(fileName):
    path = Path(__file__).with_name(fileName)
    while True:
        try:
            with open(path) as f:
                allWordsWithDoubles = [line.strip().lower() for line in f.readlines()]
            break
        
        except FileNotFoundError:
            tekst = input(f'!!! File not found: {path} , please provide the file and press ENTER - or type "END" to exit: ')
            if tekst.upper() == 'END':  
                exit()
        except IOError:
            print(f"Error reading file: {path}")
            exit()

    allWordsWithoutDoubles = removeDoubleWords(allWordsWithDoubles)
    return allWordsWithoutDoubles

def removeDoubleWords(wordList):
   return list(dict.fromkeys(wordList))

def createSortedWord(word):
    return ''.join(sorted(word.lower()))

def getAllWords(fileName):
    allWordsFromFile = removeDoubleWords(readFile(fileName))
    return allWordsFromFile

def printAnagramsByAmount(allAnagrams):
    amountWords=0
    for anagramList in sorted(allAnagrams.values(), key=lambda x: len(x)):
        amountWords += len(anagramList)
        print(anagramList)

    print('------------------------------------------')
    print(f'{amountWords} WORDS FORMED AN ANAGRAM')

def getAllAnagrams(allAnagrams):
    return {key: value for key, value in allAnagrams.items() if len(value)>1}

if __name__ == '__main__':
    allWords = getAllWords('wordlist.txt')
    possibleAnagrams = defaultdict(list)
    for word in allWords:
        sortedWord = createSortedWord(word)
        if sortedWord in possibleAnagrams:
            possibleAnagrams[sortedWord].append(word)
        else:
            possibleAnagrams[sortedWord] = [word]

    allAnagrams = getAllAnagrams(possibleAnagrams)
    printAnagramsByAmount(allAnagrams)
    print('------------------------------------------')
    print(f'{len(allAnagrams)} DIFFERENT ANAGRAMS WERE PRINTED FROM SMALL TO LARGE')
    print('------------------------------------------')