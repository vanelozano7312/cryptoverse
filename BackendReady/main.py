import random as ran
from math import gcd 
import re
from sympy import isprime
from sympy import nextprime

#///////////////////////////////////////////////////////////////
#//////////////////////FUNCIONES GENERALES///////////////////
#////////////////////////////////////////////////////////////////

#Convierte un string en una lista de enteros
def str_to_list(string):
  try:
    string = string.replace("]", '')
    string = string.replace("[", '')
    string = string.split(", ")
    lista=[]
    for i in string:
      lista.append(int(i))
    return lista      
  except:
    return -1
  
#Convierte un string en una lista de coordenadas
def str_to_coor(string):
  try:
    string = string.replace("]", '')
    string = string.replace("[", '')
    string = string.split("), (")
    string[0] = string[0].replace("(", '')
    string[len(string)-1] = string[len(string)-1].replace(")", '')
    for i in range(0, len(string)):
      string[i]=string[i].split(", ")
      string[i][0]=int(string[i][0])
      string[i][1]=int(string[i][1])
    return string
  except:
    return -1
  
# print(str_to_list("[1, 2, 3, 4, 5, 1234567, 1234567, 23456, 098]"))
print(str_to_coor("[(1, 2), (2, 3), (123456, 23456), (12, 234)]"))

def rela_primes():
  lista = []
  for i in range(26): 
    if gcd(26, i) == 1:
      lista.append(i)
  return lista 


def inver_primes():
  lista_primes = rela_primes()
  lista_inver = []
  for i in lista_primes:
    for j in range(30):
      if (i*j)%26 == 1:
        lista_inver.append(j)
        break
  return lista_inver

 
## agregar ignorar lo que no sean letras y pasar las mayus a minus 

def unify(palabra):
  palabralist = []
  palabra = palabra.replace(" ", "")
  palabra = palabra.lower()
  regex = re.compile('[^a-z]')
  palabra = regex.sub('', palabra)
  for i in range(len(palabra)):
    palabralist.append(palabra[i])
  return palabralist
  
def convert (list):
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  count = 0
  for i in list:
    for j in range(len(lista)):
      if i == lista[j]:
        list[count]= j
        continue

    count = count + 1
  return list

  
def deconvert(list):
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  string = ""
  for i in range(len(list)):
    list[i] = lista[int(list[i])]
    string = string + list[i]
  return string

def strtomat(string, m):
  if len(string)%m != 0:
    return -1
  else:
    temp = [string[index: index + m] for index in range(0, len(string), m)]
    result = [list(element) for element in temp]
    for i in range(0, m):
        for j in range(0, m):
            result[i][j]=int(result[i][j])
    return result


def rsakeygen():
  p = nextprime(150)
  q = nextprime(200)
  #n = p*q
  phi = (p-1)*(q-1)
  flag = True
  while flag == True:
    e = ran.randint(3,phi-2)
    if gcd(e, phi) == 1:
      flag = False
  flag = True
  i = 0
  while flag == True:
    if (i*e)%phi==1:
      d=i
      flag = False
    i = i + 1
  return p,q,e,d
#///////////////////////////////////////////////////////////////
#//////////////////////METODOS DE CODIFICACION///////////////////
#////////////////////////////////////////////////////////////////

###LIMPIO
def encode_despla(palabrast,key,count_falla):

  # This codification method receives a message, and a key
  # From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
  # The key is required to be between 1 and 25.
  # If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
  # Understanding a<->0, b<->1, ..., z<->25 the codification method transforms each letter to its corresponding numerical value.
  # The codification method adds the key value to each number and transforms the result back to an alphabetical value.
  # Then returns the message encrypted
  
  palabrals = unify(palabrast)
  if count_falla > 2:
    key = ran.randint(1,26)
    palabrals = convert(palabrals)
    for i in range(len(palabrals)):
      palabrals[i] = (palabrals[i] + key)%26
    palabrast = deconvert(palabrals)
    print(palabrast)
    return palabrast, key
  elif 1 <= key <= 26:
      palabrals = convert(palabrals)
      for i in range(len(palabrals)):
        palabrals[i] = (palabrals[i] + key)%26
      palabrast = deconvert(palabrals)
      print(palabrast)
      return palabrast, key
  else:
    return -1, -1

