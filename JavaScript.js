function manejarSeleccion(contenedorId, resultadoId) {
    const opciones = document.querySelectorAll(`#${contenedorId} .opcion`);
    const resultado = document.getElementById(resultadoId);
    const contenedor = document.getElementById(contenedorId);

    opciones.forEach(opcion => {
      opcion.addEventListener('click', () => {
        opcion.classList.toggle('seleccionada');

        const seleccionadas = document.querySelectorAll(`#${contenedorId} .opcion.seleccionada`);

        if (seleccionadas.length >= 3) {
          opciones.forEach(op => {
            if (!op.classList.contains('seleccionada')) {
              op.classList.add('desactivada');
            }
          });
        } else {
          opciones.forEach(op => op.classList.remove('desactivada'));
        }

      });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    manejarSeleccion('opciones', 'resultado');
    manejarSeleccion('no_opciones', 'no_resultado');
});
