// ========== SIGNUP ==========
function signupUser(event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "exists") {
            alert("⚠ Email already registered!");
        } 
        else if (data.status === "success") {
            alert("🎉 Signup Successful! Login now.");
            window.location.href = "/login";
        }
    })
    .catch(err => console.log("Signup Error:", err));
}


// ========== LOGIN ==========
function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            window.location.href = "/dashboard";
        } 
        else {
            alert("❌ Invalid email or password");
        }
    })
    .catch(err => console.log("Login Error:", err));
}
