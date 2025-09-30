function inputValidation(){

    const loginForm = document.getElementById('authForm');
    const identifier = document.getElementById('usernameOrEmail');
    const passwordField = document.getElementById('password');

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();

        let hasError = false;

        document.getElementById('identifierErr').style.display = "none";
        document.getElementById('passwordErr').style.display = "none";

        if(!identifier.value.trim()){
            document.getElementById('identifierErr').style.display = "block";
            hasError = true;
        }

        if(!passwordField.value.trim()){
            document.getElementById('passwordErr').style.display = "block";
            hasError = true;
        }

        // Clear Error once the user starts typing
        identifier.addEventListener('input', () => {
            document.getElementById('identifierErr').style.display = "none";
        });

        passwordField.addEventListener('input', () => {
            document.getElementById('passwordErr').style.display = "none";
        });

        // If there are no errors, submit the form.
        if(!hasError){
            loginForm.submit()
        }
    })
}


inputValidation();

// Alert fadeout after user creation
window.setTimeout(function() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    });
}, 3000);