####LIMPIO
def encode_mult(palabrast,key,count_falla):
  # This codification method receives a message, and a key
  # From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
  # The key is required to be in the list of relative prime numbers with 26.
  # If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
  # Understanding a<->0, b<->1, ..., z<->25 the codification method transforms each letter to its corresponding numerical value.
  # The codification method adds the key value to each number and transforms the result back to an alphabetical value.
  # Then returns the message encrypted
  
  palabrals = unify(palabrast)
  claves_validas = rela_primes()
  if count_falla > 2:
    key = claves_validas[ran.randint(1,len(claves_validas))]
    palabrals = convert(palabrals)
    for i in range(len(palabrals)):
      palabrals[i] = (palabrals[i] * key)%26
    palabrast = deconvert(palabrals)
    return palabrast, key
  
  if key in claves_validas:
      palabrals = convert(palabrals)
      for i in range(len(palabrals)):
        palabrals[i] = (palabrals[i] * key)%26
      palabrast = deconvert(palabrals)
      return palabrast, key
  
  else:
    return -1,-1

def encode_sust(palabrast,key,count_falla):
  
  # This codification method receives a message, and a key
  # From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
  # The key is a list of letters that, in order, replace one of the characters in the message. non alphabet characters and duplicates are not allowed
  # If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
  # The codification method substitutes each letter by its replacement as stated in the key.
  # Then returns the message encrypted
  

  dic = {'a':"", 'b':"", 'c':"", 'd':"", 'e':"", 'f':"", 'g':"", 'h':"", 'i':"", 'j':"", 'k':"", 'l':"",'m':"", 'n':"", 'o':"", 'p':"", 'q':"", 'r':"", 's':"", 't':"", 'u':"", 'v':"", 'w':"", 'x':"", 'y':"", 'z':""}
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  palabrals = unify(palabrast)
  count = 0
  key = key.lower()
  if count_falla > 2:
    listaran = lista[:]
    ran.shuffle(listaran)
    key = ""
    for item in listaran:
      key = key + item
    for item in key:
      if item not in dic.values():
        dic[lista[count]] = item
  elif len(key) != 26:
    return -1,-1
  for item in key:
    if item not in lista:
      return -1, -1
    else:
      if item not in dic.values():
        dic[lista[count]] = item
        count = count + 1
      else:
        return -1, -1 
  string = ""
  for i in range(len(palabrals)):
    palabrals[i] = dic[palabrals[i]]
    string = string + palabrals[i]
  return string, key

####LIMPIO
def encode_afin(palabrast, a, b, count_falla):
  
  # This codification method receives a message, and a key
  # From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
  # The key is composed by a and b, for a it needs to be in the list of relative primes of 26 and b requires it to be between 1 and 25.
  # If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
  # Understanding a<->0, b<->1, ..., z<->25 the codification method transforms each letter to its corresponding numerical value.
  # The codification method multiplies a and ads b to each number and transforms the result back to an alphabetical value.
  # Then returns the message encrypted
  
  palabrals = unify(palabrast)
  claves_validas = rela_primes()
  if count_falla > 2:
    a = claves_validas[ran.randint(1,len(claves_validas))]
    b = ran.randint(1,25)
    palabrals = convert(palabrals)
    for i in range(len(palabrals)):
      palabrals[i] = (((palabrals[i] * a)%26)+b)%26
    palabrast = deconvert(palabrals)
    return palabrast, a, b
  
  if a in claves_validas:
    if 0 <= b <= 25:
      palabrals = convert(palabrals)
      for i in range(len(palabrals)):
        palabrals[i] = (((palabrals[i] * a)%26)+b)%26
      palabrast = deconvert(palabrals)
      return palabrast, a, b
    else:
      return -1,-1, -1
  else:
    return -1,-1, -1


