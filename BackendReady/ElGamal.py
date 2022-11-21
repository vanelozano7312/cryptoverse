import random
from math import pow

# Modular exponentiation
def power(a, b, c):
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c

def elgamal_enc(text,p,g,h):
    """
    Description
    -----------
    Given a text and the public key integers 
    returns the S1 and S2 integers corresponding to
    the encryption.

    Because you must return an integer for every character 
    in the text the S2 variable is a list of integers.

    Parameters
    ----------
    text: string
        Text to encrypt
    p: int
        Public prime
    g: int
        Element of Z_p
    h: int
        Public integer h = g^a mod p

    Returns
    -------
    S1: int
        Integer corresponding to g^k mod p
    S2: list of int
        List of integers c*(h^k mod p), each corresponding 
        to a character 'c' of 'text' 
    """
    S2 = []
    k = random.randint(2,p)

    S1 = power(g,k,p)

    for i in range(len(text)):
        S2.append(ord(text[i])*power(h,k,p))

    return S1,S2

     

def elgamal_dec(text,s1,a,p):
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """
    dec = []

    s = power(s1,a,p)

    for i in range(0,len(text)):
        dec.append(chr(int(text[i]/s)))

    return dec

def elGamalECCE():
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """


def elGamalECCD():
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """

msg = "encryption"

p = 29

g = 15

a = 3

A = power(g,a,p)

enc = elgamal_enc(msg,29,15,A)
s1 = enc[0]
s2 = enc[1]
print(s2)
print(elgamal_dec(s2,s1,a,p))