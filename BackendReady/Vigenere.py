from BackendReady.Utils import utils

def GetKey(keyword):
    """
    Description
    -----------
    This function returns the numerical equivalent representation
    of the given keyword, this is a list where the i-th value is
    the code of the i-th letter in the keyword.
    
    See GetCode() to see the scheme used for the codes associated
    with the letters.

    Parameters
    ----------
    m : int
        Length of the keyword
    keyword : list
        The numerical equivalent representation of the given keyword
    keyword : string
        The keyword to encrypt
    """
    if type(keyword) == list:
        return keyword
    else:
        key = []
        for c in keyword:
            key.append(utils.GetCode(c))
        
        return key

def encode_vigenere(keyword, text, failures):
    """
    Description
    -----------
    This functions encrypts the given text with the provided keyword. If the
    given keyword is not valid it returns -1. After three tries, the keyword
    is selected randomly

    Parameters
    ----------
    keyword : string
        The keyword to encrypt
    text : string
        Text to encrypt with Vigenere Cipher
    failures : 
        Number of times the user has entered and invalid keyword

    Returns
    -------
    string, string : The first string is the text encrypted and the second one
    is the keyword used
    """
    if len(utils.preProcessText(keyword)) != 0:
            
        text = utils.preProcessText(text)
        keyword = utils.preProcessText(keyword)
        key = GetKey(keyword)
        m = len(key)

        encryptedText = ""
        for i in range(0, len(text)):
            encryptedText += utils.GetLetter((utils.GetCode(text[i]) + (key[i % m])) % 26)
        return encryptedText, keyword

    elif failures >= 2:
        keyword = utils.GetRandomString(utils.GetRandomInteger(len(text)))
        
        text = utils.preProcessText(text)
        keyword = utils.preProcessText(keyword)
        key = GetKey(keyword)
        m = len(key)

        encryptedText = ""
        for i in range(0, len(text)):
            encryptedText += utils.GetLetter((utils.GetCode(text[i]) + (key[i % m])) % 26)
        
        return encryptedText, keyword
    else:
        return -1, -1

def decode_vigenere(keyword, text):
    """
    Description
    -----------
    This functions decrypts the given text with the provided keyword of length m

    Parameters
    ----------
    keyword : string
        The keyword to encrypt
    text : string
        Text to decrypt with Vigenere Cipher
    
    Returns
    -------
    string : The decrypted text using the given keyword
    """
    if len(utils.preProcessText(keyword)) == 0:
        return -1
    
    m = len(keyword)
    keyword = utils.preProcessText(keyword)
    key = GetKey(keyword)

    decryptedText = ""
    for i in range(0, len(text)):
        decryptedText += utils.GetLetter((utils.GetCode(text[i]) - (key[i % m])) % 26)

    return decryptedText

"""
EXAMPLE
print(Encrypt("CIPHER", "This Cryptosystem is not secure", 0))
print(Decrypt("CIPHER", "vpxzgiaxivwpubttmjpwizitwzt"))
"""