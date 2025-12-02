// =========================
//  SIGN UP FUNCTION
// =========================
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

  } catch (error) {
    console.error("Signup error:", error);
    alert("Signup failed. Try again.");
  }
}

// =========================
//  LOGIN FUNCTION
// =========================
async function loginUser(event) {
  event.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
    alert("Fill email and password");
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
      alert(data.message);
    }

  } catch (error) {
    console.error("Login error:", error);
    alert("Something went wrong");
  }
}
