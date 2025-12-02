// MAIN.JS
// Handles signup + login and redirects

async function signupUser(event) {
  event.preventDefault();
  const name = document.getElementById("su_name").value.trim();
  const email = document.getElementById("su_email").value.trim();
  const password = document.getElementById("su_password").value.trim();
  const msg = document.getElementById("signupMessage");

  if (!name || !email || !password) {
    msg.style.color = "salmon";
    msg.textContent = "Please fill all fields.";
    return;
  }

  msg.style.color = "#e5e7eb";
  msg.textContent = "Creating your account...";

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
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

  if (!email || !password) {
    msg.style.color = "salmon";
    msg.textContent = "Please enter email and password.";
    return;
  }

  msg.style.color = "#e5e7eb";
  msg.textContent = "Checking your credentials...";

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
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
