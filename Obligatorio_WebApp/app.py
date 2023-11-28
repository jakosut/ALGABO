from flask import Flask, render_template, jsonify, request
import requests
import folium
from flask import send_from_directory
import itertools
import math
import random


app = Flask(__name__)

ciudadesAUtilizar = []
matrizDistanciasGlobal = []

matrizDistanciasCompleta = [
    [0, 550.0507, 385.6796, 658.8347, 412.2516, 452.2856, 500.6593, 616.5653, 695.2045, 599.0939, 324.8104, 482.7064, 111.0888, 668.2785, 209.4704, 549.119, 503.2997, 206.1982, 500.1558],
    [550.0507, 0, 406.7649, 161.9008, 139.1859, 145.9112, 51.0574, 127.8208, 146.461, 49.2188, 329.5127, 272.5451, 456.9595, 217.0472, 443.732, 49.7464, 240.7669, 346.3963, 294.7331],
    [385.6796, 406.7649, 0, 568.0044, 291.9852, 332.0192, 321.4715, 278.7872, 323.962, 396.5407, 439.8297, 558.025, 283.0195, 280.9431, 422.558, 455.8499, 552.8474, 201.3802, 112.8205],
    [658.8347, 161.9008, 568.0044, 0, 246.9863, 207.366, 197.77, 289.4664, 308.1066, 179.9495, 319.5312, 232.944, 567.1272, 378.6928, 433.7505, 112.2872, 201.1659, 456.5641, 456.3787],
    [412.2516, 139.1859, 291.9852, 246.9863, 0, 40.4425, 89.6929, 205.5989, 284.2381, 188.1275, 223.6572, 226.3038, 318.5284, 354.8242, 337.8765, 137.2758, 200.8716, 207.9653, 251.9794],
    [452.2856, 145.9112, 332.0192, 207.366, 40.4425, 0, 128.3647, 273.5497, 292.1899, 192.1741, 183.6013, 186.2479, 360.8057, 362.7761, 297.8206, 97.6352, 160.4404, 250.2426, 440.462],
    [500.6593, 51.0574, 321.4715, 197.77, 89.6929, 128.3647, 0, 116.8747, 195.5138, 99.4033, 311.7969, 307.843, 407.5676, 266.1, 426.0162, 85.0443, 276.0648, 297.0045, 283.787],
    [616.5653, 127.8208, 278.7872, 289.4664, 205.5989, 273.5497, 116.8747, 0, 79.714, 118.0836, 457.1592, 400.1916, 523.2237, 133.0312, 571.3785, 177.3929, 368.4134, 412.6606, 167.0708],
    [695.2045, 146.461, 323.962, 308.1066, 284.2381, 292.1899, 195.5138, 79.714, 0, 127.9747, 476.5861, 419.6185, 602.5552, 84.7992, 590.8054, 196.8198, 387.8403, 491.992, 212.5735],
    [599.0939, 49.2188, 396.5407, 179.9495, 188.1275, 192.1741, 99.4033, 118.0836, 127.9747, 0, 375.2205, 314.4663, 505.5459, 197.7935, 489.4398, 94.4708, 282.6882, 394.9828, 284.5693],
    [324.8104, 329.5127, 439.8297, 319.5312, 223.6572, 183.6013, 311.7969, 457.1592, 476.5861, 375.2205, 0, 126.1521, 350.4724, 545.733, 121.9773, 280.5921, 120.9745, 236.7082, 623.419],
    [482.7064, 272.5451, 558.025, 232.944, 226.3038, 186.2479, 307.843, 400.1916, 419.6185, 314.4663, 126.1521, 0, 469.341, 489.065, 240.8459, 222.6593, 34.7874, 355.5767, 566.7509],
    [111.0888, 456.9595, 283.0195, 567.1272, 318.5284, 360.8057, 407.5676, 523.2237, 602.5552, 505.5459, 350.4724, 469.341, 0, 565.4332, 333.5391, 455.2669, 463.8132, 112.3461, 397.3105],
    [668.2785, 217.0472, 280.9431, 378.6928, 354.8242, 362.7761, 266.1, 133.0312, 84.7992, 197.7935, 545.733, 489.065, 565.4332, 0, 660.4654, 266.4797, 457.5003, 561.652, 169.1621],
    [209.4704, 443.732, 422.558, 433.7505, 337.8765, 297.8206, 426.0162, 571.3785, 590.8054, 489.4398, 121.9773, 240.8459, 333.5391, 660.4654, 0, 395.7928, 236.1752, 219.6403, 532.7348],
    [549.119, 49.7464, 455.8499, 112.2872, 137.2758, 97.6352, 85.0443, 177.3929, 196.8198, 94.4708, 280.5921, 222.6593, 455.2669, 266.4797, 395.7928, 0, 191.2433, 346.6457, 344.2862],
    [503.2997, 240.7669, 552.8474, 201.1659, 200.8716, 160.4404, 276.0648, 368.4134, 387.8403, 282.6882, 120.9745, 34.7874, 463.8132, 457.5003, 236.1752, 191.2433, 0, 350.5943, 534.9636],
    [206.1982, 346.3963, 201.3802, 456.5641, 207.9653, 250.2426, 297.0045, 412.6606, 491.992, 394.9828, 236.7082, 355.5767, 112.3461, 561.652, 219.6403, 346.6457, 350.5943, 0, 314.2716],
    [500.1558, 294.7331, 112.8205, 456.3787, 251.9794, 440.462, 283.787, 167.0708, 212.5735, 284.5693, 623.419, 566.7509, 397.3105, 169.1621, 532.7348, 344.2862, 534.9636, 314.2716, 0]
]

