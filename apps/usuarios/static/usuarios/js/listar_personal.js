document.addEventListener("DOMContentLoaded", () => {
  console.log("Script JS cargado correctamente");

  const table = document.getElementById("personal-table");
  const tbody = table.querySelector("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));
  const inputs = {
    nombre: document.getElementById("filter-nombre"),
    ci: document.getElementById("filter-ci"),
    rol: document.getElementById("filter-rol"),
    telefono: document.getElementById("filter-telefono"),
  };

  let sortDirection = {}; // Guardar el estado de orden por columna

  function applyFilters() {
    console.log("Filtrando tabla...");

    const nombreVal = inputs.nombre.value.toLowerCase();
    const ciVal = inputs.ci.value.toLowerCase();
    const rolVal = inputs.rol.value.toLowerCase();
    const telVal = inputs.telefono.value.toLowerCase();

    rows.forEach(row => {
      const cells = row.querySelectorAll("td");
      const nombre = cells[0]?.textContent.toLowerCase() || "";
      const ci = cells[1]?.textContent.toLowerCase() || "";
      const rol = cells[2]?.textContent.toLowerCase() || "";
      const tel = cells[3]?.textContent.toLowerCase() || "";

      const matches =
        nombre.includes(nombreVal) &&
        ci.includes(ciVal) &&
        rol.includes(rolVal) &&
        tel.includes(telVal);

      row.style.display = matches ? "" : "none";
    });
  }

  Object.values(inputs).forEach(input =>
    input.addEventListener("input", applyFilters)
  );

  function sortTableByColumn(columnIndex) {
    const ascending = !sortDirection[columnIndex];
    sortDirection[columnIndex] = ascending;

    const sortedRows = [...rows].sort((a, b) => {
      const aText = a.cells[columnIndex].textContent.trim().toLowerCase();
      const bText = b.cells[columnIndex].textContent.trim().toLowerCase();

      return ascending
        ? aText.localeCompare(bText, 'es')
        : bText.localeCompare(aText, 'es');
    });

    while (tbody.firstChild) {
      tbody.removeChild(tbody.firstChild);
    }

    sortedRows.forEach(row => tbody.appendChild(row));
  }

  table.querySelectorAll("th[data-column]").forEach(th => {
    th.addEventListener("click", () => {
      const columnIndex = parseInt(th.getAttribute("data-column"));
      sortTableByColumn(columnIndex);
    });
  });
});
