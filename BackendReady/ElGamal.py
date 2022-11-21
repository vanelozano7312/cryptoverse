import random
from math import pow
from sympy import randprime as rand_prime
from sympy import isprime as isprime
from math import gcd as bltin_gcd
from Crypto.PublicKey import ECC

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

def is_prime_root(r,p):
    o = 1
    k = power(r,o,p)
    while k > 1:
        o = o + 1
        k = (k * r) % p
    if o == (p - 1):
        return True
    return False


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

def elgamal_enc(text,p,g,h,count_fallas):
    """
    Description
    -----------
    Given a text and the public key integers 
    returns the S1 and S2 integers corresponding to
    the encryption.

    Because you must return an integer for every character 
    in the text the S2 variable is a list of integers.

    When user inputs invalid parameters 3 times the function will generate
    these automatically.

    Parameters
    ----------
    text: string
        Text to encrypt
    p: int 
        Public prime                    (p is prime)                
    g: int                          
        Element of Z_p                  (g < p)
    h: int
        Public integer h = g^a mod p    (h < p)
    count_fallas: int
        User mistake counter

    Returns
    -------
    If parameters where invalid and (count_fallas < 3)
    (-1,-1,-1,-1,-1,-1) will be returned

    S1: int
        Integer corresponding to g^k mod p
    S2: list of int
        List of integers c*(h^k mod p), each corresponding 
        to a character 'c' of 'text' 
    p: int
        Prime 'p' upon which the algorithm ran
    g: int
        Element of Z_p upon which the algorithm ran
    h: int
        Element of Z_p 'h = g^a mod p'
    a: int
        Private key 'a' randomly generated to compute 'h', 
        (-1) if no data was generated randomly
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

    pi = p
    gi = g
    a = -1
    hi = h

    if count_fallas>=3:
        pi = rand_prime(pow(2,24),pow(2,26))
        gi = prim_roots(pi)
        a = random.randint(2,2^10)
        hi = power(gi,a,pi)

    if not isprime(pi):
        return -1,-1,-1,-1,-1,-1
    if gi >= pi:
        return -1,-1,-1,-1,-1,-1
    if h >= pi:
        return -1,-1,-1,-1,-1,-1

    S2 = []
    k = random.randint(2,pi)

    S1 = power(gi,k,pi)

    for i in range(len(text)):
        S2.append(ord(text[i])*power(hi,k,pi))

    return S1,S2,pi,gi,a,hi

     

def elgamal_dec(text,s1,a,p):
    """
    Description
    -----------
    Given an encripted list, an integer that encrypts the ephemeral key used, the public prime 'p' 
    and the private key 'a', decrypts the list into the original text.

    If the given parameters are invalid it returns (-1)

    Parameters
    ----------
    text: list of integers
        List of encrypted characters
    s1: int
        The integer pair of the list    (s1 < p1)
    a: int
        Private key
    p: int                              (p is prime) 
        Public key prime number

    Returns
    -------
    dec: string
        Decrypyted text
        (-1) if parameters where invalid

    """
    if not isprime(p):
        return -1
    if s1 >= p:
        return -1

    dec = []

    s = power(s1,a,p)

    for i in range(0,len(text)):
        dec.append(chr(int(text[i]/s)))

    return ''.join(dec)

def elgamal_ecc_e(text,pub_k_x,pub_k_y,count_fallas):
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """
    a = -1
    if count_fallas >= 3:
        a = random.randint(2,pow(10,50))
        pub_k = ECC.construct(curve = 'P-256', d = a).public_key()
    else:
        try:
            pub_k = ECC.construct(curve = 'P-256', point_x = pub_k_x, point_y = pub_k_y)
        except ValueError:
            return -1,-1,-1,-1

    S2 = []
    k = random.randint(2,pow(10,50))
    S1 = ECC.construct(curve = 'P-256', d = k).public_key()
    for i in range(len(text)):
        S2.append(k * pub_k.pointQ + ECC.construct(curve = 'P-256', d = ord(text[i])).pointQ)
        S2[i] = (int(S2[i].x),int(S2[i].y))

    return (S1.pointQ.x,S1.pointQ.y),S2,pub_k.pointQ.x,pub_k.pointQ.y,a


def elgamal_ecc_d(s1_x,s1_y,s2,a):
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """
    try:
        S1 = ECC.construct(curve = 'P-256', point_x = s1_x, point_y = s1_y)
    except ValueError:
        return -1

    text = []

    S = a*S1.pointQ
    for i in range(len(s2)):
        try:
            C = ECC.construct(curve = 'P-256', point_x = s2[i][0], point_y = s2[i][1]).pointQ
        except ValueError:
            return -1
        text.append(C + (-S))
    for i in range(len(text)):
        for j in range(97,123):
            if ECC.construct(curve = 'P-256', d = j).pointQ == text[i]:
                text[i] = chr(j)
                break
        if type(text[i]) != type(''):
            text[i] = ' '
    
    return ''.join(text)


a = 15
pr_key = ECC.construct(curve='P-256',d=a)
pub_key = pr_key.public_key()

k=  12984129847129
M = 12
kP= ECC.construct(curve='P-256',d=k).public_key()
M = ECC.construct(curve='P-256',d=M).pointQ
C = k * pub_key.pointQ + M

S = a*kP.pointQ

d_M = C + (-S) 
print(d_M == M)
for i in range(1,25):
    if ECC.construct(curve='P-256',d=i).pointQ==d_M:
        print("esta es")
        print(i)
        break

enc = elgamal_ecc_e('patacon patacon',pub_key.pointQ.x,pub_key.pointQ.y,0)
print(elgamal_ecc_d(enc[0][0],enc[0][1],enc[1],a))