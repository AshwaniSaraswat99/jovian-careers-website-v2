let currentCaptcha = "";  // Stores the generated captcha text

function togglePassword() {
  const passwordField = document.getElementById("password");
  const type = passwordField.getAttribute("type") === "password" ? "text" : "password";
  passwordField.setAttribute("type", type);
}

function generateCaptcha() {
  const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let captcha = "";
  for (let i = 0; i < 6; i++) {
    captcha += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  currentCaptcha = captcha;  // Save for validation
  document.getElementById("cap").innerText = captcha; // for testing
}

function refresh() {
  generateCaptcha();  // Refresh triggers new captcha
}

function validateCaptcha() {
  const userInput = document.getElementById("captcha").value;
  if (userInput === currentCaptcha) {
    alert("valid captcha!");
  } else {
    alert("Invalid captcha. Please try again.");
  }
}