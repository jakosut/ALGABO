import requests


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
    # Divide la cadena en partes usando la coma como separador
    name = display_name.split(",")
    
    # Toma la última parte (que debería ser el país) y elimina espacios en blanco
    pais = name[-1].strip()
    
    # Verifica si el país es "Uruguay"
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

# Lista de ciudades de Uruguay
ciudades_uruguay = [
    "Artigas", "Canelones", "Melo", "Colonia", "Durazno", "Trinidad", 
    "Florida", "Lavalleja", "Maldonado", "Montevideo", "Paysandú", "Río Negro", 
    "Rivera", "Rocha", "Salto", "San José", "Mercedes", "Tacuarembó", "Treinta y Tres"
]

# Obteniendo coordenadas
coordenadas_ciudades = [obtener_coordenadas(ciudad) for ciudad in ciudades_uruguay]

# Crear una matriz de distancias
num_ciudades = len(ciudades_uruguay)

# Inicializa una lista vacía para almacenar las filas de la matriz
matriz_distancias = []

# Recorre cada ciudad para crear las filas de la matriz
for i in range(num_ciudades):
    # Crea una fila vacía para la matriz
    fila = []
    # Recorre nuevamente cada ciudad para llenar la fila con valores de distancia (inicialmente 0.0)
    for j in range(num_ciudades):
        fila.append(0.0)
    # Añade la fila completa a la matriz
    matriz_distancias.append(fila)

# Llenar la matriz con las distancias entre cada par de ciudades
for i, ciudad1 in enumerate(coordenadas_ciudades):
    for j, ciudad2 in enumerate(coordenadas_ciudades):
        if i < j:  # Evita comparar la ciudad consigo misma y repetir pares
            distancia = obtener_distancia_osrm(ciudad1, ciudad2)
            matriz_distancias[i][j] = distancia
            matriz_distancias[j][i] = distancia  # La matriz es simétrica

# Imprimir la matriz
print(matriz_distancias)


# # Imprimir las ciudades y la matriz
# print(" " * 15 + "|", end="")
# for ciudad in ciudades_uruguay:
#     print(f"{ciudad[:10]:<15}", end="")
# print()
# print("-" * (15 * (num_ciudades + 1)))

# for i, fila in enumerate(matriz_distancias):
#     print(f"{ciudades_uruguay[i][:10]:<15}|", end="")
#     for j, distancia in enumerate(fila):
#         print(f"{distancia:<15.2f}", end="")
#     print()

