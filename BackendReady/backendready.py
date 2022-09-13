import random as ran
from math import gcd as bltin_gcd
import re




#///////////////////////////////////////////////////////////////
#//////////////////////FUNCIONES GENERALES///////////////////
#////////////////////////////////////////////////////////////////


def rela_primes():
  """
  Generates a list of relative primes with 26
  """
  lista = []
  for i in range(26): 
    if bltin_gcd(26, i) == 1:
      lista.append(i)
  return lista 



def inver_primes():
  """
  Generates a list with the inverses of the relative primes with 26
  """
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
  """
  Converts all to lower, eliminates characters that arent aphabetical
  eliminates the spaces between words and creates a list where each element
  is one of the symbols left 
  """
  palabralist = []
  palabra = palabra.replace(" ", "")
  palabra = palabra.lower()
  regex = re.compile('[^a-z]')
  palabra = regex.sub('', palabra)
  print(palabra)
  for i in range(len(palabra)):
    palabralist.append(palabra[i])
  return palabralist
  
def convert (list):
  """
  Converst a list of characters into a list of numbers
  corresponding to it's position on the alphabet
  """
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
  """
  Converts a list of numbers to a list of characters corresponding
  to it's position on the alphabet
  """
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  string = ""
  for i in range(len(list)):
    list[i] = lista[int(list[i])]
    string = string + list[i]
  return string



#///////////////////////////////////////////////////////////////
#//////////////////////METODOS DE CODIFICACION///////////////////
#////////////////////////////////////////////////////////////////

####LIMPIO
def encode_despla(palabrast,key,count_falla):
  """
This codification method receives a message, and a key
From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
The key is required to be between 1 and 25.
If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
Understanding a<->0, b<->1, ..., z<->25 the codification method transforms each letter to its corresponding numerical value.
The codification method adds the key value to each number and transforms the result back to an alphabetical value.
Then returns the message encrypted
  """
  palabrals = unify(palabrast)
  if count_falla > 2:
    key = ran.randint(1,26)
    palabrals = convert(palabrals)
    for i in range(len(palabrals)):
      palabrals[i] = (palabrals[i] + key)%26
    palabrast = deconvert(palabrals)
    print(palabrast)
    return palabrast, key
  if 1 <= key <= 26:
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
  """
This codification method receives a message, and a key
From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
The key is required to be in the list of relative prime numbers with 26.
If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
Understanding a<->0, b<->1, ..., z<->25 the codification method transforms each letter to its corresponding numerical value.
The codification method adds the key value to each number and transforms the result back to an alphabetical value.
Then returns the message encrypted
  """

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

###### LIMPIO
def encode_sust(palabrast,key,count_falla):
  """
This codification method receives a message, and a key
From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
The key is a list of letters that, in order, replace one of the characters in the message. non alphabet characters and duplicates are not allowed
If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
The codification method substitutes each letter by its replacement as stated in the key.
Then returns the message encrypted
  """

  dic = {'a':"", 'b':"", 'c':"", 'd':"", 'e':"", 'f':"", 'g':"", 'h':"", 'i':"", 'j':"", 'k':"", 'l':"",'m':"", 'n':"", 'o':"", 'p':"", 'q':"", 'r':"", 's':"", 't':"", 'u':"", 'v':"", 'w':"", 'x':"", 'y':"", 'z':""}
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  palabrals = unify(palabrast)
  count = 0
  if count_falla > 2:
    listaran = lista[:]
    ran.shuffle(listaran)
    for item in listaran:
      if item not in dic.values():
        dic[lista[count]] = item
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
  """
This codification method receives a message, and a key
From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
The key is composed by a and b, for a it needs to be in the list of relative primes of 26 and b requires it to be between 1 and 25.
If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
Understanding a<->0, b<->1, ..., z<->25 the codification method transforms each letter to its corresponding numerical value.
The codification method multiplies a and ads b to each number and transforms the result back to an alphabetical value.
Then returns the message encrypted
  """

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
    if 1 <= b <= 25:
      palabrals = convert(palabrals)
      for i in range(len(palabrals)):
        palabrals[i] = (((palabrals[i] * a)%26)+b)%26
      palabrast = deconvert(palabrals)
      return palabrast, a, b
    else:
      return -1, -1
  else:
    return -1,-1



####LIMPIO
def encode_permu(string, tama, key, count_falla):
  """
This codification method receives a message, and a key
From the message we remove all non alphabetical characters, remove spaces, and lower all characters that remain.
The key is composed by a and b, a needs to bea positive number lower than the length of the processed text, b requires to be between 1 and a.
If the user fails 3 times providing a valid key, the program chooses randomly a valid key and encrypts the message using it.
The codification method takes chunks of size a and moves each letter b spaces to the right, if the letter is in the last position of the chunk, it goes back to the first.
Then returns the message encrypted
  """

  palabrals = unify(string)
  while True:
    if 1 <= tama <=len(palabrals):
      break
    return -1, -1
  while True:
    if 1<= key < tama:
      break
    return -1, -1
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

#///////////////////////////////////////////////////////////////
#//////////////////////METODOS DE DECODIFICACION///////////////////
#////////////////////////////////////////////////////////////////
#### LIMPIO
####mbwjebftnvzmjoeb
####xmhupmqegzmoaeufmxuzpm (12)
def decode_despla(string, key, count_fallas):
  if 1<= key<=26:
    lista = unify(string)
    lista = convert(lista)
    for j in range(len(lista)):
      lista[j] = (lista[j]-key)%26
    string = deconvert(lista)
    print(string)
    return string
  for i in range(25):
    lista = unify(string)
    lista = convert(lista)
    for j in range(len(lista)):
      lista[j] = (lista[j]+1)%26
    string = deconvert(lista)
  return string



