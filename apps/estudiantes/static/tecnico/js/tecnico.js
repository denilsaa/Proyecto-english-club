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

  // Crear div para errores y añadirlo
  const errorDiv = document.createElement('div');
  errorDiv.style.color = 'red';
  errorDiv.style.marginTop = '5px';
  fechaInput.parentNode.appendChild(errorDiv);

  // Modal y botones del modal ya están en el HTML
  const modal = document.getElementById('modalConfirmacion');
  const modalMensaje = document.getElementById('modalMensaje');
  const btnAceptar = document.getElementById('btnAceptar');
  const btnCancelar = document.getElementById('btnCancelar');

  // Estado para saber si menor confirmado
  let menorConfirmado = false;

  function calcularEdad(fecha) {
    const hoy = new Date();
    let edad = hoy.getFullYear() - fecha.getFullYear();
    const mes = hoy.getMonth() - fecha.getMonth();
    const dia = hoy.getDate() - fecha.getDate();
    if (mes < 0 || (mes === 0 && dia < 0)) edad--;
    return edad;
  }

  function validarFecha() {
    const valor = fechaInput.value.trim();

    if (!valor) {
      errorDiv.textContent = 'La fecha de nacimiento es obligatoria.';
      fechaInput.classList.add('border-red-500');
      menorConfirmado = false;
      return false;
    }

    const fechaVal = new Date(valor);
    if (isNaN(fechaVal.getTime())) {
      errorDiv.textContent = 'Fecha inválida.';
      fechaInput.classList.add('border-red-500');
      menorConfirmado = false;
      return false;
    }

    const edad = calcularEdad(fechaVal);

    if (edad < 14) {
      errorDiv.textContent = 'Debes tener al menos 14 años para registrarte.';
      fechaInput.classList.add('border-red-500');
      menorConfirmado = false;
      return false;
    }

    if (edad > 85) {
      errorDiv.textContent = 'La edad máxima permitida es 85 años.';
      fechaInput.classList.add('border-red-500');
      menorConfirmado = false;
      return false;
    }

    // Si está entre 14 y 17 y no ha confirmado aún
    if (edad >= 14 && edad <= 17 && !menorConfirmado) {
      errorDiv.textContent = '';
      fechaInput.classList.remove('border-red-500');

      // Mostrar modal con mensaje y esperar respuesta
      modalMensaje.textContent = `La persona es menor de edad (tiene ${edad} años, nacido el ${valor}). ¿Deseas continuar con esta fecha?`;
      modal.classList.remove('hidden');
      fechaInput.blur();

      return null; // Validación pendiente de confirmación
    }

    // Si pasa todas las validaciones
    errorDiv.textContent = '';
    fechaInput.classList.remove('border-red-500');
    menorConfirmado = false;
    return true;
  }

  // Evento input para validar en tiempo real
  fechaInput.addEventListener('input', function () {
    menorConfirmado = false; // reset al cambiar fecha
    validarFecha();
  });

  // Botones del modal
  btnAceptar.addEventListener('click', function () {
    menorConfirmado = true;
    modal.classList.add('hidden');
    errorDiv.textContent = '';
    fechaInput.classList.remove('border-red-500');
    fechaInput.focus();
  });

  btnCancelar.addEventListener('click', function () {
    modal.classList.add('hidden');
    fechaInput.value = '';
    menorConfirmado = false;
    errorDiv.textContent = 'Por favor ingresa una nueva fecha.';
    fechaInput.classList.add('border-red-500');
    fechaInput.focus();
  });

  // Opcional: evitar submit si validación falla
  const form = document.getElementById('form-registro');
  form.addEventListener('submit', function (e) {
    const valido = validarFecha();
    if (valido === false || valido === null) {
      e.preventDefault();
      if (valido === null) {
        // si es null, está pendiente confirmación, ya mostramos modal
      } else {
        fechaInput.focus();
      }
    }
  });
});

mapboxgl.accessToken = 'pk.eyJ1IjoiYWlseW5lbmNpbmFzIiwiYSI6ImNsdXN6OXltZjAzNHMyam9nNHR2bGk3dmgifQ.a1eP122SNX_g_e2EbskphA';

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-68.1193, -16.4897], // Coordenadas iniciales (ej. La Paz)
  zoom: 12
});

const geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  types: 'address',
  placeholder: 'Ingresa tu dirección',
  mapboxgl: mapboxgl,
  marker: false
});

document.getElementById('geocoder').appendChild(geocoder.onAdd(map));

let marker = null;

// Crear un div para mostrar errores (puedes ponerlo en el HTML o crearlo aquí)
const errorDiv = document.createElement('div');
errorDiv.style.color = 'red';
errorDiv.style.marginTop = '5px';
document.getElementById('geocoder').appendChild(errorDiv);

// Declarar el formulario
const form = document.getElementById('form-registro');

geocoder.on('result', (e) => {
  const coords = e.result.center;
  // Guardar coordenadas ocultas para el formulario
  document.getElementById('lat').value = coords[1];
  document.getElementById('lng').value = coords[0];

  // Mover marcador al punto seleccionado o crear uno nuevo
  if (marker) {
    marker.setLngLat(coords);
  } else {
    marker = new mapboxgl.Marker().setLngLat(coords).addTo(map);
  }

  // Centrar mapa en la ubicación seleccionada
  map.flyTo({ center: coords, zoom: 15 });

  // Limpiar mensaje de error si existía
  errorDiv.textContent = '';
});

// Validación al enviar formulario
form.addEventListener('submit', (e) => {
  const lat = document.getElementById('lat').value;
  const lng = document.getElementById('lng').value;

  if (!lat || !lng) {
    e.preventDefault();
    errorDiv.textContent = 'Por favor selecciona una dirección válida de la lista.';
  }
});