def encode_permu(string, tama, key, count_falla):
  
  # This codification method receives a message, and a key
  # From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
  # The key is composed by a and b, a needs to bea positive number lower than the length of the processed text, b requires to be between 1 and a.
  # If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
  # The codification method takes chunks of size a and moves each letter b spaces to the right, if the letter is in the last position of the chunk, it goes back to the first.
  # Then returns the message encrypted
  
  
  palabrals = unify(string)
  if count_falla > 2:
    tama = ran.randint(1,len(palabrals))
    key = ran.randint(1,tama -1)
    print("a")
  while True:
    if 1 <= tama <=len(palabrals):
      break
    
    print("b")
    return -1, -1, -1
  while True:
    if 1<= key < tama:
      break
    
    print("c", key, tama)
    return -1, -1, -1
  chunks = [palabrals[x:x+tama] for x in range(0, len(palabrals), tama)]
  final=[]
  for x in chunks:
    test = []
    for i in range(key):
      test.append(x[(len(x)-(key-i))%len(x)])
      if(i>=len(x)-1):
        break
    for i in range(len(x)-key):
      test.append(x[i])
    final.extend(test)
  final = convert(final)
  final = deconvert(final)
  return final, tama, key

    
def rsaencript(palabra,p,q,e,d,fallas):
  if fallas > 2:
    p,q,e,d = rsakeygen()
  n = p*q
  phi = (p-1)*(q-1)
  if isprime(p) == False:
    return -1,-1,-1,-1,-1
  if isprime(q) == False:
    return -1,-1,-1,-1,-1 
  if gcd(e, phi) != 1:
    return -1,-1,-1,-1,-1  
  if (d*e)%phi != 1:
    return -1,-1,-1,-1,-1  
  palabra =unify(palabra)
  palabralist = convert(palabra)
  for i in range(len(palabralist)):
    palabralist[i] = (palabralist[i]**e)%n
  
  return palabralist,p,q,e,d

# print(rsaencript("estamos", 151, 211, 26801, 23201, 0))
# print(rsaencript("estamos", 1, 1, 1, 1, 3))

#///////////////////////////////////////////////////////////////
#//////////////////////METODOS DE DECODIFICACION///////////////////
#////////////////////////////////////////////////////////////////


def decode_despla(string, key, count_fallas):
  if count_fallas>2:
    all=[]
    for i in range(25):
      lista = unify(string)
      lista = convert(lista)
      for j in range(len(lista)):
        lista[j] = (lista[j]-1)%26
      string = deconvert(lista)
      all.append("Key used " + str(i+1) + " :    " + string)

    return all
  if 1<= key<=26:
    lista = unify(string)
    lista = convert(lista)
    for j in range(len(lista)):
      lista[j] = (lista[j]-key)%26
    string = deconvert(lista)
    return string
  else:
    return -1


def decode_mult(string, key, count_fallas):
  inver_validas = inver_primes()
  keys = rela_primes()
  results = []
  if count_fallas > 2:
    for i in inver_validas:
      lista = unify(string)
      lista = convert(lista)
      for j in range(len(lista)):
        lista[j] = int((lista[j]*i)%26)
      res = deconvert(lista)
      for a in range(len(inver_validas)):
        if inver_validas[a] == i:
          valor = keys[a]
      results.append("Key used "+ str(valor) + " :     "+res)
    return results, key
  
  if key in keys:
    lista = unify(string)
    lista = convert(lista)
    for i in range(len(keys)):
      if keys[i] == key:
        a = inver_validas[i]
    for j in range(len(lista)):  
      lista[j] = int((lista[j]*a)%26)
    string = deconvert(lista)
    return string, key
  else:
    return -1,-1

#LIMPIO
def decode_sust(palabrast,key,count_falla):
  dic = {'a':"", 'b':"", 'c':"", 'd':"", 'e':"", 'f':"", 'g':"", 'h':"", 'i':"", 'j':"", 'k':"", 'l':"",'m':"", 'n':"", 'o':"", 'p':"", 'q':"", 'r':"", 's':"", 't':"", 'u':"", 'v':"", 'w':"", 'x':"", 'y':"", 'z':""}
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  palabrals = unify(palabrast)
  count = 0
  keyf = key.lower()
  if count_falla > 2:
    listaran = lista[:]
    ran.shuffle(listaran)
    keyf = ""
    for item in listaran:
      keyf = keyf + item
    for item in keyf:
      if item not in dic.values():
        dic[lista[count]] = item
  elif len(keyf) != 26:
    return -1,-1
  for item in keyf:
    if item not in lista:
      return -1, -1
    else:
      if item not in dic.values():
        dic[lista[count]] = item
        count = count + 1
      else:
        return -1, -1 
  string = ""
  for i in range(len(palabrals)):
    palabrals[i] = list(dic.keys())[list(dic.values()).index(palabrals[i])]
    string = string + palabrals[i]
  return string, keyf

