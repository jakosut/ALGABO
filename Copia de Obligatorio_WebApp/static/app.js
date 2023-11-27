// // Lista de ciudades de Uruguay
// const ciudadesUruguay = [
//   "Artigas",
//   "Canelones",
//   "Melo",
//   "Colonia",
//   "Durazno",
//   "Trinidad",
//   "Florida",
//   "Lavalleja",
//   "Maldonado",
//   "Montevideo",
//   "Paysandú",
//   "Fray Bentos",
//   "Rivera",
//   "Rocha",
//   "Salto",
//   "San José",
//   "Mercedes",
//   "Tacuarembó",
//   "Treinta y Tres",
// ];

// // Llenar las opciones de ciudades
// const seleccionCiudades = document.getElementById("citiesSelection");
// ciudadesUruguay.forEach((ciudad) => {
//   seleccionCiudades.innerHTML += `<label><input type="checkbox" name="cities" value="${ciudad}"> ${ciudad}</label>`;
// });

// function generarMatriz() {
//   const ciudadesSeleccionadas = [];
//   document
//     .querySelectorAll('input[name="cities"]:checked')
//     .forEach((checkbox) => {
//       ciudadesSeleccionadas.push(checkbox.value);
//     });

//   // Mostrar el efecto de carga
//   mostrarSpinnerMatrix();

//   fetch("/seleccionar-ciudades", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({ selectedCities: ciudadesSeleccionadas }),
//   })
//     .then((respuesta) => respuesta.json())
//     .then((datos) => {
//       ocultarSpinnerMatrix();
//       mostrarMatriz(datos.matrix, datos.selectedCities);
//     })
//     .catch((error) => {
//       // Ocultar el efecto de carga en caso de error
//       ocultarSpinnerMatrix();
//       console.error("Error al obtener datos:", error);
//     });
// }

// function mostrarMatriz(matriz, ciudadesSeleccionadas) {
//   const contenedorMatriz = document.getElementById("matrixContainer");
//   let html = "<table>";
//   html += "<thead><tr><th></th>"; // Celda vacía en la esquina superior izquierda

//   // Encabezados de la tabla
//   for (let ciudad of ciudadesSeleccionadas) {
//     html += `<th>${ciudad}</th>`;
//   }
//   html += "</tr></thead><tbody>";

//   // Filas de la matriz
//   for (let i = 0; i < matriz.length; i++) {
//     html += `<tr><td>${ciudadesSeleccionadas[i]}</td>`; // Nombre de la ciudad
//     for (let j = 0; j < matriz[i].length; j++) {
//       html += `<td>${matriz[i][j]}</td>`;
//     }
//     html += "</tr>";
//   }

//   html += "</tbody></table>";
//   contenedorMatriz.innerHTML = html;

//   // Mostrar el título "Matriz de Distancias:" y la selección de algoritmo
//   document.getElementById("matrixTitle").style.display = "block";
//   document.getElementById("seleccionAlgoritmo").style.display = "block";
// }

// function generarMapa() {
//   const algoritmoSeleccionado = document.getElementById("opcionMapa").value;
//   let url = "";
  
//   switch (algoritmoSeleccionado) {
//     case "opcion1":
//       url = "/algoritmo-del-viajero";
//       break;
//     case "opcion2":
//       url = "/algoritmo-aleatorio";
//       break;
//     case "opcion3":
//       url = "/algoritmo-secuencial";
//       break;
//     case "opcion4":
//       url = "/algoritmo-genetico";
//       break;
//     default:
//       console.error("Algoritmo no seleccionado");
//       return;
//   }

//   // Mostrar el efecto de carga
//   mostrarSpinnerMap();

//   fetch(url)
//     .then((respuesta) => {
//       if (!respuesta.ok) {
//         throw new Error("Error en el servidor");
//       }
//       return respuesta.json();
//     })
//     .then((datos) => {
//       if (datos.error) {
//         console.error("Error del servidor:", datos.error);
//         return;
//       }
//       ocultarSpinnerMap();

//       // Mostrar el camino y la distancia total en la consola y en la web
//       console.log("Camino:", datos.camino);
//       console.log("Distancia total:", datos.distanciaTotal);
//       document.getElementById("caminoResultado").innerText = "Camino: " + datos.camino.join(" -> ");
//       document.getElementById("distanciaResultado").innerText = "Distancia total: " + datos.distanciaTotal.toFixed(2) + " km";
//       document.getElementById("resultadoAlgoritmo").style.display = "block";

//       // Eliminar el iframe existente, si hay alguno
//       const existingIframe = document.querySelector("#resultadoAlgoritmo iframe");
//       if (existingIframe) {
//         existingIframe.remove();
//       }

//       // Mostrar el mapa en un nuevo iframe
//       const iframe = document.createElement("iframe");
//       iframe.src = datos.mapPath;
//       iframe.width = "100%";
//       iframe.height = "600px";
//       document.getElementById("resultadoAlgoritmo").appendChild(iframe);
//     })
//     .catch((error) => {
//       ocultarSpinnerMap();
//       console.error("Error al obtener datos:", error);
//     });
// }


// function mostrarSpinnerMap() {
//   const loadingMap = document.getElementById("loadingMap");
//   loadingMap.style.setProperty("display", "flex", "important");
// }

// function ocultarSpinnerMap() {
//   const loadingMap = document.getElementById("loadingMap");
//   loadingMap.style.setProperty("display", "none", "important");
// }

// function mostrarSpinnerMatrix() {
//   const loadingMatrix = document.getElementById("loadingMatrix");
//   loadingMatrix.style.setProperty("display", "flex", "important");
// }

