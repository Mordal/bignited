import string

#string. contains a collection of string constants whith for example all ascii-lowercase characters, which is used in this script.
#string constant is transformed in a list

def ShiftString(shift, str):
    LETTERS = list(string.ascii_lowercase)
    shiftedString = ""
    for letter in str:
        #if the letter from the given string is an ascii letter -> perform shift operation
        if letter in list(string.ascii_letters):
            try:
                oldLetterIndex = LETTERS.index(letter.lower()) #potential upercase letters are converted to lowercase
                newLetterIndex = (oldLetterIndex + shift) % len(LETTERS) #to handle a loop around of the list, modulo (%) is used to get the remainder..blabla math
                shiftedString += LETTERS[newLetterIndex]
            except:
                #catch non-integer shifts
                shiftedString = " - ERROR: Crazy input - "
                break
        else:
            shiftedString = " - ERROR: Crazy input - "
            break
    return shiftedString
