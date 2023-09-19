import folium

# Crea un objeto de mapa centrado en Uruguay
uruguay_map = folium.Map(location=[-32.794044, -56.018652], zoom_start=7)

# Añade marcadores para algunas ciudades de Uruguay
cities = [
    {"name": "Montevideo", "coordinates": [-34.901112, -56.164531]},
    {"name": "Salto", "coordinates": [-31.383365, -57.968678]},
    {"name": "Punta del Este", "coordinates": [-34.959436, -54.943848]},
    # Agrega más ciudades aquí
]

for city in cities:
    folium.Marker(
        location=city["coordinates"],
        popup=city["name"]
    ).add_to(uruguay_map)

# Guarda el mapa en un archivo HTML
uruguay_map.save("mapa_uruguay.html")

# Abre el archivo HTML en tu navegador web
import webbrowser
webbrowser.open("mapa_uruguay.html")
