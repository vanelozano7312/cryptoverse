from BackendReady.Utils import utils
def CreateSubstrings(m, text):
    """
    Description
    -----------
    Given a text = y_1, y_2, ..., y_n it returns a list with m
    strings y1, y2,.., ym where:

    y1 = y_1, y_m+1, y_2m+1, ...
    y2 = y_2, y_m+2, y_2m+2, ...
    .
    .
    .
    ym = y_m, y_2m, y_3m, ...

    Parameters
    ----------
    m : int
        The number of strings we want to produce
    text : string
        The text used to produce the list with m strings
    
    Returns
    -------
    A list with m strings defined as mentioned above
    """
    text = utils.preProcessText(text)
    substrings = []
    for i in range(0, m):
        currSubstring = ""
        for j in range(i, len(text), m):
            currSubstring += text[j]
        substrings.append(currSubstring)
    return substrings

def GenerateAlphabet():
    """
    Description
    -----------
    Generates a dictionary with the english alphabet
    characters(lowercase) as keys and zero as value
    for each of them

    Returns
    -------
    A dictionary with the english alphabet characters
    (lowercase) as keys and zero as value for each of
    them
    """
    alphabet = {}
    for i in range(97, 97 + 26):
        alphabet[chr(i)] = 0
    return alphabet

def GetFrequencies(text):
    """
    Description
    -----------
    Given a text, it returns a dictionary with the
    frequencies of each english alphabet character
    in the text

    Parameters
    ----------
    text : string
        The text in which we want to find the frequencies
        of each english characters
    
    Returns
    -------
    A dictionary with the frequencies of each english alphabet
    character in the text
    """
    frequencies = GenerateAlphabet()
    for c in text:
        frequencies[c] += 1
    return frequencies

def GetIndexOfCoincidence(text):
    """
    Description
    -----------
    Computes the index of coincidence, defined to be the probability
    that two random elements of the text are identical

    Parameters
    ----------
    text : string
        The string to find its index of coincidence

    Returns
    -------
    A float value which is the index of coincidence of the given text
    """
    n = len(text)
    IOC = 0
    frequencies = GetFrequencies(text)
    for c in frequencies:
        IOC += frequencies[c]*(frequencies[c] - 1)
    return IOC/(n*(n - 1))

def GetAverage(l):
    """
    Description
    -----------
    Computes the average of the given list

    Parameters
    ----------
    l : list
        The list to find its average
    Returns
    -------
    int : The average of the list
    """
    return sum(l) / len(l)

def GuessKeywordLength(k, text):
    """
    Description
    -----------
    Using the index of coincidence for each value from 1 to k
    it tries to find the length of the keyword used to encrypt

    Parameters
    ----------
    k : int
        The biggest guess value for the key length
    text : string
        The text encrypted with the keyword we are looking for
    
    Returns
    -------
    int : The length of the keyword used to encrypt the given text
    """
    lessDiff = 3
    guess = 0
    for m in range(1, k + 1):
        y_m = CreateSubstrings(m, text)
        IOCs = []
        for y in y_m:
            IOCs.append(GetIndexOfCoincidence(y))
        iocsAverage = GetAverage(IOCs)
        diff = abs(0.065 - iocsAverage)
        if diff < lessDiff:
            lessDiff = diff
            guess = m
    return guess

def GuessKeyword(m, text):
    """
    Description
    -----------
    Using a guess for the keyword length it tries to find the 
    keyword used to encrypt the given text

    Parameters
    ----------
    m : int
        The guess for the keyword length
    text : string
        The string encrypted with the keyword we are looking for
    
    Returns
    -------
    string : The potential keyword used to encrypt the given text
    """
    potentialKeyword = ""
    y_m = CreateSubstrings(m, text)
    nPrime = len(text)/m
    for y_i in y_m:
        frequencies = GetFrequencies(y_i)
        minDiff = 3
        potentialGuess = ""
        for g in range(0, 26):
            m_g = M_g(frequencies, nPrime, g)
            if abs(m_g - 0.065) < minDiff:
                minDiff = abs(m_g - 0.065)
                potentialGuess = utils.GetLetter(g)
        potentialKeyword += potentialGuess
    
    return potentialKeyword

def M_g(frequencies, nPrime, g):
    """
    Description
    -----------
    Computes the M_g value for a given frequencies list
    and a shift. See Cryptography: Theory and Practice.
    Stinson 3rd edition, pag 35

    Parameters
    ----------
    frequencies : dictionary
        A dictionary with the frequencies of each english
        alphabet character in y_i string computed with the
        encrypted text
    nPrime : int
        The length of the y_i string
    g : int
        The potential shift
    
    Returns
    -------
    The M_g value for y_i string
    """
    idealDistribution = {
        'a' : 0.082,
        'b' : 0.015,
        'c' : 0.028,
        'd' : 0.043,
        'e' : 0.127,
        'f' : 0.022,
        'g' : 0.020,
        'h' : 0.061,
        'i' : 0.070,
        'j' : 0.002,
        'k' : 0.008,
        'l' : 0.040,
        'm' : 0.024,
        'n' : 0.067,
        'o' : 0.075,
        'p' : 0.019,
        'q' : 0.001,
        'r' : 0.060,
        's' : 0.063,
        't' : 0.091,
        'u' : 0.028,
        'v' : 0.010,
        'w' : 0.023,
        'x' : 0.001,
        'y' : 0.020,
        'z' : 0.001
    }
    m_g = 0
    for i in range(0, 25):
        m_g += (idealDistribution[utils.GetLetter(i)] * frequencies[utils.GetLetter((i + g) % 25)]) / nPrime
    return m_g

"""
Example
text = "CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBWRVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAKLXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELXVRVPRTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHRZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJTAMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBIPEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHPWQAIIWXNRMGWOIIFKEE"
text = utils.preProcessText(text)
print(GuessKeywordLegth(7, text))
print(GuessKeyword(5, text))
"""