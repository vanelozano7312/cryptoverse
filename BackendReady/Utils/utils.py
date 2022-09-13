import random
import string

def GetCode(c):
    """
    Description
    -----------
    Using the correspondence a <-> 0, b <-> 1, ... , z <-> 25
    we associate to each character its corresponding numeric
    value.

    This function returns the corresponding numeric value 
    associated with the given character, according to the
    scheme described above.
    """
    return ord(c) - 97

def GetLetter(n):
    """
    Description
    -----------
    Using the correspondence a <-> 0, b <-> 1, ... , z <-> 25
    we associate to each character its corresponding numeric
    value.

    This function returns the corresponding letter asociated
    with the given value, according to the scheme described 
    above.
    """
    return chr(n + 97)

def GetRandomInteger(n):
    """
    Description
    -----------
    This function returns a random integer from 1 to n inclusive
    """
    return random.randint(1, n)

def GetRandomString(n):
    """
    Description
    -----------
    This function returns a random string of length n in lower
    case with letters from a to z
    """
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    randomString = ''.join(random.choice(letters) for i in range(n))
    return randomString

def preProcessText(text):
    """
    Description
    -----------
    This function returns the given text in lowercase without
    spaces and not english alphabet characters.
    """
    text = text.replace(' ', '')
    text = text.lower()
    processedText = ""
    for c in text:
        if ord(c) >= 97 and ord(c) <= 97 + 25:
            processedText += c
    return processedText

def IsValidMatrix(m):
    if len(m) != len(m[0]):
        raise "The matrix is not square"