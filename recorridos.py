from grafo import Grafo
from collections import deque

def bfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    q = deque()
    q.append(origen)
    while q:
        v = q.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                q.append(w)
    return padres, orden

def _dfs(grafo, v, visitados, padres, orden):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            visitados.add(w)
            padres[w] = v
            orden[w] = orden[v] + 1
            _dfs(grafo, w, visitados, padres, orden)

#Desde un vertice en particular
def dfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    _dfs(grafo, origen, visitados, padres, orden)
    return padres, orden

#Recorre todo el grafo desde un vertice aleatorio
def dfs_completo(grafo):
    visitados = set()
    padres = {}
    orden = {}
    for v in grafo:
        if v not in visitados:
            visitados.add(v)
            padres[v] = None
            orden[v] = 0
            _dfs(grafo, v, visitados, padres, orden)

def cfc(grafo, v):
    visitados = set()
    apilados = set() # para mantener el orden computacional
    todas_cfc = []
    orden = {}
    mb = {}
    pila = deque()
    orden_contador = 0
    componentes_fuertemente_conexas(grafo, v, visitados, apilados, todas_cfc, orden, mb, pila, orden_contador)
    for listas in todas_cfc:
        if v in listas:
            return listas

def componentes_fuertemente_conexas(grafo, v, visitados, apilados, todas_cfc, orden, mb, pila, orden_contador):
    visitados.add(v)
    orden[v] = orden_contador
    mb[v] = orden[v]
    orden_contador += 1
    pila.appendleft(v)
    apilados.add(v)
  
    for w in grafo.adyacentes(v):
        if w not in visitados:
            componentes_fuertemente_conexas(grafo, w, visitados, apilados, todas_cfc, orden, mb, pila, orden_contador)

        if w in apilados:
            mb[v] = min(mb[v], mb[w])
    
  
    if orden[v] == mb[v] and len(pila) > 0:
        nueva_cfc = []
        while True:
            w = pila.popleft()
            apilados.remove(w)
            nueva_cfc.append(w)
            if w == v:
                break
        todas_cfc.append(nueva_cfc)

def grados_entrada(grafo):
    g_ent = {}
    for v in grafo.obtener_vertices():
        g_ent[v] = 0
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            g_ent[w] += 1
    return g_ent

def topologico(grafo):
    g_ent = grados_entrada(grafo)
    q = deque()
    for v in grafo.obtener_vertices():
        if g_ent[v] == 0:
            q.append(v)
    resultado = []
    while q:
        v = q.popleft()
        resultado.append(v)
        for w in grafo.adyacentes(v):
            g_ent[w] -= 1
            if g_ent[w] == 0:
                q.append(w)

    if len(resultado) != grafo.largo():
        ("No hay recorrido posible")
        return
        
    return resultado

def aristas_entrada(grafo):
    entrada = {}
    for v in grafo.obtener_vertices():
        entrada[v] = []
    
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            entrada[w].append(v)

    return entrada

# def obtener_ciclo_dfs(grafo, origen):
#     visitados = {}
#     padre = {}
#     ciclos = []
#     for v in grafo:
#         if v not in visitados:
#             ciclo = dfs_ciclo(grafo, v, visitados, padre)
#             if ciclo is not None:
#                 ciclos.append(ciclo)
#     return ciclos

# def dfs_ciclo(grafo, v, visitados, padre):
#     visitados[v] = True
#     for w in grafo.adyacentes(v):
#         if w in visitados:
#             if w != padre[v]:
#                 return reconstruir_ciclo(padre, w, v)
#         else:
#             padre[w] = v
#             ciclo = dfs_ciclo(grafo, w, visitados, padre)
#             if ciclo is not None:
#                 return ciclo
#     return None

# def reconstruir_ciclo(padre, inicio, fin):
#   v = fin
#   camino = []
#   while v != inicio:
#     camino.append(v)
#     v = padre[v]
#   camino.append(inicio)
#   return camino.invertir()

# def es_bipartito(grafo):
#     color = {}
#     ROJO = 1
#     NEGRO = 2
#     for v in grafo.obtener_vertices():
#         color[v] = None
#     nodo = grafo.vertice_aleatorio()
#     color[nodo] = ROJO
#     q = deque()
#     q.append(nodo)
#     while q:
#         v = q.popleft()
#         for w in grafo.adyacentes(v):
#             if(color[v] == color[w]):
#                 return False
#             elif (color[w] == None):
#                 if color[v] == ROJO:
#                     color[w] = NEGRO
#                 else:
#                     color[w] = ROJO
#                 q.append(w)
#     return True

# def grados_entrada(grafo):
#     grados = {}
#     for v in grafo.obtener_vertices():
#         grados[v] = 0
#     for v in grafo.obtener_vertices():
#         for w in grafo.adyacentes(v):
#             grados[w] += 1
#     return grados

# def obtener_orden(grafo):
#     gr_entrada = grados_entrada(grafo)
#     q = deque()
#     for v in grafo.obtener_vertices():
#         if gr_entrada[v] == 0:
#             q.append(v)
#     orden = []
#     while q:
#         v = q.popleft()
#         orden.append(v)
#         for w in grafo.adyacentes(v):
#             gr_entrada[w] -= 1
#             if gr_entrada[w] == 0:
#                 q.append(w)
#     return orden

# def es_compatible(grafo, resultado, v_actual):
#     for v in grafo.adyacentes(v_actual):
#         if v in resultado:
#             return False
#     return True

# def _no_adyacentes(grafo, n, v_actual, vertices, resultado):
#     if(v(v_actual) == len(vertices)):
#         return False
#     if len(resultado) == n:
#         return es_compatible()
    
#     if not es_compatible():
#         return False

#     resultado.add(vertices[v_actual])
#     if _no_adyacentes(grafo, n, v_actual + 1, vertices, resultado):
#         return True
#     resultado.remove(vertices[v_actual])
#     return _no_adyacentes(grafo, n, v_actual + 1, vertices, resultado)

# def no_adyacentes(grafo, n):
#     vertices = {}
#     resultado = set()
#     for v in grafo.obtener_vertices():
#         vertices[v] = v
#     return _no_adyacentes(grafo, n, 0, vertices, resultado)