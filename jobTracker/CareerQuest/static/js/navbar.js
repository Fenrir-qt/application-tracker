(function () {
  document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.menuBtn');
    const nav = document.getElementById('mobile-menu');
    if (!toggleBtn || !nav) return;

    function closeMenu() {
      nav.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    }

    toggleBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      const isOpen = nav.classList.toggle('open');
      toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close on link click 
    nav.addEventListener('click', function (e) {
      if (e.target && e.target.tagName === 'A') {
        closeMenu();
      }
    });

    // Click outside to close
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && !toggleBtn.contains(e.target)) {
        closeMenu();
      }
    });

    // On resize to desktop, ensure menu is reset
    window.addEventListener('resize', function () {
      if (window.innerWidth > 768) {
        closeMenu();
      }
    });
  });
})();
