function manejarSeleccion(contenedorId, resultadoId, bloquearId) {
    const opciones = document.querySelectorAll(`#${contenedorId} .opcion`);
    const resultado = document.getElementById(resultadoId);
    const bloquearOpciones = document.querySelectorAll(`#${bloquearId} .opcion`);

    opciones.forEach(opcion => {
      opcion.addEventListener('click', () => {
        opcion.classList.toggle('seleccionada');

        const seleccionadas = document.querySelectorAll(`#${contenedorId} .opcion.seleccionada`);

       
    })});
}


document.addEventListener('DOMContentLoaded', () => {
    manejarSeleccion('opciones', 'resultado', 'no_opciones');
    

    document.getElementById('reset').addEventListener('click', () => {
      document.querySelectorAll('.opcion').forEach(op => {
        op.classList.remove('seleccionada', 'desactivada');
        op.style.display = '';
      });
    });
});
