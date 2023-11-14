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

# --------------------- FUNCIONES DE COORDENADAS Y DISTANCIAS ---------------------

# Función para obtener las coordenadas de las ciudades
def obtener_coordenadas(ciudad):
    base_url = "https://nominatim.openstreetmap.org/search"
    parametros = {
        "city": ciudad,
        "format": "json"
    }

    respuesta = requests.get(base_url, params=parametros)
    
    if respuesta.status_code != 200:
        raise Exception(f"Error al obtener datos de Nominatim para la ciudad {ciudad}")
    
    datos = respuesta.json()
    for lugar in datos:
        if es_ciudad_en_uruguay(lugar.get("display_name", "")):
            return {
                "nombre": ciudad,
                "latitud": float(lugar["lat"]),
                "longitud": float(lugar["lon"])
            }

    return {
        "nombre": ciudad,
        "latitud": None,
        "longitud": None
    }

def es_ciudad_en_uruguay(display_name):
    name = display_name.split(",")
    pais = name[-1].strip()
    return pais == "Uruguay"

def obtener_distancia_osrm(coord1, coord2):

    base_url = "http://router.project-osrm.org/route/v1/driving"
    coordenadas_ruta = f"{coord1['longitud']},{coord1['latitud']};{coord2['longitud']},{coord2['latitud']}"
    url_completa = f"{base_url}/{coordenadas_ruta}?overview=false"
    
    # Solicita la información de distancia al servicio OSRM usando la URL completa
    respuesta = requests.get(url_completa)
    data = respuesta.json()

    # Verifica si la respuesta tiene la información que necesitamos
    if 'routes' not in data:
        raise Exception(f"Error al obtener ruta entre {coord1} y {coord2}")

    # Extrae la distancia de la respuesta. Está en metros, así que la convertimos a kilómetros
    distancia_en_metros = data['routes'][0]['distance']
    distancia_en_kilometros = distancia_en_metros / 1000
    
    # Devuelve la distancia en kilómetros
    return distancia_en_kilometros

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
    ciudades = list(range(len(distancias)))
    random.shuffle(ciudades)
    costo_total = 0
    camino = []

    for i in range(len(ciudades) - 1):
        ciudad_actual = ciudades[i]
        siguiente_ciudad = ciudades[i + 1]
        costo_actual = distancias[ciudad_actual][siguiente_ciudad]
        costo_total += costo_actual
        camino.append(ciudad_actual)

    # Volver a la ciudad inicial
    ciudad_inicial = ciudades[-1]
    ciudad_final = ciudades[0]
    costo_final = distancias[ciudad_inicial][ciudad_final]
    costo_total += costo_final
    camino.append(ciudad_final)

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
# --------------------- FUNCIONES DE MAPA ---------------------

def generar_mapa(camino, coordenadasCiudades):
    m = folium.Map(location=[-32.5, -56], zoom_start=7)

    # Agregar puntos al mapa
    for coord in coordenadasCiudades:
        folium.Marker(location=[coord['latitud'], coord['longitud']]).add_to(m)

    # Agregar líneas al mapa para conectar los puntos en el orden del camino
    route = [coordenadasCiudades[i] for i in camino]
    route.append(route[0])  # cerrar el circuito
    folium.PolyLine([(coord['latitud'], coord['longitud']) for coord in route], color="red", weight=2.5, opacity=1).add_to(m)

    # Guardar el mapa en un archivo HTML
    map_path = "static/uruguay_map.html"
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
    
    # Obteniendo coordenadas
    coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]

    # Crear una matriz de distancias
    numCiudades = len(ciudadesAUtilizar)
    matrizDistancias = []

    # Recorre cada ciudad para crear las filas de la matriz
    for i in range(numCiudades):
        # Crea una fila vacía para la matriz
        fila = []
        # Recorre nuevamente cada ciudad para llenar la fila con valores de distancia (inicialmente 0.0)
        for j in range(numCiudades):
            fila.append(0.0)
        # Añade la fila completa a la matriz
        matrizDistancias.append(fila)

    # Llenar la matriz con las distancias entre cada par de ciudades
    for i, ciudad1 in enumerate(coordenadasCiudades):
        for j, ciudad2 in enumerate(coordenadasCiudades):
            if i < j:  # Evita comparar la ciudad consigo misma y repetir pares
                distancia = obtener_distancia_osrm(ciudad1, ciudad2)
                matrizDistancias[i][j] = distancia
                matrizDistancias[j][i] = distancia  # La matriz es simétrica

    matrizDistanciasGlobal = matrizDistancias

    return jsonify({
        "message": "Ciudades seleccionadas y distancias calculadas correctamente",
        "selectedCities": ciudadesAUtilizar,
        "matrix": matrizDistancias
    })

@app.route('/algoritmo-del-viajero', methods=['GET'])
def algoritmo_del_viajero_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = algoritmo_del_viajero(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades)
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/algoritmo-aleatorio', methods=['GET'])
def algoritmo_aleatorio_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = tsp_aleatorio(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades)
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/algoritmo-secuencial', methods=['GET'])
def algoritmo_secuencial_app():
    try:
        global ciudadesAUtilizar, matrizDistanciasGlobal
        camino, distanciaTotal = tsp_secuencial(matrizDistanciasGlobal)
        coordenadasCiudades = [obtener_coordenadas(ciudad) for ciudad in ciudadesAUtilizar]
        map_path = generar_mapa(camino, coordenadasCiudades)
        return jsonify({
            "camino": [ciudadesAUtilizar[i] for i in camino],
            "distanciaTotal": distanciaTotal,
            "mapPath": map_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