indiceCiudades = {
    "Artigas": 0,
    "Canelones": 1,
    "Melo": 2,
    "Colonia": 3,
    "Durazno": 4,
    "Trinidad": 5,
    "Florida": 6,
    "Lavalleja": 7,
    "Maldonado": 8,
    "Montevideo": 9,
    "Paysandú": 10,
    "Fray Bentos": 11,
    "Rivera": 12,
    "Rocha": 13,
    "Salto": 14,
    "San José": 15,
    "Mercedes": 16,
    "Tacuarembó": 17,
    "Treinta y Tres": 18
}

coordenadasCiudades = {
    "Artigas": {"latitud": -30.4000, "longitud": -56.4667},
    "Canelones": {"latitud": -34.5228, "longitud": -56.2778},
    "Melo": {"latitud": -32.3667, "longitud": -54.1833},
    "Colonia": {"latitud": -34.4607, "longitud": -57.8400},
    "Durazno": {"latitud": -33.4131, "longitud": -56.5006},
    "Trinidad": {"latitud": -33.5389, "longitud": -56.8886},
    "Florida": {"latitud": -34.0956, "longitud": -56.2142},
    "Lavalleja": {"latitud": -34.3700, "longitud": -55.2300},
    "Maldonado": {"latitud": -34.9000, "longitud": -54.9500},
    "Montevideo": {"latitud": -34.8335, "longitud": -56.1674},
    "Paysandú": {"latitud": -32.3214, "longitud": -58.0756},
    "Fray Bentos": {"latitud": -33.1325, "longitud": -58.2956},
    "Rivera": {"latitud": -30.9053, "longitud": -55.5508},
    "Rocha": {"latitud": -34.4839, "longitud": -54.3336},
    "Salto": {"latitud": -31.3833, "longitud": -57.9667},
    "San José": {"latitud": -34.3378, "longitud": -56.7139},
    "Mercedes": {"latitud": -33.2558, "longitud": -58.0192},
    "Tacuarembó": {"latitud": -31.7333, "longitud": -55.9833},
    "Treinta y Tres": {"latitud": -33.2333, "longitud": -54.3833}
}

# --------------------- FUNCIONES DE COORDENADAS Y DISTANCIAS ---------------------

def obtener_coordenadas(ciudad):
    return coordenadasCiudades.get(ciudad, {"nombre": ciudad, "latitud": None, "longitud": None})

def calcular_distancia(ciudad1, ciudad2, matriz_distancias):
    return matriz_distancias[ciudad1][ciudad2]

# --------------------- ALGORITMO DEL VIAJERO ---------------------

def calcular_longitud_ruta(ruta, matriz_distancias):
    longitud = 0
    for i in range(len(ruta) - 1):
        longitud += calcular_distancia(ruta[i], ruta[i + 1], matriz_distancias)
    longitud += calcular_distancia(ruta[-1], ruta[0], matriz_distancias)  # Volver al punto de inicio
    return longitud

def algoritmo_del_viajero(matriz_distancias):
    num_ciudades = len(matriz_distancias)
    mejor_ruta = None
    mejor_longitud = float('inf')
    todas_rutas = list(itertools.permutations(range(num_ciudades)))

    for ruta in todas_rutas:
        longitud = calcular_longitud_ruta(ruta, matriz_distancias)
        if longitud < mejor_longitud:
            mejor_longitud = longitud
            mejor_ruta = ruta

    return mejor_ruta, mejor_longitud

# --------------------- ALGORITMO Aleatorio ---------------------