// function ocultarSpinnerMatrix() {
//   const loadingMatrix = document.getElementById("loadingMatrix");
//   loadingMatrix.style.setProperty("display", "none", "important");
// }

// /////////////////////////////////////////////

// function verificarResultados(nombreAlgoritmo) {
//   fetch(`/obtener-resultados/${nombreAlgoritmo}`)
//       .then(response => response.json())
//       .then(data => {
//           if (data.mapPath) {
//               console.log(`Resultados del algoritmo ${nombreAlgoritmo}:`, data);
//               mostrarResultados(data);
//           } else {
//               console.log(`Esperando resultados del algoritmo ${nombreAlgoritmo}...`);
//               setTimeout(() => verificarResultados(nombreAlgoritmo), 5000); // Revisa de nuevo después de 5 segundos
//           }
//       })
//       .catch(error => console.error(`Error al obtener resultados del algoritmo ${nombreAlgoritmo}:`, error));
// }

/////////////////////////////////////////////


// Lista de ciudades de Uruguay
const ciudadesUruguay = [
  "Artigas",
  "Canelones",
  "Melo",
  "Colonia",
  "Durazno",
  "Trinidad",
  "Florida",
  "Lavalleja",
  "Maldonado",
  "Montevideo",
  "Paysandú",
  "Fray Bentos",
  "Rivera",
  "Rocha",
  "Salto",
  "San José",
  "Mercedes",
  "Tacuarembó",
  "Treinta y Tres",
];

// Llenar las opciones de ciudades
const seleccionCiudades = document.getElementById("citiesSelection");
ciudadesUruguay.forEach((ciudad) => {
  seleccionCiudades.innerHTML += `<label><input type="checkbox" name="cities" value="${ciudad}"> ${ciudad}</label>`;
});

// Función para generar la matriz de distancias
function generarMatriz() {
  const ciudadesSeleccionadas = [];
  document.querySelectorAll('input[name="cities"]:checked').forEach((checkbox) => {
    ciudadesSeleccionadas.push(checkbox.value);
  });

  mostrarSpinnerMatrix();

  fetch("/seleccionar-ciudades", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ selectedCities: ciudadesSeleccionadas }),
  })
  .then((respuesta) => respuesta.json())
  .then((datos) => {
    ocultarSpinnerMatrix();
    mostrarMatriz(datos.matrix, datos.selectedCities);
  })
  .catch((error) => {
    ocultarSpinnerMatrix();
    console.error("Error al obtener datos:", error);
  });
}

function mostrarMatriz(matriz, ciudadesSeleccionadas) {
  const contenedorMatriz = document.getElementById("matrixContainer");
  let html = "<table>";
  html += "<thead><tr><th></th>"; // Celda vacía en la esquina superior izquierda

  // Encabezados de la tabla
  for (let ciudad of ciudadesSeleccionadas) {
    html += `<th>${ciudad}</th>`;
  }
  html += "</tr></thead><tbody>";

  // Filas de la matriz
  for (let i = 0; i < matriz.length; i++) {
    html += `<tr><td>${ciudadesSeleccionadas[i]}</td>`; // Nombre de la ciudad
    for (let j = 0; j < matriz[i].length; j++) {
      html += `<td>${matriz[i][j]}</td>`;
    }
    html += "</tr>";
  }
}

// Función para iniciar el algoritmo y verificar los resultados
function generarMapa() {
  const algoritmoSeleccionado = document.getElementById("opcionMapa").value;
  let url = "";

  switch (algoritmoSeleccionado) {
    case "opcion1":
      url = "/algoritmo-del-viajero";
      break;
    // ... otras opciones ...
  }

  mostrarSpinnerMap();

  fetch(url)
    .then((respuesta) => {
      if (!respuesta.ok) {
        throw new Error("Error en el servidor");
      }
      return respuesta.json();
    })
    .then((datos) => {
      console.log(datos.message);
      ocultarSpinnerMap();
      verificarResultados(algoritmoSeleccionado); // Inicia la verificación de los resultados
    })
    .catch((error) => {
      ocultarSpinnerMap();
      console.error("Error al iniciar el algoritmo:", error);
    });
}

// Función para verificar los resultados de manera periódica
function verificarResultados(algoritmoSeleccionado) {
  fetch(`/obtener-resultados/${algoritmoSeleccionado}`)
    .then(response => response.json())
    .then(data => {
      if (data.mapPath) {
        console.log("Resultados del algoritmo:", data);
        mostrarResultados(data);
      } else {
        console.log("Esperando resultados...");
        setTimeout(() => verificarResultados(algoritmoSeleccionado), 5000);
      }
    })
    .catch(error => console.error('Error al obtener resultados:', error));
}

function mostrarResultados(data) {
  // Implementar lógica para mostrar los resultados
  // Por ejemplo, actualizar el DOM con los datos de 'data'
}

// Funciones para mostrar y ocultar los spinners
function mostrarSpinnerMap() {
  const loadingMap = document.getElementById("loadingMap");
  loadingMap.style.display = "flex";
}

function ocultarSpinnerMap() {
  const loadingMap = document.getElementById("loadingMap");
  loadingMap.style.display = "none";
}

function mostrarSpinnerMatrix() {
  const loadingMatrix = document.getElementById("loadingMatrix");
  loadingMatrix.style.display = "flex";
}

function ocultarSpinnerMatrix() {
  const loadingMatrix = document.getElementById("loadingMatrix");
  loadingMatrix.style.display = "none";
}