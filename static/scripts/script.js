const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const emailInput = document.getElementById('email-input');
const emailError = document.getElementById('email-error');
const successMessage = document.getElementById('success-message');
const signUpButton = document.getElementById('signup-button');
// document.addEventListener("DOMContentLoaded", function() {

//   signUpButton.addEventListener('click', function(e) {
//     e.preventDefault();
//     successMessage.style.display = 'block'; // Display the message
//     setTimeout(function() {
//       successMessage.style.display = 'none'; // Hide the message after 3 seconds
//     }, 3000);
//   });
// });
const showPasswordButton = document.getElementById("show-password-button");
const showPasswordButtonSignUp = document.getElementById("show-password-buttonSignup");

const passwordInputSignIn = document.getElementById("password-input");
const passwordInputSignUp = document.getElementById("password-inputSignup");


showPasswordButton.addEventListener("click", () => {
  if (passwordInputSignIn.type === "password") {
    passwordInputSignIn.type = "text";
  } else {
    passwordInputSignIn.type = "password";
  }

});

showPasswordButtonSignUp.addEventListener("click", () => {
  if (passwordInputSignUp.type === "password") {
    passwordInputSignUp.type = "text";
  } else {
    passwordInputSignUp.type = "password";
  }
});
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});


document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('signup-form');
  const formSignIn = document.getElementById('sign-in-form');


  const emailInput = document.getElementById('email-input');
  const usernameInput = document.getElementsByName('username-sign-up')[0];
  const usernameInputSignIn = document.getElementsByName('username-sign-in')[0];

  const passwordInput = document.getElementsByName('password-sign-up')[0];
  const passwordInputSignIn = document.getElementsByName('password-sign-in')[0];


  const emailError = document.getElementById('email-error');
  const usernameError = document.getElementById('username-error');
  const passwordError = document.getElementById('password-error');
  const passwordErrorSignIn = document.getElementById('password-error-signIn');

  const usernameSignInError = document.getElementById('username-error-sign-in');

  const usernameErrorExist = document.getElementById('username-error-exist');
  const emailErrorExist = document.getElementById('email-error-exist');

  const successMessage = document.getElementById('success-message');
  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    let hasError = false;

    // Clear previous error messages
    emailError.style.display = 'none';
    usernameError.style.display = 'none';
    passwordError.style.display = 'none';
    emailErrorExist.style.display = 'none';
    usernameErrorExist.style.display = 'none';

    // Check for empty email
    if (emailInput.value.trim() === '') {
      emailError.style.display = 'block';
      hasError = true;
      console.log("Empty email");
      console.log(emailInput);

    }

    // Check for empty username
    if (usernameInput.value.trim() === '') {
      usernameError.style.display = 'block';
      hasError = true;
      console.log("Empty username");
      console.log(usernameInput);
    }
    // Check for invalid email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(emailInput.value)) {
      emailError.style.display = 'block';
      hasError = true;
      console.log("invalid email format");
    }

    // Check password strength
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    if (!passwordPattern.test(passwordInput.value)) {
      passwordError.style.display = 'block';
      hasError = true;
      console.log("invalid passwords format");
    }

    if (hasError) {
      event.preventDefault(); // Prevent form submission
    }



    const response = await fetch('/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: usernameInput.value,
        email: emailInput.value,
      }),
    });

    const data = await response.json();
    console.log(data)
    if (data.usernameExists) {
      usernameErrorExist.style.display = 'block';
      console.log("User name exists");
    }

    if (data.emailExists) {
      emailErrorExist.style.display = 'block';
      console.log(" email exists");
    }
    // Continue with form submission if no errors
    if (!data.usernameExists && !data.emailExists && passwordError.style.display !== 'block') {
      form.submit();
      successMessage.style.display = 'block'; // Display the message
      setTimeout(function () {
        console.log("Wait 3 seconds");
        successMessage.style.display = 'none'; // Hide the message after 3 seconds
      }, 3000);
      console.log("Submit no error");
    }
  });

  formSignIn.addEventListener('submit', async function (event) {
    event.preventDefault();
    let hasErrorSignIn = false;
    usernameSignInError.style.display = 'none';
    passwordErrorSignIn.style.display = 'none';

    // Check for empty username
    if (usernameInputSignIn.value.trim() === '') {
      usernameSignInError.style.display = 'block';
      hasErrorSignIn = true;
      console.log("Empty username from Sign In");
    }


    if (passwordInputSignIn.value.trim() == '') {
      passwordErrorSignIn.style.display = 'block';
      hasErrorSignIn = true;
      console.log("invalid passwords format");
    }
    if (hasErrorSignIn) {
      event.preventDefault(); // Prevent form submission
    }
    if (!hasErrorSignIn) {
      // Continue with form submission if no errors
      formSignIn.submit();
      console.log("sent from Sign In")
    }
  });

});

