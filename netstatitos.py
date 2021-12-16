import sys
from grafo import Grafo
from csv import reader
import recorridos
from collections import deque
from sys import setrecursionlimit
from random import shuffle
sys.setrecursionlimit(20000)

def cargar_grafo():
    archivo = open("wiki-reducido-75000.tsv")
    leer = reader(archivo, delimiter="\t")
    grafo = Grafo(True)

    for linea in leer:
        for item in linea:
            grafo.crear_vertice(item)
        for i in range(0, len(linea)):  # Se agregan las conexiones entre los vertices agregados
            if i != len(linea) - 1:
                grafo.crear_arista(linea[0], linea[i+1])
    archivo.close
    return grafo

def listar_operaciones():
    print("camino")
    print("rango")
    print("diametro")
    print("navegacion")
    print("conectados")
    print("lectura")
    print("comunidad")
    print("clustering")

#Imprime una lista de vertices de manera vertice -> vertice -> ... -> vertice
def imprimir_recorrido(lista):
    resultado = ""
    #Chequear si el item es == al ultimo elemento no sirve, genera conflictos cuando se imprime un ciclo en navegacion
    for index, elem in enumerate(lista):
        if index == len(lista) - 1:
            resultado += elem
        else:
            resultado += elem + " - > "
    print(resultado)

#Busca el camino mas corto entre desde y hasta
def camino(grafo, desde, hasta):
    padres, orden = recorridos.bfs(grafo, desde)
    lista = []
    actual = hasta
    if actual == None:
        print("No existe el recorrido")
        return
    while actual != None:
        lista.insert(0, actual)
        actual = padres[actual]

    imprimir_recorrido(lista)
    print("Costo: ", orden[hasta])

#Devuelve todos los vertices a distancia n del vertice
def rango(grafo, vertice, n):
    orden = recorridos.bfs(grafo, vertice)[1]
    suma = 0
    for v in orden:
        if int(orden[v]) == n:
            suma += 1
    return suma

#Devuelve el camino minimo mas largo en todo el grafo
def diametro(grafo):
    diametro = 0
    vertices = grafo.obtener_vertices()
    punta = None
    padres_parcial = None
    _padres_parcial = None
    for v in vertices:
        parcial = 0
        padres, orden = recorridos.bfs(grafo, v)
        for k in orden:
            if orden[k] > parcial:
                parcial = int(orden[k])
                punta_parcial = k
                padres_parcial = padres
        if parcial > diametro:
            diametro = parcial
            punta = punta_parcial
            _padres_parcial = padres_parcial
    
    camino = []
    while(punta != None):
        camino.insert(0, punta)
        punta = _padres_parcial[punta]

    imprimir_recorrido(camino)
    print("Costo: ", diametro)

#Arma un camino accediendo al primer vertice listado en el diccionario cada vez hasta llegar a n vertices o llegar a un vertice sin adyacentes
def navegacion(grafo, vertice):
    lista = grafo.adyacentes(vertice)
    resultado = []
    resultado.append(vertice)
    conteo = 0
    while len(lista) > 0 and conteo < 20:
        resultado.append(lista[0])
        lista.clear
        lista = grafo.adyacentes(lista[0])
        conteo += 1
    
    imprimir_recorrido(resultado)

#Devuelve el componente fuertemente conexo del vertice
def conectividad(grafo, vertice):
    cfc = recorridos.cfc(grafo, vertice)
    print(len(cfc))
    for v in cfc:
        print(v)

#Arma, si es posible, un orden entre los vertices dados tal que no se visite primero un vertice que tenga una arista de entrada proveniente de un vertice en la lista
def dos_am(grafo, lista):
    aux = Grafo(True)
    for v in lista:
        aux.crear_vertice(v)

    for v in lista:
        for w in grafo.adyacentes(v):
            if aux.existe(w):
                aux.crear_arista(w, v)

    resultado = recorridos.topologico(aux)
    print('%s' % ', '.join(map(str, resultado)))

def max_freq(vertices, labels):
    frecuencia = {}
    for v in vertices:
        if labels[v] not in frecuencia:
            frecuencia[v] = 0
        frecuencia[v] += 1

    max = frecuencia[vertices[0]]
    for i in frecuencia:
        if frecuencia[i] > max:
            max = frecuencia[i]

    return max

def label_propagation(grafo, vertice):
    label = {}
    for i,v in enumerate(grafo.obtener_vertices()):
        label[v] = i

    adyacentes = recorridos.aristas_entrada(grafo)

    label_anterior = label.copy()
    vertices = grafo.obtener_vertices()
    shuffle(vertices)
    for i in range(0, 50):
        for v in vertices:
            if len(adyacentes[v]) == 0:
                continue
            label[v] = max_freq(adyacentes[v], label_anterior)

        shuffle(vertices)
        label_anterior = label.copy()

    resultado = []
    comunidad = label[vertice]
    for v in grafo.obtener_vertices():
        if label[v] == comunidad:
            resultado.append(v)

    print('%s' % ', '.join(map(str, resultado)))

def clustering(grafo, vertice):
    adyacentes = grafo.adyacentes(vertice)
    suma = 0

    for v in adyacentes:
        for w in grafo.adyacentes(v):
            if w in adyacentes:
                suma += 1

    divisor = len(adyacentes) * (len(adyacentes) - 1)
    if divisor == 0:
        print("0.000")
        return

    print("%1.3f" % (suma/divisor))

def main():
    grafo = cargar_grafo()
    linea = input()
    comandos = linea.split(" ",1)

    while(comandos[0] != "salir"):
        if comandos[0] == "listar_operaciones":
            listar_operaciones()
        elif comandos[0] == "camino":
            valores = comandos[1].split(",")
            camino(grafo, valores[0], valores[1])
        elif comandos[0] == "rango":
            valores = comandos[1].split(",")
            print(rango(grafo, valores[0], int(valores[1])))
        elif comandos[0] == "diametro":
            diametro(grafo)
        elif comandos[0] == "navegacion":
            valores = comandos[1].split(",")
            navegacion(grafo, valores[0])
        elif comandos[0] == "conectados":
            valores = comandos[1].split(",")
            conectividad(grafo, valores[0])
        elif comandos[0] == "lectura":
            valores = comandos[1].split(",")
            dos_am(grafo, valores)
        elif comandos[0] == "comunidad":
            valores = comandos[1].split(",")
            label_propagation(grafo, valores[0])
        elif comandos[0] == "clustering":
            valores = comandos[1].split(",")
            clustering(grafo, valores[0])
        else: print("operacion no permitida")
        linea = input()
        comandos = linea.split(" ",1)

if __name__ == "__main__":
    main()