def tsp_aleatorio(distancias):
    num_ciudades = len(distancias)
    ciudades = list(range(num_ciudades))
    random.shuffle(ciudades)
    costo_total = 0
    camino = []

    for i in range(num_ciudades - 1):
        ciudad_actual = ciudades[i]
        siguiente_ciudad = ciudades[i + 1]
        costo_actual = distancias[ciudad_actual][siguiente_ciudad]
        costo_total += costo_actual
        camino.append(ciudad_actual)

    # Agregar la última ciudad al camino
    ultima_ciudad = ciudades[-1]
    camino.append(ultima_ciudad)

    # Volver a la ciudad inicial
    ciudad_final = ciudades[0]
    costo_final = distancias[ultima_ciudad][ciudad_final]
    costo_total += costo_final

    return camino, costo_total
#  Este algoritmo simplemente permuta aleatoriamente las ciudades y calcula el costo total del recorrido. 
# Debido a su enfoque aleatorio, no garantiza una solución óptima en absoluto y 
# generalmente producirá soluciones muy subóptimas para instancias más grandes del problema del TSP. 
# Es importante destacar que este algoritmo no es una solución viable para resolver el TSP en la práctica, pero puede servir como un ejemplo de un enfoque no efectivo.

#--------------------------- Algoritmo Secuencial-------------------------------------------
def tsp_secuencial(distancias):
    num_ciudades = len(distancias)
    camino = list(range(num_ciudades))
    costo_total = 0

    for i in range(num_ciudades - 1):
        costo_total += distancias[camino[i]][camino[i + 1]]

    # Incluir el costo de volver a la ciudad inicial
    costo_total += distancias[camino[-1]][camino[0]]
    return camino, costo_total

# Recorre las ciudades en el sentido que se van marcando   
# -------------------------------------------------------------------
#--------------------------- Algoritmo Genetico ---------------------------

def crear_ruta(num_ciudades):
    return random.sample(range(num_ciudades), num_ciudades)

def calcular_distancia_indices(ruta, matriz_distancias):
    #Calcula la distancia total de una ruta utilizando índices y una matriz de distancias.
    distancia = 0
    for i in range(len(ruta)):
        ciudad_origen = ruta[i]
        ciudad_destino = ruta[(i + 1) % len(ruta)]
        distancia += matriz_distancias[ciudad_origen][ciudad_destino]
    return distancia

