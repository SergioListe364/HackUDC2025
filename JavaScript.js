    function manejarSeleccion(contenedorId, resultadoId, bloquearId) {
        const opciones = document.querySelectorAll(`#${contenedorId} .opcion`);
        const resultado = document.getElementById(resultadoId);
        const bloquearOpciones = document.querySelectorAll(`#${bloquearId} .opcion`);

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
              bloquearOpciones.forEach(op => {
                if (!op.classList.contains('seleccionada')) {
                  op.classList.remove('desactivada');
                }
              });
            } else {
              opciones.forEach(op => op.classList.remove('desactivada'));
              bloquearOpciones.forEach(op => op.classList.add('desactivada'));
            }

            // Eliminar opciones en la otra sección
            const seleccionadasText = Array.from(seleccionadas).map(op => op.textContent);
            bloquearOpciones.forEach(op => {
              if (seleccionadasText.includes(op.textContent)) {
                op.style.display = 'none';
              } else {
                op.style.display = '';
              }
            });
          });
        });
    }

    function manejarSeleccion2(contenedorId, resultadoId, bloquearId) {
        const opciones = document.querySelectorAll(`#${contenedorId} .opcion`);
        const resultado = document.getElementById(resultadoId);
        const bloquearOpciones = document.querySelectorAll(`#${bloquearId} .opcion`);

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
              bloquearOpciones.forEach(op => {
                if (!op.classList.contains('seleccionada')) {
                  op.classList.add('desactivada');
                }
              });
            }
          });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        manejarSeleccion('opciones', 'resultado', 'no_opciones');
        manejarSeleccion2('no_opciones', 'no_resultado', 'opciones');

        document.getElementById('reset').addEventListener('click', () => {
          document.querySelectorAll('.opcion').forEach(op => {
            op.classList.remove('seleccionada', 'desactivada');
            op.style.display = '';
          });
        });
    });
