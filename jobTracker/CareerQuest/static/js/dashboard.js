document.addEventListener("DOMContentLoaded", () => {
  function statusIndicator() {
    const status = document.querySelectorAll("[data-value]");

    const colorClassMap = {
      Rejected: "text-danger",
      Pending: "text-warning",
      Offered: "text-info",
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


//Search Function AJAX

function searchApplication(){

const searchInput = document.getElementById('search-application');

let debounceTimer;
searchInput.addEventListener('keyup', function() {
    clearTimeout(debounceTimer);
    const query = this.value;
    debounceTimer = setTimeout(() => {

    fetch(`/search-application/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            // Update Desktop Table
            const tbody = document.querySelector('table tbody');
            tbody.innerHTML = '';

            if (data.results.length > 0) {
                data.results.forEach(job => {
                    let tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td id="companyCell"><span><p>&nbsp;</p>${ job.company }</span></td>
                        <td id="jobCell"><span><p>&nbsp;</p>${ job.job_name }</span></td>
                        <td id="descCell"><span><p>&nbsp;</p>${ job.job_desc }</span></td>
                        <td data-value="${job.status}" id="statusCell"><span><i class="bi bi-dot statusDot"></i>${ job.status }</span></td>
                        <td id="dateCell"><span><p>&nbsp;</p>${ job.application_date }</span></td>
                    `;
                    tbody.appendChild(tr);
                });
            } else {
                tbody.innerHTML = `<tr><td colspan="5"><h5>No records found.</h5></td></tr>`;
            }

            // Update Mobile Cards
            const mobileContainer = document.querySelectorAll('.card-container, #noRecordMobile');
            mobileContainer.forEach(el => el.remove());

            const parent = document.querySelector('.table-container').parentNode;

            if (data.results.length > 0) {
                data.results.forEach(job => {
                    let card = document.createElement('div');
                    card.className = 'card-container';
                    card.innerHTML = `
                        <div class="card">
                            <div class="card-body">
                                <div class="card-head">
                                    <p class="card-title mobileHeading">${job.job_name}</p>
                                    <div class="button-group mobileBtnGrp">
                                        <button class="editBtn btn btn-warning text-white" data-bs-toggle="modal" data-bs-target="#editApplicationModal${job.id}">Edit</button>
                                        <button class="deleteBtn btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal${job.id}">Delete</button>
                                    </div>
                                </div>
                                <span>Company: ${job.company}</span>
                                <span>Description: ${job.job_desc}</span>
                                <span data-value="${job.status}" id="mobileStatusCell">Status: ${job.status}<i class="bi bi-dot statusDot"></i></span>
                                <span>Date Applied: ${job.application_date}</span>
                            </div>
                        </div>
                    `;
                    parent.appendChild(card);
                });
            } else {
                let noRecord = document.createElement('div');
                noRecord.className = 'card mb-3';
                noRecord.id = 'noRecordMobile';
                noRecord.innerHTML = `
                    <div class="card-body">
                        <h5 class="text-center">No records found</h5>
                    </div>
                `;
                parent.appendChild(noRecord);
            }
            statusIndicator();
        });
    }, 300);
});
}
searchApplication();
});

