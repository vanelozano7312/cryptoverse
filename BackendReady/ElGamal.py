import random
from math import pow
from sympy import randprime as rand_prime
from math import gcd as bltin_gcd

def prim_roots(p):
    """
    Description
    -----------
    Given a prime number p finds a 
    random primitive root modulo p.

    Parameters
    ----------
    p: int
        Prime number p

    Returns
    -------
    r: int
        Random primitive root modulo p

    """
    o = 1
    while True:
        r = random.randint(2,p)
        k = power(r, o, p)
        while (k > 1):
            o = o + 1
            k = (k * r) % p
        if o == (p - 1):
            return r
        o = 1

def power(a, b, c):
    """
    Description
    -----------
    Computes a^b mod c

    Parameters
    ----------
    a: int
        Base
    b: int
        Exponent
    c: int
        Modulo

    Returns
    -------
    (x % c): int
        a^b mod n
    """
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)

    return x % c

#Para generar automaticamente un primo aleatorio se usa rand_prime().
#Lo mejor es generar uno tan grande como se pueda, puede ser en el intervalo [2^24,2^26].

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
    
    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////

    #To generate randomly:
    #Generate public p:             rand_prime(pow(2,24),pow(2,26))
    #Generate public g:             prim_roots(p)
    #Generate private a:            random.randint(2,2^10)
    #Generate public h:             power(g,a,p)

    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////

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
    Given an encripted list, an integer that encrypts the ephemeral key used, the public prime 'p' 
    and the private key 'a', decrypts the list into the original text.

    Parameters
    ----------
    text: list of integers
        List of encrypted characters
    s1: int
        The integer pair of the list
    a: int
        Private key
    p: int 
        Public key prime number

    Returns
    -------
    dec: string
        Decrypyted text

    """
    dec = []

    s = power(s1,a,p)

    for i in range(0,len(text)):
        dec.append(chr(int(text[i]/s)))

    return ''.join(dec)

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

p = rand_prime(pow(2,24),pow(2,26))
print(p)

g = prim_roots(p)
print(g)

a = random.randint(2,pow(2,10))
print(a)

A = power(g,a,p)
print(A)

enc = elgamal_enc(msg,p,g,A)
s1 = enc[0]
s2 = enc[1]
print(s2)
print(elgamal_dec(s2,s1,a,p))
