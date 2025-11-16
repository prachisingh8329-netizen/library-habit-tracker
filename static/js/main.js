// Signup form
async function signupUser(e) {
  e && e.preventDefault();
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const res = await fetch("/api/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  });
  const j = await res.json();
  if (!res.ok) {
    alert(j.message || "Signup failed");
    return;
  }
  alert("Signup successful — please login");
  window.location.href = "/login";
}

// Login form
async function login(e) {
  e && e.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });
  const j = await res.json();
  if (!res.ok) {
    alert(j.message || "Login failed");
    return;
  }
  // on success, go to dashboard
  window.location.href = "/dashboard";
}
