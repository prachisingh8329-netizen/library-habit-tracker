// MAIN.JS
// Signup + Login with extra validation rules

// Common email regex: must be something@something.com with nothing after .com
const emailRegex = /^[^\s@]+@[^\s@]+\.com$/;

// Name: only letters (A–Z, a–z), max 15 characters, no digits, no spaces
const nameRegex = /^[A-Za-z]{1,15}$/;

async function signupUser(event) {
  event.preventDefault();
  const name = document.getElementById("su_name").value.trim();
  const email = document.getElementById("su_email").value.trim();
  const password = document.getElementById("su_password").value.trim();
  const msg = document.getElementById("signupMessage");

  // ---- NAME RULES ----
  if (!nameRegex.test(name)) {
    msg.style.color = "salmon";
    msg.textContent =
      "Name must contain only letters (A–Z), no numbers, and max 15 characters.";
    return;
  }

  // ---- EMAIL RULES ----
  if (!emailRegex.test(email)) {
    msg.style.color = "salmon";
    msg.textContent =
      "Enter a valid email that ends exactly with .com (nothing after .com).";
    return;
  }

  if (!password) {
    msg.style.color = "salmon";
    msg.textContent = "Please enter a password.";
    return;
  }

  msg.style.color = "#e5e7eb";
  msg.textContent = "Creating your account...";

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();

    if (!data.success) {
      msg.style.color = "salmon";
      msg.textContent = data.message || "Sign up failed.";
      return;
    }

    msg.style.color = "#4ade80";
    msg.textContent = "Signup successful! Redirecting to login...";
    setTimeout(() => {
      window.location.href = "/login";
    }, 1200);

  } catch (err) {
    console.error(err);
    msg.style.color = "salmon";
    msg.textContent = "Server error. Please try again.";
  }
}

async function loginUser(event) {
  event.preventDefault();
  const email = document.getElementById("li_email").value.trim();
  const password = document.getElementById("li_password").value.trim();
  const msg = document.getElementById("loginMessage");

  // ---- EMAIL RULES (LOGIN ME BHI SAME) ----
  if (!emailRegex.test(email)) {
    msg.style.color = "salmon";
    msg.textContent =
      "Enter a valid email that ends exactly with .com (nothing after .com).";
    return;
  }

  if (!password) {
    msg.style.color = "salmon";
    msg.textContent = "Please enter your password.";
    return;
  }

  msg.style.color = "#e5e7eb";
  msg.textContent = "Checking your credentials...";

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!data.success) {
      msg.style.color = "salmon";
      msg.textContent = data.message || "Login failed.";
      return;
    }

    msg.style.color = "#4ade80";
    msg.textContent = "Login successful! Opening dashboard...";

    const redirectUrl = data.redirect || "/dashboard";
    setTimeout(() => {
      window.location.href = redirectUrl;
    }, 900);

  } catch (err) {
    console.error(err);
    msg.style.color = "salmon";
    msg.textContent = "Server error. Please try again.";
  }
}
