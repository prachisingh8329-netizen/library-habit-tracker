// SIGNUP
async function signupUser(event) {
  event.preventDefault();

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/api/signup", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name, email, password})
  });

  const data = await res.json();
  alert(data.message);

  if (data.success) window.location = "/login";
}

// LOGIN
async function loginUser(event) {
  event.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/api/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email, password})
  });

  const data = await res.json();

  if (data.success) {
    window.location = "/dashboard";
  } else {
    alert(data.message);
  }
}