def seleccionar_padres(poblacion, aptitud):
    #Selecciona los mejores individuos de la generación actual como padres. 
    poblacion_ordenada = sorted(zip(poblacion, aptitud), key=lambda x: x[1])
    return [individuo for individuo, _ in poblacion_ordenada[:len(poblacion)//2]]

def cruce(padre1, padre2, matriz_distancias):
    longitud_ruta = len(padre1)
    hijo = []
    ciudades_incluidas = set()

    # Crear la ruta inicial basada en distancias
    for i in range(longitud_ruta):
        if calcular_distancia_indices([padre1[i], padre1[(i + 1) % longitud_ruta]], matriz_distancias) < calcular_distancia_indices([padre2[i], padre2[(i + 1) % longitud_ruta]], matriz_distancias):
            ciudad_elegida = padre1[i]
        else:
            ciudad_elegida = padre2[i]

        if ciudad_elegida not in ciudades_incluidas:
            hijo.append(ciudad_elegida)
            ciudades_incluidas.add(ciudad_elegida)

    # Añadir ciudades faltantes
    for ciudad in range(longitud_ruta):
        if ciudad not in ciudades_incluidas:
            hijo.append(ciudad)

    return hijo


def mutar(ruta, tasa_mutacion):
    for i in range(len(ruta)):
        if random.random() < tasa_mutacion:
            j = int(random.random() * len(ruta))
            ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

def siguiente_generacion(generacion_actual, tasa_mutacion, matriz_distancias):
    aptitud = [1 / calcular_distancia_indices(ruta, matriz_distancias) for ruta in generacion_actual]
    padres = seleccionar_padres(generacion_actual, aptitud)
    descendientes = []
    longitud_deseada = len(generacion_actual) - len(padres)
    while len(descendientes) < longitud_deseada:
        padre = random.choice(padres)
        madre = random.choice(padres)
        if padre != madre:
            hijo = cruce(padre, madre, matriz_distancias)
            descendientes.append(hijo)
    siguiente_gen = padres + descendientes
    siguiente_gen = [mutar(ruta, tasa_mutacion) for ruta in siguiente_gen]
    return siguiente_gen

def algoritmo_genetico(matriz_distancias, tamano_poblacion, tasa_mutacion, generaciones):
    num_ciudades = len(matriz_distancias)
    poblacion = [crear_ruta(num_ciudades) for _ in range(tamano_poblacion)]

    for _ in range(generaciones):
        poblacion = siguiente_generacion(poblacion, tasa_mutacion, matriz_distancias)

    mejor_ruta = poblacion[0]
    mejor_distancia = calcular_distancia_indices(mejor_ruta, matriz_distancias)
    return mejor_ruta, mejor_distancia

# --------------------- ALGORITMO DEL VIAJERO CON PROGRAMACIÓN DINÁMICA ---------------------

#Este algoritmo de programación dinámica busca la solución óptima para el TSP, evitando la redundancia al almacenar resultados intermedios en la tabla dp_table.

# Esta función toma como entrada una matriz de distancias entre ciudades y devuelve la ruta óptima y su longitud.
def tsp_dinamico(matriz_distancias):
    num_ciudades = len(matriz_distancias)
    # Memoización para almacenar resultados ya calculados
    memo = {}

    # Función recursiva interna para calcular el camino óptimo
    def recorrer(conjunto, ultimo_nodo):
        # Verificar si ya hemos calculado este conjunto y último nodo
        if (tuple(conjunto), ultimo_nodo) in memo:
            return memo[(tuple(conjunto), ultimo_nodo)]

        # Caso base: si el conjunto está vacío, retornar la distancia al nodo inicial
        if not conjunto:
            return matriz_distancias[ultimo_nodo][0]

        # Calcular las distancias para los subconjuntos restantes y encontrar el mínimo
        distancias = []
        for prox_nodo in conjunto:
            nuevo_conjunto = conjunto - {prox_nodo}
            distancia = matriz_distancias[ultimo_nodo][prox_nodo] + recorrer(nuevo_conjunto, prox_nodo)
            distancias.append(distancia)

        # Almacenar el resultado en la memoización y retornarlo
        resultado = min(distancias)
        memo[(tuple(conjunto), ultimo_nodo)] = resultado
        return resultado

    # Iniciar el recorrido con el conjunto completo y el nodo inicial
    conjunto_completo = set(range(0, num_ciudades))
    longitud_optima = recorrer(conjunto_completo, 0)

    # Reconstruir el camino óptimo
    return conjunto_completo, longitud_optima

# --------------------- FUNCIONES DE MAPA ---------------------

def generar_mapa(camino, coordenadasCiudades,nombre_mapa):
    m = folium.Map(location=[-32.5, -56], zoom_start=7)

    # Agregar puntos al mapa
    for coord in coordenadasCiudades:
        folium.Marker(location=[coord['latitud'], coord['longitud']]).add_to(m)

    # Agregar líneas al mapa para conectar los puntos en el orden del camino
    route = [coordenadasCiudades[i] for i in camino]
    route.append(route[0])  # cerrar el circuito
    folium.PolyLine([(coord['latitud'], coord['longitud']) for coord in route], color="red", weight=2.5, opacity=1).add_to(m)

    # Guardar el mapa en un archivo HTML
    map_path = f"static/{nombre_mapa}.html"
    m.save(map_path)
    return map_path

# --------------------- RUTAS DE FLASK ---------------------

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/seleccionar-ciudades', methods=['POST'])
def seleccionarCiudades():
    global ciudadesAUtilizar, matrizDistanciasGlobal
    ciudadesAUtilizar = request.json.get('selectedCities', [])
    
    # Crear una matriz de distancias basada en las ciudades seleccionadas
    indicesSeleccionados = [indiceCiudades[ciudad] for ciudad in ciudadesAUtilizar]
    matrizDistanciasGlobal = [[matrizDistanciasCompleta[i][j] for j in indicesSeleccionados] for i in indicesSeleccionados]

    return jsonify({
        "message": "Ciudades seleccionadas y distancias calculadas correctamente",
        "selectedCities": ciudadesAUtilizar,
        "matrix": matrizDistanciasGlobal
    })

@app.route('/algoritmo-del-viajero', methods=['GET'])
def algoritmo_del_viajero_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = algoritmo_del_viajero(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades, "Algoritmo_del_viajero_Distancia:_" +  str(distanciaTotal))
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return jsonify({"error": str(e)}), 500
    
@app.route('/algoritmo-aleatorio', methods=['GET'])
def algoritmo_aleatorio_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = tsp_aleatorio(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades,"Algoritmo_del_viajero_Distancia:_" +  str(distanciaTotal))
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return jsonify({"error": str(e)}), 500

@app.route('/algoritmo-secuencial', methods=['GET'])
def algoritmo_secuencial_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = tsp_secuencial(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades, "Algoritmo_del_viajero_Distancia:_" +  str(distanciaTotal))
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return jsonify({"error": str(e)}), 500

@app.route('/algoritmo-genetico', methods=['GET'])
def ruta_algoritmo_genetico():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = algoritmo_genetico(matrizDistanciasGlobal, 300, 0.01, 1000)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades,"Algoritmo_del_viajero_Distancia:_" +  str(distanciaTotal))
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/programacion-dinamica', methods=['GET'])
def tsp_dinamico_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = tsp_dinamico(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades,"Algoritmo_del_viajero_Distancia:_" +  str(distanciaTotal))
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
