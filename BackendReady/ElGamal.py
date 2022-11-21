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
    Encrypts a clear text given the coordinates of a public key
    over the elliptic curve NIST P-256.

    When input from user is incorrect 3 times, for example to give a coordinate outside the curve,
    the function will randomly assume a private key 'a' and the corresponding public key coordinates.
    
    Parameters
    ----------
    text: string
        Clear text to encrypt
    pub_k_x: int
        Coordinate in x of the public key
    pub_k_y: int
        Coordinate in y of the public key
    count_fallas: int
        Count of bad input from user

    Returns
    -------
    (S1.pointQ.x,S1.pointQ.y): Tuple of int
        Part of the encrypted message 'S1' corresponding to the public counterpart of the
        ephemeral key 'k'
    S2: List of tuples of int
        List where every tuple corresponds to the coordinates of every encrypyed letter of the message
    pub_k.pointQ.x: int
        Coordinate in x of the public key used to encrypt
    pub_k.pointQ.y: int
        Coordinate in y of the public key used to encrypt
    a: int
        Private key used to generate the public key to encrypt if needed to randomize.
        If the user gave correct parameters and the function didn't randomly generate 
        returns (-1)
    """

    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////

    #To generate randomly:
    #Generate private key a:                random.randint(2,pow(10,50))
    #Generate public key in the curve:      ECC.construct(curve = 'P-256', d = a).public_key()

    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////
    #/////////////////////////////////////////////////////////////

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
    Given the x and y coordinates of S1 and a list of coordinates S2 product of an elgamal ECC and the 
    private key 'a' returns the clear decrypted text.

    Parameters
    ----------
    s1_x: int
        x coordinate of S1
    s1_y: int
        y coordinate of S1
    s2: List of integer tuples
        List of coordinates being every coordinate an encrypted letter
    a: int 
        Private key

    Returns
    -------
    text: string
        Clear decrypted text.
        (-1) if the parameters are out of bounds    
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

# p = rand_prime(pow(2,24),pow(2,26))
# g = prim_roots(p)
# a = random.randint(2,2^10)
# h = power(g,a,p)
# print(p, g, a, h)
# print(elgamal_enc('askjfhaskjf',p,g,h,1))

# p = 42004813
# g = 7597416
# a = random.randint(2,2^10)
# h = 28025900

# print(elgamal_enc('askjfhaskjf', p, g, h, 0))

# p=39577913
# a=5
# s1=15151015
# text="[500024720, 533680230, 519256440, 466369210]"
# text = str_to_list(text)
# print(elgamal_dec(text, s1, a, p))

s11=101677601383488996603075606535380255913010825269751815769841498664861664196811
s12=13773740408660364011136485548507825733693522803178641816330243385508794177318
s2="[(100496040572723822934014757929413114100665887872085620547350405136730667827870, 11891784355483902878420332758254726272363245351700905244072721670011843095230), (8459579126204352643407501919024558721938392553927414518975256116869977596062, 15331667878075208381306875463013169571040001120005414383843820657260996309916), (63585599298583948292450817100721955471936610691296952417434272025052465189539, 115594602241206645993104028328760770511057139783849136013195948214649174654810), (88676361745046123069790464985751564899090966340535587979919104072725408960877, 48085515339909112600553883066276515839924106387251701126694562793231124542056), (108868155680714357461498365085860541962634841613942544335336385814513262407664, 64747336522822438799697023904881487219791681139116515168766305265359278982931), (103687670218257693414125117510826151548340956699690369706564851224691769253617, 4096153036426876202722232016627631216992890943478348602103866440979888546193)]"
a= 12061096845004200634431039739511748362955237408440