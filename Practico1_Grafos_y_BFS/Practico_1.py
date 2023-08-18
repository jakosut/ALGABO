
class Grafo:
    def __init__(self, num_vertices):
        self.lista = [] # lista 
        for x in range(num_vertices): # agrego una lista por cada vertice
            self.lista.append([])
    
    def nueva_arista(self, i, j):
        if i < len(self.lista) and j < len(self.lista): # Si la arista que quiero agregar (par de vertices) es menor a la lista no lo hace 
            self.lista[i].append(j)
    
    def nuevo_vertice(self):
        self.lista.append([]) # Nueva lista para el nuevo vertice
    

    def print(self):
        for x in range(len(self.lista)):
            print(x, ">", self.lista[x])
        print("--------------")

# Implementacion
g = Grafo(4)
g.print()
g.nueva_arista(0,3)
g.print()
g.nueva_arista(1,3)
g.nueva_arista(3,2)
g.nueva_arista(2,0)
g.print()
g.nueva_arista(0,1)
g.print()
g.nuevo_vertice()
g.print()
g.nueva_arista(0,4)
g.print()
