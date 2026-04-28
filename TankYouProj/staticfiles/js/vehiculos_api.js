// Este mensaje debe salir SIEMPRE al cargar la página
console.log('JS de vehículos cargado');

function cargarVehiculos() {
    console.log('BOTÓN PULSADO');

    const contenedor = document.getElementById('vehiculosResultado');

    if (!contenedor) {
        console.error('No existe el div vehiculosResultado');
        return;
    }

    contenedor.innerHTML = 'Cargando vehículos...';

    fetch('/api/vehiculos_list/')
        .then(response => {
            console.log('Respuesta GET:', response);
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);

            contenedor.innerHTML = '';

            data.results.forEach(v => {
                contenedor.innerHTML += `
                    <div class="border p-2 mb-2">
                        <strong>${v.marca}</strong> - ${v.modelo}
                    </div>
                `;
            });
        })
        .catch(error => {
            console.error('Error en fetch:', error);
            contenedor.innerHTML = 'Error al cargar los datos';
        });
}
