document.addEventListener('DOMContentLoaded', function () {
  const nombreInput = document.querySelector('input[name="nombres"]');

  const errorDiv = document.createElement('div');
  errorDiv.style.color = 'red';
  errorDiv.style.marginTop = '5px';
  nombreInput.parentNode.appendChild(errorDiv);

  const numerosRomanos = {
    '1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V',
    '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X'
  };

  nombreInput.addEventListener('input', function () {
    let valor = nombreInput.value;

    // Convertir todos los números (del 1 al 10) a romanos con regex global
    // Usamos un callback para cada match que retorna el romano correspondiente
    valor = valor.replace(/\b(10|[1-9])\b/g, function(match) {
      return numerosRomanos[match];
    });

    // Actualizamos el input solo si cambió para no resetear cursor innecesariamente
    if (nombreInput.value !== valor) {
      const start = nombreInput.selectionStart;
      const end = nombreInput.selectionEnd;
      nombreInput.value = valor;

      // Intentamos preservar la posición del cursor (puede fallar en algunos casos)
      nombreInput.setSelectionRange(start, end);
    }

    const letrasEspacios = /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]*$/;
    const soloLetras = valor.replace(/\s/g, '');
    const espacios = (valor.match(/ /g) || []).length;

    let mensaje = '';
    if (!letrasEspacios.test(valor)) {
      mensaje = 'El nombre solo puede contener letras y espacios.';
    } else if (soloLetras.length < 3) {
      mensaje = 'El nombre debe tener al menos 3 letras.';
    } else if (espacios > 2) {
      mensaje = 'El nombre solo puede tener hasta dos espacios.';
    }

    errorDiv.textContent = mensaje;
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const apellidoInput = document.querySelector('input[name="apellidos"]');

  const errorDiv = document.createElement('div');
  errorDiv.style.color = 'red';
  errorDiv.style.marginTop = '5px';
  apellidoInput.parentNode.appendChild(errorDiv);

  const numerosRomanos = {
    '1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V',
    '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X'
  };

  apellidoInput.addEventListener('input', function () {
    let valor = apellidoInput.value;

    // Convertir números (1-10) a romanos
    valor = valor.replace(/\b(10|[1-9])\b/g, match => numerosRomanos[match]);

    // Evitar más de un espacio y que esté entre letras (no al inicio ni al final)
    // Para esto: 
    // 1. Contamos espacios
    const espacios = (valor.match(/ /g) || []).length;

    // 2. Validamos que no haya espacios al inicio o al final
    const espacioInicioFin = /^\s|\s$/.test(valor);

    // 3. Validamos caracteres permitidos: letras y espacio
    const letrasEspacios = /^[A-Za-zÁÉÍÓÚáéíóúÑñ ]*$/;

    // 4. Eliminar más de un espacio dejando solo el primero entre palabras
    if (espacios > 1) {
      // Quitamos espacios extras dejando solo el primero
      let primeraPos = valor.indexOf(' ');
      valor = valor.slice(0, primeraPos + 1) + valor.slice(primeraPos + 1).replace(/ /g, '');
    }

    // Actualizar valor si cambió
    if (apellidoInput.value !== valor) {
      const start = apellidoInput.selectionStart;
      const end = apellidoInput.selectionEnd;
      apellidoInput.value = valor;
      apellidoInput.setSelectionRange(start, end);
    }

    const soloLetras = valor.replace(/\s/g, '');
    let mensaje = '';

    if (!letrasEspacios.test(valor)) {
      mensaje = 'El apellido solo puede contener letras y espacios.';
    } else if (soloLetras.length < 3) {
      mensaje = 'El apellido debe tener al menos 3 letras.';
    } else if (espacios > 1) {
      mensaje = 'Solo se permite un espacio entre palabras.';
    } else if (espacioInicioFin) {
      mensaje = 'No se permiten espacios al inicio o al final.';
    }

    errorDiv.textContent = mensaje;
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const ciInput = document.querySelector('input[name="ci"]');

  const ciError = document.createElement('div');
  ciError.style.color = 'red';
  ciError.style.marginTop = '5px';
  ciInput.parentNode.appendChild(ciError);

  ciInput.addEventListener('input', function () {
    let valor = ciInput.value;
    let mensaje = '';

    // Eliminar todo lo que no sea número
    valor = valor.replace(/\D/g, '');
    ciInput.value = valor;

    if (valor === '') {
      mensaje = 'El CI no puede estar vacío.';
    } else if (!/^\d+$/.test(valor)) {
      mensaje = 'El CI solo puede contener números.';
    } else if (valor.length < 7 || valor.length > 8) {
      mensaje = 'El CI debe tener 7 u 8 dígitos.';
    }

    ciError.textContent = mensaje;
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const fechaInput = document.querySelector('input[name="fecha_nacimiento"]');

  const fechaError = document.createElement('div');
  fechaError.className = 'text-red-500 text-sm mt-1 transition-opacity duration-300 opacity-0';
  fechaInput.parentNode.appendChild(fechaError);

  fechaInput.addEventListener('input', function () {
    const valor = fechaInput.value;
    const mensaje = validarFecha(valor);
    fechaError.textContent = mensaje;
    fechaError.style.opacity = mensaje ? '1' : '0';
  });

  function validarFecha(valor) {
    if (!valor) return 'La fecha no puede estar vacía.';

    const fechaIngresada = new Date(valor);
    const fechaMinima = new Date('1940-01-01');
    const hoy = new Date();

    let edad = hoy.getFullYear() - fechaIngresada.getFullYear();
    const m = hoy.getMonth() - fechaIngresada.getMonth();
    const d = hoy.getDate() - fechaIngresada.getDate();
    if (m < 0 || (m === 0 && d < 0)) edad--;

    if (fechaIngresada < fechaMinima) {
      return 'La fecha no puede ser menor al 01/01/1940.';
    }

    if (edad < 14) {
      return 'La edad mínima es 14 años.';
    }

    if (edad >= 14 && edad <= 17) {
      if (!confirm(`La fecha ingresada corresponde a un menor de edad (${edad} años). ¿Desea continuar con esta fecha: ${valor}?`)) {
        fechaInput.value = '';
        return 'Ingrese otra fecha.';
      }
    }

    return '';
  }
});