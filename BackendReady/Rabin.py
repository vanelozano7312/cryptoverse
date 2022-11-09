import random

first_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733, 1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877, 1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017, 2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143, 2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297, 2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423, 2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593, 2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713, 2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851, 2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011, 3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181, 3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323, 3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467, 3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571]

def StringToASCII(plaintext):
    plaintext_list = []
    for c in plaintext:
        plaintext_list.append(ord(c))
    return plaintext_list

def ASCIIToString(ascii_list):
    plaintext = ""
    for i in ascii_list:
        plaintext += chr(i)
    return plaintext

def ASCIIToHex(ascii_list):
    hex_text = ""
    for i in ascii_list:
        if len(hex(i)[2:]) < 2:
            hex_text += '0'
        hex_text += hex(i)[2:]
    return hex_text

def HexToASCII(hex_text):
    ascii_list = []
    for i in range(0, len(hex_text), 2):
        letter = hex_text[i] + hex_text[i+1]
        ascii_list.append(int(letter, base=16))
    return ascii_list

def MapString(plaintext):
    ascii_text = StringToASCII(plaintext)
    #print(ascii_text)
    hex_text = ASCIIToHex(ascii_text)
    #print(hex_text)
    code = int(hex_text, base=16)
    return code

def GetString(code):
    hex_text = hex(code)[2:]
    if len(hex_text) % 2 != 0:
        hex_text = '0' + hex_text
    ascii_list = HexToASCII(hex_text)
    plaintext = ASCIIToString(ascii_list)
    return plaintext
    
"""
Map string texts

texts = ["panela", "iguana", "almojabana", "granola", "zocalo", "rae", "cerdo", "fem", "ricardo", "violin", "hoja", "simio"]
ciphertexts = []
for text in texts:
    ciphertexts.append(MapString(text))

for i in range(0, len(ciphertexts)):
    plaintext = GetString(ciphertexts[i])
    if plaintext != texts[i]:
        print("FAIL!")
        print(plaintext, texts[i])
        break
"""
def nBitRandom(n):
   
    # Returns a random number
    # between 2**(n-1)+1 and 2**n-1'''
    return(random.randrange(2**(n-1)+1, 2**n-1))

def getLowLevelPrime(n):
    while True:
        prime_candidate = nBitRandom(n)

        not_prime = False
        for divisor in first_primes:
            if (prime_candidate % divisor == 0) and (divisor**2 <= prime_candidate):
                not_prime = True
                break
        
        if not not_prime:
            return prime_candidate

def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True

def GeneratePrimeNumber(n):
    while True:
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        elif prime_candidate % 4 != 3:
            continue
        else:
            return prime_candidate

def gcdExtended(a, b):
    """
    Description
    -----------
    From number theory we have ax + by = gcd(a, b). This function
    finds the value of x,y and the gcd, given a, b, and returns
    them

    Parameters
    ----------
    a: int
        First number to get the gcd
    b: int
        Second number to get the gcd
    
    Returns
    -------
    gcd : int
        The gcd(a,b)
    x : int
        The coefficient of a in the formula ax + by = gcd(a,b)
    y : int
        The coefficient of b in the formula ax + by = gcd(a,b)
    """
    # Base Case
    if a == 0 :
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a)
     
    # Update x and y using results of recursive
    # call
    x = y1 - (b//a) * x1
    y = x1
    
    return gcd,x,y

def power(x, y, p) :
    res = 1     # Initialize result
 
    # Update x if it is more
    # than or equal to p
    x = x % p
     
    if (x == 0) :
        return 0
 
    while (y > 0) :
         
        # If y is odd, multiply
        # x with result
        if ((y & 1) == 1) :
            res = (res * x) % p
 
        # y must be even now
        y = y >> 1      # y = y/2
        x = (x * x) % p
         
    return res

def encode_rabin(plaintext, n):
    code = MapString(plaintext)
    print("code: " + str(code))
    if code >= n:
        return -1
    return power(code, 2, n)

def decode_rabin(cipher_number, p, q, n):
    try:
        m_p = power(cipher_number, round((p + 1)//4), p)
        m_q = power(cipher_number, round((q + 1)//4), q)
        gcd, y_p, y_q = gcdExtended(p, q)
        r_1 = (y_p*p*m_q + y_q*q*m_p) % n
        r_2 = n - r_1
        r_3 = (y_p*p*m_q - y_q*q*m_p) % n
        r_4 = n - r_3
        return GetString(r_1), GetString(r_2), GetString(r_3), GetString(r_4)
    except:
        return -1

"""
text = "amazing grace, how sweet that song"
length = 8*len(text) + 1
p = GeneratePrimeNumber(length//2)
q = GeneratePrimeNumber(length//2)
n = p*q
print(p)
print(q)
print(n)
cipher_number = encode_rabin(text, n)
print(cipher_number)
plaintext = decode_rabin(cipher_number, p, q, n)
print(plaintext)
"""

