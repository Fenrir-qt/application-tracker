function inputValidation(){
    const regForm = document.getElementById('regForm')
    const usernameField = document.getElementById('username');
    const emailField = document.getElementById('email');
    const password1Field = document.getElementById('password1');
    const password2Field = document.getElementById('password2');

    regForm.addEventListener('submit', (e) => {
        e.preventDefault();

        let hasErrors = false;

        document.getElementById("userErr").style.display = "none";
        document.getElementById("emailErr").style.display = "none";
        document.getElementById("password1Err").style.display = "none";
        document.getElementById("password2Err").style.display = "none";

        
        if (!usernameField.value.trim()) {
            document.getElementById("userErr").style.display = "block";
            hasErrors = true;
        }

        if (!emailField.value.trim()) {
            document.getElementById("emailErr").style.display = "block";
            hasErrors = true;
        }

        if (!password1Field.value.trim()) {
            document.getElementById("password1Err").style.display = "block";
            hasErrors = true;
        }

        if (!password2Field.value.trim()) {
            document.getElementById("password2Err").style.display = "block";
            hasErrors = true;
        }

        // Check if passwords match
        if (password1Field.value !== password2Field.value && password1Field.value && password2Field.value) {
            document.getElementById("password2Err").textContent = "Passwords don't match!";
            document.getElementById("password2Err").style.display = "block";
            hasErrors = true;
        }

        // If no errors, submit the form
        if (!hasErrors) {
            regForm.submit();
        } 
        
    })
}

inputValidation()