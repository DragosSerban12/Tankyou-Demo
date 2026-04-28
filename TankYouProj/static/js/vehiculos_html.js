// Este script reconstruye dinámicamente el listado de vehículos
// a partir del HTML generado inicialmentes

document.addEventListener("DOMContentLoaded", () => { // Espero a que el DOM esté cargado antes de manipularlo
    const row = document.querySelector(".row"); // Busco el contenedor principal del listado, sino el script para
    if (!row) return;

    // Leer vehículos desde el HTML generado por Django
    const cards = row.querySelectorAll(".card"); // Saco los datos de las tarjetas del html
    const vehiculos = [];

    cards.forEach(card => { // Recorro cada tarjeta
        const titulo = card.querySelector(".card-title")?.innerText || ""; // Saco el titulo de la tarjeta
        const textos = card.querySelectorAll("p"); // Saco los textos de la tarjeta

        const matricula = textos[0]?.innerText.replace("Matrícula:", "").trim(); // Saco la matricula de la tarjeta
        const combustible = textos[1]?.innerText.replace("Combustible:", "").trim(); // Saco el combustible de la tarjeta
        const anyo = textos[2]?.innerText.replace("Año:", "").trim(); // Saco el año de la tarjeta

        const img = card.querySelector("img")?.src; // Saco la imagen de la tarjeta

        const botones = card.querySelectorAll("a"); // Saco los botones de la tarjeta
        const editarUrl = botones[0]?.href;  // Saco la url de editar de la tarjeta
        const fotosUrl = botones[1]?.href; // Saco la url de fotos de la tarjeta
        const borrarUrl = botones[2]?.href; // Saco la url de borrar de la tarjeta

        vehiculos.push({ // Paso de html a una estructura de datos js
            titulo,
            matricula,
            combustible,
            anyo,
            img,
            editarUrl,
            fotosUrl,
            borrarUrl
        });
    });

    // Borrar HTML original
    row.innerHTML = "";

    // Caso: no hay vehículos
    if (vehiculos.length === 0) {
        row.innerHTML = `
            <div class="col-12">
                <div class="card text-center p-5 shadow-sm">
                    <h5 class="mb-3">No dispones de vehículos</h5>
                    <p class="text-muted">Añade tu primer vehículo para empezar</p>
                </div>
            </div>
        `;
        return;
    }

    // Reconstruir tarjetas dinámicamente
    vehiculos.forEach(v => {
        const col = document.createElement("div");
        col.className = "col-md-6 col-lg-4 mb-4";

        col.innerHTML = `
            <div class="card shadow-sm h-100">
                <img src="${v.img}"
                     class="card-img-top"
                     style="height:220px; object-fit:cover;">

                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${v.titulo}</h5>

                    <p class="mb-1"><strong>Matrícula:</strong> ${v.matricula}</p>
                    <p class="mb-1"><strong>Combustible:</strong> ${v.combustible}</p>
                    <p class="mb-3"><strong>Año:</strong> ${v.anyo}</p>

                    <div class="mt-auto d-flex justify-content-end gap-2">
                        <a href="${v.editarUrl}"
                           class="btn btn-outline-secondary btn-sm">
                            Editar
                        </a>

                        <a href="${v.fotosUrl}"
                           class="btn btn-outline-primary btn-sm">
                            Ver más fotos
                        </a>

                        <a href="${v.borrarUrl}"
                           class="btn btn-outline-danger btn-sm">
                            Borrar
                        </a>
                    </div>
                </div>
            </div>
        `;

        row.appendChild(col);
    });
});
