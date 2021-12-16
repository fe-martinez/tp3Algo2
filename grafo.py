class Grafo():
    def __init__(self, dirigido=False):
        self.grafo = {}
        self.es_dirigido = dirigido

    def crear_vertice(self, vertice):
        if self.existe(vertice):
            return False
        self.grafo[vertice] = {}

    def crear_arista(self, desde, hasta, peso=1):
        self.grafo[desde][hasta] = peso
        if not self.es_dirigido:
            self.grafo[hasta][desde] = peso

    def borrar_vertice(self, vertice):
        for v in self.grafo:
            if vertice in self.grafo[v].keys():
                del self.grafo[v][vertice]
        del self.grafo[vertice]
    
    def borrar_arista(self, desde, hasta):
        del self.grafo[desde][hasta]
        if not self.es_dirigido:
            del self.grafo[hasta][desde]

    def se_unen(self, desde, hasta):
        return hasta in self.grafo[desde]
    
    def largo(self):
        return len(self.grafo)

    def existe(self, vertice):
        return vertice in self.grafo

    def obtener_vertices(self):
        lista = []
        for v in self.grafo:
            lista.append(v)
        return lista
    
    def adyacentes(self, vertice):
        lista = []
        if vertice in self.grafo:
            for v in self.grafo[vertice]:
                lista.append(v)
            return lista
        else:
            return None
