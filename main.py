import random as ran
from math import gcd as bltin_gcd


#///////////////////////////////////////////////////////////////
#//////////////////////FUNCIONES GENERALES///////////////////
#////////////////////////////////////////////////////////////////
def rela_primes():
  lista = []
  for i in range(26): 
    if bltin_gcd(26, i) == 1:
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




#///////////////////////////////////////////////////////////////
#//////////////////////METODOS DE CODIFICACION///////////////////
#////////////////////////////////////////////////////////////////

def encode_despla(palabrast):
  palabrals = unify(palabrast)
  
  for count_falla in range(4):
    if count_falla > 2:
      clave = ran.randint(1,26)
      print("Al usar todos los intentos, hemos elegido una clave por usted. La clave sera: {}.".format(clave))
      palabrals = convert(palabrals)
      for i in range(len(palabrals)):
        palabrals[i] = (palabrals[i] + clave)%26
      palabrast = deconvert(palabrals)
      print(palabrast)
      return palabrast
    print("ingrese una clave entre 1 y 26. \n numero de intento: {}, tiene 3 intentos.".format(count_falla+1))
    clave = int(input())
    if 1 <= clave <= 26:
        palabrals = convert(palabrals)
        for i in range(len(palabrals)):
          palabrals[i] = (palabrals[i] + clave)%26
        palabrast = deconvert(palabrals)
        print(palabrast)
        return palabrast
    else:
      print("clave ilegal")




#///////////////////////////////////////////////////////////////
#//////////////////////METODOS DE DECODIFICACION///////////////////
#////////////////////////////////////////////////////////////////
####mbwjebftnvzmjoeb
####xmhupmqegzmoaeufmxuzpm (12)
def decode_despla(string):
  count_fallas = 0
  while count_fallas < 3:
    print("ingrese la clave, esta debe ser un numero entre 1 y 25.\n Tiene 3 intentos, este es el intento numero {}".format(count_fallas+1))
    key = int(input())
    if 1<= key<=26:
      lista = unify(string)
      lista = convert(lista)
      for j in range(len(lista)):
        lista[j] = (lista[j]-key)%26
      string = deconvert(lista)
      print(string)
      return string
    count_fallas = count_fallas + 1
  print("Al usar los 3 intentos, la aproximacion sera por fuerza bruta, las posibilidades son las siguientes:")
  for i in range(25):
    lista = unify(string)
    lista = convert(lista)
    for j in range(len(lista)):
      lista[j] = (lista[j]+1)%26
    string = deconvert(lista)
    print(string)
  return string