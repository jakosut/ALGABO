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

let mapUrls = [];


// Llenar las opciones de ciudades
const seleccionCiudades = document.getElementById("citiesSelection");
ciudadesUruguay.forEach((ciudad) => {
  seleccionCiudades.innerHTML += `<label><input type="checkbox" name="cities" value="${ciudad}"> ${ciudad}</label>`;
});

function generarMatriz() {
  const ciudadesSeleccionadas = [];
  document
    .querySelectorAll('input[name="cities"]:checked')
    .forEach((checkbox) => {
      ciudadesSeleccionadas.push(checkbox.value);
    });

  // Mostrar el efecto de carga
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
      // Ocultar el efecto de carga en caso de error
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

  html += "</tbody></table>";
  contenedorMatriz.innerHTML = html;

  // Mostrar el título "Matriz de Distancias:" y la selección de algoritmo
  document.getElementById("matrixTitle").style.display = "block";
  document.getElementById("seleccionAlgoritmo").style.display = "block";
}

function generarMapa() {
  const algoritmoSeleccionado = document.getElementById("opcionMapa").value;
  let url = "";
  
  switch (algoritmoSeleccionado) {
      case "opcion1":
          url = "/algoritmo-del-viajero";
          break;
      case "opcion2":
          url = "/algoritmo-aleatorio";
          break;
      case "opcion3":
          url = "/algoritmo-secuencial";
          break;
      case "opcion4":
          url = "/algoritmo-genetico";
          break;
      case "opcion5":
          url = "/programacion-dinamica";
          break;
      default:
          console.error("Algoritmo no seleccionado");
          return;
  }

  // Mostrar el efecto de carga
  mostrarSpinnerMap();

  fetch(url)
      .then((respuesta) => {
          if (!respuesta.ok) {
              throw new Error("Error en el servidor");
          }
          return respuesta.json();
      })
      .then((datos) => {
          if (datos.error) {
              console.error("Error del servidor:", datos.error);
              return;
          }
          ocultarSpinnerMap();

          // Mostrar el camino y la distancia total en la consola y en la web
          console.log("Camino:", datos.camino);
          console.log("Distancia total:", datos.distanciaTotal);
          document.getElementById("caminoResultado").innerText = "Camino: " + datos.camino.join(" -> ");
          document.getElementById("distanciaResultado").innerText = "Distancia total: " + datos.distanciaTotal.toFixed(2) + " km";
          document.getElementById("resultadoAlgoritmo").style.display = "block";

          // Eliminar el iframe existente, si hay alguno
          const existingIframe = document.querySelector("#resultadoAlgoritmo iframe");
          if (existingIframe) {
              existingIframe.remove();
          }

          // Mostrar el mapa en un nuevo iframe
          const iframe = document.createElement("iframe");
          iframe.src = datos.mapPath;
          iframe.width = "100%";
          iframe.height = "600px";
          document.getElementById("resultadoAlgoritmo").appendChild(iframe);

          // Almacena la URL del mapa con el nombre del algoritmo
          mapUrls.push({ name: algoritmoSeleccionado, url: datos.mapPath });
      })
      .catch((error) => {
          ocultarSpinnerMap();
          console.error("Error al obtener datos:", error);
      });
}

function mostrarTodosLosMapas() {
  let htmlContent = "<html><head><style>";
  htmlContent += ".grid-container { display: grid; grid-template-columns: auto auto; gap: 20px; padding: 20px; }";
  htmlContent += ".grid-item { text-align: center; }";
  htmlContent += "iframe { width: 100%; height: 600px; border: 1px solid #ddd; }";
  htmlContent += "</style></head><body>";
  htmlContent += "<div class='grid-container'>";

  mapUrls.forEach(item => {
      let nombreAmigable = item.url
                            .replace('static/', '')
                            .replace('.html', ' Km');

      htmlContent += `<div class='grid-item'><h2> ${nombreAmigable}</h2>`;
      htmlContent += `<iframe src="${item.url}"></iframe></div>`;
  });

  htmlContent += "</div></body></html>";

  const newWindow = window.open("", "_blank");
  newWindow.document.write(htmlContent);
  newWindow.document.close();
}


function mostrarSpinnerMap() {
  const loadingMap = document.getElementById("loadingMap");
  loadingMap.style.setProperty("display", "flex", "important");
}

function ocultarSpinnerMap() {
  const loadingMap = document.getElementById("loadingMap");
  loadingMap.style.setProperty("display", "none", "important");
}

function mostrarSpinnerMatrix() {
  const loadingMatrix = document.getElementById("loadingMatrix");
  loadingMatrix.style.setProperty("display", "flex", "important");
}

function ocultarSpinnerMatrix() {
  const loadingMatrix = document.getElementById("loadingMatrix");
  loadingMatrix.style.setProperty("display", "none", "important");
}


