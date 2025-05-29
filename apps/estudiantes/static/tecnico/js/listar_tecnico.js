document.addEventListener('DOMContentLoaded', () => {
  const table = document.getElementById('estudiantes-table');
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  const filters = {
    nombre: document.getElementById('filter-nombre'),
    ci: document.getElementById('filter-ci'),
    telefono: document.getElementById('filter-telefono'),
    ocupacion: document.getElementById('filter-ocupacion')
  };
  let currentSort = { column: null, direction: 'asc' };

  // Función para filtrar filas según inputs
  function filterRows() {
    const filterValues = {
      nombre: filters.nombre.value.toLowerCase(),
      ci: filters.ci.value.toLowerCase(),
      telefono: filters.telefono.value.toLowerCase(),
      ocupacion: filters.ocupacion.value.toLowerCase()
    };

    rows.forEach(row => {
      const cells = row.querySelectorAll('td');
      // Aquí el nombre es la concatenación nombres + apellidos en la celda 0
      const nombre = cells[0].textContent.toLowerCase();
      const ci = cells[1].textContent.toLowerCase();
      const telefono = cells[2].textContent.toLowerCase();
      const ocupacion = cells[3].textContent.toLowerCase();

      const show =
        nombre.includes(filterValues.nombre) &&
        ci.includes(filterValues.ci) &&
        telefono.includes(filterValues.telefono) &&
        ocupacion.includes(filterValues.ocupacion);

      row.style.display = show ? '' : 'none';
    });
  }

  Object.values(filters).forEach(input => {
    if (input) {
      input.addEventListener('input', filterRows);
    }
  });

  // Mapeo de columna a índice (1-based)
  function columnIndex(column) {
    switch (column) {
      case 'nombre': return 1;
      case 'ci': return 2;
      case 'telefono': return 3;
      case 'ocupacion': return 4;
      default: return 1;
    }
  }

  // Función para ordenar tabla
  function sortTable(column, type = 'string') {
    if (currentSort.column === column) {
      currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
      currentSort.column = column;
      currentSort.direction = 'asc';
    }

    // Quitar clases anteriores
    table.querySelectorAll('th').forEach(th => {
      th.classList.remove('sorted-asc', 'sorted-desc');
    });

    const th = table.querySelector(`th[data-column="${column}"]`);
    if (th) {
      th.classList.add(currentSort.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
    }

    rows.sort((a, b) => {
      const aText = a.querySelector(`td:nth-child(${columnIndex(column)})`).textContent.trim().toLowerCase();
      const bText = b.querySelector(`td:nth-child(${columnIndex(column)})`).textContent.trim().toLowerCase();

      if (type === 'number') {
        // Por si quieres ordenar números, pero mejor manejar como string en ci
        return currentSort.direction === 'asc'
          ? Number(aText) - Number(bText)
          : Number(bText) - Number(aText);
      } else {
        if (aText < bText) return currentSort.direction === 'asc' ? -1 : 1;
        if (aText > bText) return currentSort.direction === 'asc' ? 1 : -1;
        return 0;
      }
    });

    // Reordenar rows en el tbody
    rows.forEach(row => tbody.appendChild(row));
  }

  // Asignar evento click a th que tengan data-column para ordenar
  table.querySelectorAll('th[data-column]').forEach(th => {
    th.addEventListener('click', () => {
      // Mejor dejar todo como string, ya que CI puede tener ceros a la izquierda o letras
      sortTable(th.dataset.column, 'string');
    });
  });
});
