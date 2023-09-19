
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

def BFS(H, inicio):
        n = len(H.lista) #Numero de vertices 
        T = Grafo(n)
        visitados = [False] * n # Armo una lista con los vertices que ya fueron visitados, los marco con true cuando estan visitados
        cola = [inicio] #Arranco la cola con el vertice de inicio
        visitados[inicio] = True #Marco el vertice de inicio como visitado

        while len(cola) != 0: #Mientras no este vacia..
            vertice = cola.pop(0) # Sacar el próximo vértice de la cola
            
            for vecino in H.lista[vertice]: # Para cada vecino del vértice
                if not visitados[vecino]:
                    visitados[vecino] = True # Si el vecino no ha sido visitado, lo marcamos y lo añadimos a la cola
                    cola.append(vecino) # Ponemos una arista entre el vértice y su vecino en el árbol BFS
                    T.nueva_arista(vertice, vecino)
        return T

# # Implementacion
# g = Grafo(4)
# g.print()
# g.nueva_arista(0,3)
# g.print()
# g.nueva_arista(1,3)
# g.nueva_arista(3,2)
# g.nueva_arista(2,0)
# g.print()
# g.nueva_arista(0,1)
# g.print()
# g.nuevo_vertice()
# g.print()
# g.nueva_arista(0,4)
# g.print()



#--------

# # Crear un grafo
# H = Grafo(5)
# H.nueva_arista(0, 1)
# H.nueva_arista(0, 2)
# H.nueva_arista(1, 3)
# H.nueva_arista(2, 4)
# H.print()

# # Crear el árbol BFS a partir del vértice 0
# T = BFS(H, 0)
# T.print()


# Crear mapeo de etiquetas a índices numéricos
etiquetas_a_indices = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11}

# Crear grafo con 12 vértices (desde A hasta L)
G = Grafo(12)

# Lista de aristas a agregar
aristas = [('A','B'), ('B','A'), ('A','L'), ('L','A'), ('A','E'), ('E','A'), ('B','C'), ('C','B'), ('C','F'), 
           ('F','C'), ('C','E'), ('E','C'), ('B','D'), ('D','B'), ('D','G'), ('G','D'), ('L','H'), ('H','L'), 
           ('H','G'), ('G','H'), ('L','K'), ('K','L'), ('K','I'), ('I','K'), ('K','J'), ('J','K')]

# Agregar aristas al grafo
for u, v in aristas:
    G.nueva_arista(etiquetas_a_indices[u], etiquetas_a_indices[v])

# Mostrar grafo
G.print()


# Crear el árbol BFS a partir del vértice 0
T = BFS(G, etiquetas_a_indices['D'])
T.print()