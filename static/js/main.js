// ============== SIGNUP ==============
async function signupUser(event) {
  event.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!name || !email || !password) {
    alert("Please fill all fields");
    return;
  }

  try {
    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();
    alert(data.message);

    if (data.success) {
      window.location.href = "/login";
    }
  } catch (err) {
    console.error("Signup error:", err);
    alert("Signup failed. Try again.");
  }
}

// backup name, agar kahin onsubmit="signup(event)" likha ho
async function signup(event) {
  return signupUser(event);
}

// ============== LOGIN ==============
async function loginUser(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Enter email and password");
    return;
  }

  try {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (data.success) {
      window.location.href = "/dashboard";
    } else {
      alert(data.message || "Login failed");
    }
  } catch (err) {
    console.error("Login error:", err);
    alert("Something went wrong.");
  }
}

// backup name, agar kahin onsubmit="login(event)" likha ho
async function login(event) {
  return loginUser(event);
}
