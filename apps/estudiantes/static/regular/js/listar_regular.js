document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('tabla-estudiantes');
  const tbody = table.tBodies[0];
  const filas = Array.from(tbody.rows);

  // Filtros por ID
  const filtros = {
    estudiante: document.getElementById('filter-estudiante'),
    ci: document.getElementById('filter-ci'),
    telefono: document.getElementById('filter-telefono'),
    grupo: document.getElementById('filter-grupo'),
    padre: document.getElementById('filter-padre'),
    ciPadre: document.getElementById('filter-ci-padre'),
    telPadre: document.getElementById('filter-tel-padre'),
  };

  let currentSort = { column: null, direction: 'asc' };

  // FILTRO
  function filtrarTabla() {
    const valoresFiltro = {
      estudiante: filtros.estudiante.value.trim().toLowerCase(),
      ci: filtros.ci.value.trim().toLowerCase(),
      telefono: filtros.telefono.value.trim().toLowerCase(),
      grupo: filtros.grupo.value.trim().toLowerCase(),
      padre: filtros.padre.value.trim().toLowerCase(),
      ciPadre: filtros.ciPadre.value.trim().toLowerCase(),
      telPadre: filtros.telPadre.value.trim().toLowerCase(),
    };

    filas.forEach(fila => {
      const textoEstudiante = fila.cells[0].textContent.toLowerCase();
      const textoCI = fila.cells[1].textContent.toLowerCase();
      const textoTelefono = fila.cells[2].textContent.toLowerCase();
      const textoGrupo = fila.cells[3].textContent.toLowerCase();
      const textoPadre = fila.cells[4].textContent.toLowerCase();
      const textoCIPadre = fila.cells[5].textContent.toLowerCase();
      const textoTelPadre = fila.cells[6].textContent.toLowerCase();

      const coincide =
        textoEstudiante.includes(valoresFiltro.estudiante) &&
        textoCI.includes(valoresFiltro.ci) &&
        textoTelefono.includes(valoresFiltro.telefono) &&
        textoGrupo.includes(valoresFiltro.grupo) &&
        textoPadre.includes(valoresFiltro.padre) &&
        textoCIPadre.includes(valoresFiltro.ciPadre) &&
        textoTelPadre.includes(valoresFiltro.telPadre);

      fila.style.display = coincide ? '' : 'none';
    });
  }

  // Escuchar eventos input para filtrar
  Object.values(filtros).forEach(input => {
    if (input) {
      input.addEventListener('input', filtrarTabla);
    }
  });

  // ORDENAMIENTO
  function sortTable(columnIndex) {
    if (currentSort.column === columnIndex) {
      currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
      currentSort.column = columnIndex;
      currentSort.direction = 'asc';
    }

    table.querySelectorAll('th').forEach(th => {
      th.classList.remove('sorted-asc', 'sorted-desc');
    });

    const th = table.querySelector(`th[data-column="${columnIndex}"]`);
    if (th) {
      th.classList.add(currentSort.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
    }

    filas.sort((a, b) => {
      const aText = a.cells[columnIndex].textContent.trim().toLowerCase();
      const bText = b.cells[columnIndex].textContent.trim().toLowerCase();

      if (!isNaN(aText) && !isNaN(bText)) {
        return currentSort.direction === 'asc'
          ? Number(aText) - Number(bText)
          : Number(bText) - Number(aText);
      }

      if (aText < bText) return currentSort.direction === 'asc' ? -1 : 1;
      if (aText > bText) return currentSort.direction === 'asc' ? 1 : -1;
      return 0;
    });

    filas.forEach(fila => tbody.appendChild(fila));
  }

  // Agregar evento a los headers
  table.querySelectorAll('th[data-column]').forEach((th, index) => {
    th.addEventListener('click', () => {
      sortTable(index);
    });
  });
});
