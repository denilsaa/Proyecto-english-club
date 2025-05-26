document.addEventListener("DOMContentLoaded", function () {
  const toggle = document.getElementById('navbar-toggle');
  const menu = document.getElementById('mobile-menu');

  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      menu.classList.toggle('hidden');
    });
  }
});