def decode_afin(string, a, b, count_fallas):
  
  alf = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  lista = unify(string)
  claves_validas = rela_primes()
  inversas_validas = inver_primes()
  if a in claves_validas:
    for i in range(len(claves_validas)):
      if claves_validas[i] == a:
        ai = inversas_validas[i]
    if 0 <= b <= 25:
      palabrals = convert(lista)
      for i in range(len(palabrals)):
        palabrals[i] = (((palabrals[i] - b)%26)*ai)%26
      palabrast = deconvert(palabrals)
      print(palabrast)
      return palabrast, a, b
    else:
      return -1,-1,-1
  else:
    return -1,-1,-1


def permufiesta(palabra,m,l):
  chunks = [palabra[x:x+m] for x in range(0, len(palabra), m)]
  final=[]
  for x in chunks:
    test = []
    for i in range(l,len(x)):
      test.append(x[i])
    for i in range(l):
      test.append(x[i])
      if(i>=len(x)-1):
        break
    final.extend(test)
  final = convert(final)
  final = deconvert(final)
  return final, m, l

#### LIMPIO
def decode_permu(string, tama, key, count_falla):
  palabra = unify(string)
  if count_falla > 2:
    final = []
    for i in range(1,len(palabra)+1):
      for j in range(i):
        palabra, tama, key = permufiesta(palabra,i,j)
        final.append("Size: "+str(tama) + " Key: "+str(key)+ " Cleartext:" + str(palabra))
    return final
  if 1 <= tama <= len(palabra):
    if 1 <= key < tama:
      palabra, tama, key = permufiesta(palabra,tama,key)
      return palabra, tama, key
    else:
      return -1
  else:
    return -1

#/////////////////////////////////////////////////
#//////////////CRYPTOANALISIS/////////////////////
#/////////////////////////////////////////////////


def analisis_afin(string):
  alf = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  dic={}
  lista = unify(string)
  claves_validas = rela_primes()
  inversas_validas = inver_primes()
  for item in lista:
    if item not in dic.keys():
      dic[item] = 1
    else:
      dic[item] = dic[item]+1
  dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse = True))
  dict_items = dic.items()
  first_two = list(dict_items)[:6]
  for x in range(6):
    for y in range(6):
      if x == y:
        continue
      e= "e"
      ei = first_two[x][0]
      t = "t"
      ti = first_two[y][0]
      for i in range(len(alf)):
        if alf[i] == e:
          e = i
        if alf[i] == ei:
          ei = i 
        if alf[i] == t:
          t = i
        if alf[i] == ti:
          ti = i
      a = e - t
      c = ei - ti
      signoa = a/abs(a)
      signoc = c/abs(c)
      if abs(a) not in claves_validas:
        return -1,-1,-1
      else:
        for i in range(len(claves_validas)):
          if claves_validas[i] == abs(a):
            a = inversas_validas[i]
        lista = unify(string)
        ares = ((signoa*abs(a))*c)%26
        bres = (ei-(e * ares)%26)%26
        for i in range(len(claves_validas)):
          if claves_validas[i] == abs(ares):
            ares = inversas_validas[i]
            break
        bres = int(bres)
        if ares not in inversas_validas:
          continue
        ei = first_two[x]
        ti = first_two[y]
        first_two = [ei,ti]
        return ares, bres, first_two, dic

def rsadecript(palabralist,p,q,d,fallas):
  n = p*q
  #phi = (p-1)*(q-1)
  for i in range(len(palabralist)):
    palabralist[i] = (palabralist[i]**d)%n
  palabra = deconvert(palabralist)
  return palabra,p,q,d    