from itertools import permutations
from BackendReady.backendready import *
import matplotlib.pyplot as plt
import numpy as np
import random

#Genera una permutación de 10 números aleatoria 
def generarPermutacion():
    permutacion=[]
    for i in range(10):
        permutacion.append(random.randint(0, 25))
    return(permutacion)

#Genera un punto inicial x, y
def generarPunto():
    x = random.randint(-10, 3)
    y = random.randint(-10, 3)
    return x, y
    
#Dibuja la permutación 
def dibujarPermutacion(permutacion, x, y):
    
    plt.figure(figsize=(10,6))
    plt.style.use('ggplot')
    # plt.plot([0, 0], [y-1, 26], color="yellow")
    # plt.plot([x-1, 10], [0, 0], color="yellow")
    columna=0
    for num in permutacion:
        num = int(num)
        for i in range(0, 26):
            letra = deconvert([(num+i)%26])
            plt.text(columna, i, letra,
                fontsize=10,
                color="black",
                verticalalignment ='bottom', 
                horizontalalignment ='center',
                ) 
        columna+=1           
            
    plt.xlabel("Permutación: "+str(permutacion))
    plt.xlim(-0.2, 9.2)
    plt.ylim(0, 26)
    plt.savefig("static/images/GMpermutacion.png")


#Crea el grafo según el punto inicial y lo guarda en un diccionario
def generarGrafo(x_inicial, y_inicial):
    vectores={}
    #cada punto va a ser un elemento del diccionario de la forma
    # (x, y): [lista de pendientes  que llegan a este punto]
        
    #PRIMERA GENERACIÓN
    pendiente = 0
    x=int(x_inicial)
    y=int(y_inicial)
    while y < 26 and x < 26:
        if (x+1, y+pendiente) in vectores.keys():
            vectores[(x+1, y+pendiente)].append(pendiente)
        else:
            vectores[(x+1, y+pendiente)]=[pendiente]
        x+=1
        y+=pendiente
        pendiente+=1
    primera_gen = list(vectores.keys())
    
    
    #SEGUNDA GENERACIÓN: Recorro todos los puntos visitados y creo una nueva linea apartir de cada uno 
    queue=[]
    for key in primera_gen:
        pendiente = 0
        x=key[0]
        y=key[1]
        if x<26 and y<26:
            while y < 26 and x < 26:
                if (x+1, y+pendiente) in vectores.keys():
                    vectores[(x+1, y+pendiente)].append(pendiente)
                else:
                    vectores[(x+1, y+pendiente)]=[pendiente]
                queue.append((x+1, y+pendiente))
                x+=1
                y+=pendiente
                pendiente+=1
        #el stack queda con todos los puntos recorridos en 2da gen
    
    
    #TERCERA GENERACIÓN: ahora recorro esos desde 0 y solo dibujo hasta el máximo vector que llega AL PUNTO
    while len(queue)!= 0:
        (x, y)=queue[0]
        pendientes_punto = vectores[(x, y)]
        mayor_pend=max(pendientes_punto)
        if x<26 and y<26:
            for pendiente in range(0, mayor_pend+1):
                if (x+1, y+pendiente) in vectores.keys():
                    vectores[(x+1, y+pendiente)].append(pendiente)
                else:
                    vectores[(x+1, y+pendiente)]=[pendiente]
                x+=1
                y+=pendiente
                if x>=26 or y>=26:
                    break
        queue.pop(0)
        
    #Guardo el grafo como imagen en static/images/GMgrafo.png
    dibujarGrafo(vectores, x_inicial, y_inicial)
    return vectores


#dibuja el grafo en (x, y)
def dibujarGrafo(vectores, x, y):
    plt.style.use('ggplot')
    
    plt.figure(figsize=(10,6))
    plt.xlabel("Grafo con punto inicial: "+str(x)+", "+str(y))
    if x <=0:
        plt.xlim(x-0.2, 10)
        plt.plot([x-1, 10], [0, 0], color="yellow")
    else:
        plt.xlim(-0.2, 10)
        plt.plot([-1, 10], [0, 0], color="yellow")
    if y <=0:
        plt.ylim(y-0.2, 26)
        plt.plot([0, 0], [y-1, 26], color="yellow")
    else:
        plt.ylim(-0.2, 26)
        plt.plot([0, 0], [-1, 26], color="yellow")
        
    
    for a in range(x-1, 11):
        for b in range(y-1, 27):
            plt.plot(a, b, marker="o", markersize = 1, color="#BABABA")
            
    puntos = list(vectores.keys())
    for i in puntos:
        x_f=i[0]
        y_f=i[1]
        for pend in vectores[i]:
            plt.plot([x_f-1, x_f], [y_f-pend, y_f],  marker = 'o', markersize = 4)
            
    plt.savefig("static/images/GMgrafo.png")


#Encriptación 
def gammaencript(palabra,permu,vectores):
    alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    palabralist = unify(palabra)
    vectorconvert = []
    for i in range(0,len(palabralist)):
        for j in range (0,26):
            if palabralist[i] == alfabeto[(j+permu[i%10])%26]: 
                if (i%10,j) not in list(vectores.keys()):
                    vectores[(i%10,j)] = []
                vectorconvert.append(((i%10)+len(vectores[(i%10,j)]),j))
    vectorconvert_str = ""
    for i in vectorconvert:
        vectorconvert_str+= str(i)+" "

    return vectorconvert_str


#Decriptación
def gammadecript(vectorconvert,permu,vectores):
    try:
        vectorconvert =vectorconvert.replace(" ", '')
        vectorconvert = vectorconvert.replace(")", '')
        vectorconvert = vectorconvert.split("(")
        for i in range(0, len(vectorconvert)):
            vectorconvert[i]=vectorconvert[i].split(",")
        vectorconvert.pop(0)
        if vectorconvert==[]:
            return -1
        alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        palabra = []
        for i in range(0,len(vectorconvert)):
            palabra.append(alfabeto[(permu[i%10]+ int(vectorconvert[i][1]))%26])
            
        palabra_str = ""
        for i in palabra:
            palabra_str = palabra_str + i
            
        return palabra_str
    except:
        return -1

def convertirPermutacion(permutacion):
    try:
        permutacion = permutacion.split()
        if len(permutacion)!=10:
            return -1
        for i in range(10):
            permutacion[i]=int(permutacion[i])
        return permutacion
    except:
        return -1


def nuevoGrafo(x, y, permutacion):
    try:
        x=int(x)
        y=int(y)
        vectores = generarGrafo(x, y)
        dibujarPermutacion(permutacion, x, y)
        return vectores
    except:
        return -1
    
    
def nuevoGrafoAlt(x, y):
    try:
        x=int(x)
        y=int(y)
        vectores = generarGrafo(x, y)
        permutacion = generarPermutacion()
        dibujarPermutacion(permutacion, x, y)
        return vectores, permutacion
    except:
        return -1, -1
    