##### LIMPIO
#lavidaesmuylinda
#sqbasqmnalmsnajaralfajafasnwfkjbaf (11) 
######### existe algo raro con el 11, arreglar
##qeaxgoxabaxxagngojgsgnoahg (21)
def decode_mult(string, key, count_fallas):
  inver_validas = inver_primes()
  keys = rela_primes()
  if key in keys:
    lista = unify(string)
    lista = convert(lista)
    for i in range(len(keys)):
      if keys[i] == key:
        key = inver_validas[i]
    for j in range(len(lista)):  
      lista[j] = int((lista[j]*key)%26)
    string = deconvert(lista)
    return string
  for i in inver_validas:
    lista = unify(string)
    lista = convert(lista)
    for j in range(len(lista)):
      lista[j] = int((lista[j]*i)%26)
    res = deconvert(lista)
  return res

#LIMPIO
def decode_sust(palabrast,key,count_falla):
  dic = {'a':"", 'b':"", 'c':"", 'd':"", 'e':"", 'f':"", 'g':"", 'h':"", 'i':"", 'j':"", 'k':"", 'l':"",'m':"", 'n':"", 'o':"", 'p':"", 'q':"", 'r':"", 's':"", 't':"", 'u':"", 'v':"", 'w':"", 'x':"", 'y':"", 'z':""}
  lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  palabrals = unify(palabrast)
  count = 0
  if count_falla > 2:
    listaran = lista[:]
    ran.shuffle(listaran)
    for item in listaran:
      if item not in dic.values():
        dic[lista[count]] = item
  for item in key:
    if item not in lista:
      return -1
    else:
      if item not in dic.values():
        dic[lista[count]] = item
        count = count + 1
      else:
        return -1  
  string = ""
  for i in range(len(palabrals)):
    palabrals[i] = dic[palabrals[i]]
    string = string + palabrals[i]
  return string
  
  
## la vida es hermosa
##tulypuwqrwjaoqu (7,20)
##xuvijuogdobcmgu (5,20)
def decode_afin(string):
  alf = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  lista = unify(string)
  claves_validas = rela_primes()
  inversas_validas = inver_primes()
  print("tiene usted la clave? (Y/n)")
  res = input()
  if res == "Y":
    flag = True
    while flag == True:
      print("ingrese 'a': ")
      a = int(input())
      for i in range(len(claves_validas)):
        if claves_validas[i] == a:
          ai = inversas_validas[i]
      print("ingrese 'b': ")
      b = int(input())
      if a in claves_validas:
        if 1 <= b <= 25:
          palabrals = convert(lista)
          for i in range(len(palabrals)):
            palabrals[i] = (((palabrals[i] - b)%26)*ai)%26
          palabrast = deconvert(palabrals)
          print(palabrast)
          return palabrast
        else:
          print("ingrese nuevamente la clave")
      else:
        print("ingrese nuevamente la clave")
    
  else:
    dic={}
    for item in lista:
      if item not in dic.keys():
        dic[item] = 1
      else:
        dic[item] = dic[item]+1
    dic = dict(sorted(dic.items(), key=lambda item: item[1], reverse = True))
    print("Se ha realizado el siguiente conteo, basado en esto, como desea mapear?")
    print(dic)
    flag = True
    while flag == True:
      print("Como primera letra, cual letra desea mapear. (sugerimos las letras con mayor frecuencias en el alfabeto ingles 'e','t','a','o','n')")
      e = input()
      print("Cual letra cree que mapea a '{}'?".format(e))
      ei = input()
      print("Como segunda letra, cual letra desea mapear. (sugerimos las letras con mayor frecuencias en el alfabeto ingles 'e','t','a','o','n')")
      t = input()
      print("Cual letra cree que mapea a '{}'?".format(t))
      ti = input()
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
      print(e,ei,t,ti,a,c,signoa,signoc)
      if abs(a) not in claves_validas:
        print("intentelo nuevamente")
      else:
        for i in range(len(claves_validas)):
          if claves_validas[i] == abs(a):
            a = inversas_validas[i]
        lista = unify(string)
        ares = ((signoa*abs(a))*c)%26
        bres = (ei-(e * ares)%26)%26
        print("estos son a = {} y b = {}".format(ares,bres))
        palabrals = convert(lista)
        for i in range(len(claves_validas)):
          if claves_validas[i] == abs(ares):
            ares = inversas_validas[i]
            break
        for i in range(len(palabrals)):
          palabrals[i] = ((palabrals[i] - bres)*ares)%26
        palabrast = deconvert(palabrals)
        print(palabrast)
        return palabrast


#### LIMPIO
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
  return final

#### LIMPIO
def decode_permu(string, tama, key, count_falla):
  palabra = unify(string)
  if count_falla > 2:
    final = []
    for i in range(1,len(palabra)+1):
      final.append(permufiesta(palabra,i))
    return final
  if 1 <= tama <= len(palabra):
    if 1 <= key < tama:
      return permufiesta(palabra,tama,key)
    else:
      return -1
  else:
    return -1