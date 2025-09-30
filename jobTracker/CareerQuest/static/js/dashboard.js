document.addEventListener("DOMContentLoaded", () => {
  function statusIndicator() {
    const status = document.querySelectorAll("[data-value]");

    const colorClassMap = {
      Rejected: "text-danger",
      Pending: "text-warning",
      Accepted: "text-success",
    };

    status.forEach((td) => {
      const value = td.dataset.value;
      const dot = td.querySelector(".statusDot");

      const colorClass = colorClassMap[value] || "text-secondary";

      // Remove any existing Bootstrap text-* color classes first
      dot.classList.remove(
        "text-danger",
        "text-warning",
        "text-success",
        "text-secondary"
      );
      dot.classList.add(colorClass);
    });
  }

  function inputValidation() {

  }

statusIndicator();

// Alert fadeout 
window.setTimeout(function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    });
}, 3000);

});


