// SIGNUP
async function signupUser(event) {
  event.preventDefault();

  const name     = document.getElementById("name").value.trim();
  const email    = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();
    alert(data.message);

    if (data.ok) {
      // signup success → login page
      window.location.href = "/login";
    }
  } catch (err) {
    console.error(err);
    alert("Signup error, please try again.");
  }
}

// LOGIN
async function login(event) {
  event.preventDefault();

  const email    = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    alert(data.message);

    if (data.ok) {
      // login success → dashboard
      window.location.href = "/dashboard";
    }
  } catch (err) {
    console.error(err);
    alert("Login error, please try again.");
  }
}
