// Lista de ciudades de Uruguay
const ciudadesUruguay = [
    "Artigas", "Canelones", "Melo", "Colonia", "Durazno", "Trinidad", 
    "Florida", "Lavalleja", "Maldonado", "Montevideo", "Paysandú", "Río Negro", 
    "Rivera", "Rocha", "Salto", "San José", "Mercedes", "Tacuarembó", "Treinta y Tres"
];

// Llenar las opciones de ciudades
const seleccionCiudades = document.getElementById('citiesSelection');
ciudadesUruguay.forEach(ciudad => {
    seleccionCiudades.innerHTML += `<label><input type="checkbox" name="cities" value="${ciudad}"> ${ciudad}</label>`;
});

function generarMatriz() {
    const ciudadesSeleccionadas = [];
    document.querySelectorAll('input[name="cities"]:checked').forEach(checkbox => {
        ciudadesSeleccionadas.push(checkbox.value);
    });
    
    fetch('/seleccionar-ciudades', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({selectedCities: ciudadesSeleccionadas})
    })
    .then(respuesta => respuesta.json())
    .then(datos => {
        mostrarMatriz(datos.matrix, datos.selectedCities);
    });
}

function mostrarMatriz(matriz, ciudadesSeleccionadas) {
    const contenedorMatriz = document.getElementById('matrixContainer');
    let html = '<table>';
    html += '<thead><tr><th></th>'; // Celda vacía en la esquina superior izquierda

    // Encabezados de la tabla
    for (let ciudad of ciudadesSeleccionadas) {
        html += `<th>${ciudad}</th>`;
    }
    html += '</tr></thead><tbody>';

    // Filas de la matriz
    for (let i = 0; i < matriz.length; i++) {
        html += `<tr><td>${ciudadesSeleccionadas[i]}</td>`; // Nombre de la ciudad
        for (let j = 0; j < matriz[i].length; j++) {
            html += `<td>${matriz[i][j]}</td>`;
        }
        html += '</tr>';
    }

    html += '</tbody></table>';
    contenedorMatriz.innerHTML = html;

    // Mostrar el título "Matriz de Distancias:" y la selección de algoritmo
    document.getElementById('matrixTitle').style.display = 'block';
    document.getElementById('seleccionAlgoritmo').style.display = 'block';
}

function generarMapa() {
    const algoritmoSeleccionado = document.getElementById('opcionMapa').value;
    if (algoritmoSeleccionado === 'opcion1') {
        fetch('/algoritmo-vecino-cercano')
        .then(respuesta => {
            if (!respuesta.ok) {
                throw new Error('Error en el servidor');
            }
            return respuesta.json();
        })
        .then(datos => {
            if (datos.error) {
                console.error("Error del servidor:", datos.error);
                return;
            }

            // Mostrar el camino y la distancia total en la consola
            console.log("Camino:", datos.camino);
            console.log("Distancia total:", datos.distanciaTotal);

            // Mostrar el camino y la distancia total en la web
            document.getElementById('caminoResultado').innerText = "Camino: " + datos.camino.join(" -> ");
            document.getElementById('distanciaResultado').innerText = "Distancia total: " + datos.distanciaTotal.toFixed(2) + " km";
            document.getElementById('resultadoAlgoritmo').style.display = 'block';

            // Eliminar el iframe existente, si hay alguno
            const existingIframe = document.querySelector('#resultadoAlgoritmo iframe');
            if (existingIframe) {
                existingIframe.remove();
            }

            // Mostrar el mapa en un nuevo iframe
            const iframe = document.createElement('iframe');
            iframe.src = datos.mapPath;
            iframe.width = "100%";
            iframe.height = "600px";
            document.getElementById('resultadoAlgoritmo').appendChild(iframe);
        })
        .catch(error => {
            console.error("Error al obtener datos:", error);
        });
    }
}

