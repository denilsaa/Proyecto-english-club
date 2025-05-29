document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('personal-table');
  const tbody = table.tBodies[0];
  const filas = Array.from(tbody.rows);

  // Inputs de filtros según tu HTML
  const filtros = {
    nombre: document.getElementById('filter-nombre'),
    ci: document.getElementById('filter-ci'),
    rol: document.getElementById('filter-rol'),
    telefono: document.getElementById('filter-telefono'),
  };

  let currentSort = { column: null, direction: 'asc' };

  // Función para filtrar tabla
  function filtrarTabla() {
    const valoresFiltro = {
      nombre: filtros.nombre.value.trim().toLowerCase(),
      ci: filtros.ci.value.trim().toLowerCase(),
      rol: filtros.rol.value.trim().toLowerCase(),
      telefono: filtros.telefono.value.trim().toLowerCase(),
    };

    filas.forEach(fila => {
      const textoNombre = fila.cells[0].textContent.toLowerCase();
      const textoCI = fila.cells[1].textContent.toLowerCase();
      const textoRol = fila.cells[2].textContent.toLowerCase();
      const textoTelefono = fila.cells[3].textContent.toLowerCase();

      const coincide =
        textoNombre.includes(valoresFiltro.nombre) &&
        textoCI.includes(valoresFiltro.ci) &&
        textoRol.includes(valoresFiltro.rol) &&
        textoTelefono.includes(valoresFiltro.telefono);

      fila.style.display = coincide ? '' : 'none';
    });
  }

  // Escuchar inputs para filtrar
  Object.values(filtros).forEach(input => {
    if (input) {
      input.addEventListener('input', filtrarTabla);
    }
  });

  // Función para ordenar tabla
  function sortTable(columnIndex) {
    if (currentSort.column === columnIndex) {
      currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
      currentSort.column = columnIndex;
      currentSort.direction = 'asc';
    }

    // Limpiar clases de sorting en headers
    table.querySelectorAll('th[data-column]').forEach(th => {
      th.classList.remove('sorted-asc', 'sorted-desc');
    });

    // Añadir clase a la columna ordenada
    const th = table.querySelector(`th[data-column="${columnIndex}"]`);
    if (th) {
      th.classList.add(currentSort.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
    }

    filas.sort((a, b) => {
      const aText = a.cells[columnIndex].textContent.trim().toLowerCase();
      const bText = b.cells[columnIndex].textContent.trim().toLowerCase();

      // Comparar numérico si ambos son números
      if (!isNaN(aText) && !isNaN(bText)) {
        return currentSort.direction === 'asc'
          ? Number(aText) - Number(bText)
          : Number(bText) - Number(aText);
      }

      // Comparar texto
      if (aText < bText) return currentSort.direction === 'asc' ? -1 : 1;
      if (aText > bText) return currentSort.direction === 'asc' ? 1 : -1;
      return 0;
    });

    // Añadir filas ordenadas al tbody
    filas.forEach(fila => tbody.appendChild(fila));
  }

  // Añadir evento click para ordenar a los th que tienen data-column
  table.querySelectorAll('th[data-column]').forEach(th => {
    th.addEventListener('click', () => {
      const columnIndex = Number(th.getAttribute('data-column'));
      sortTable(columnIndex);
    });
  });
});
