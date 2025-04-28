console.log("auth.js loaded");

// Ensure the form submission triggers login
document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();  // Prevent actual form submission
    console.log("login() called");
    login();
});

async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (res.ok) {
            const data = await res.json();
            console.log("Login successful, token:", data.access_token);
            console.log("Role:", data.role);

            // Save the token and role in localStorage
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("role", data.role);

            // Redirect with a slight delay
            setTimeout(() => {
                if (data.role === "admin") {
                    console.log("Redirecting to admin dashboard");
                    window.location.href = "/frontend/dashboard.html";  // Redirect to admin dashboard
                } else {
                    console.log("Redirecting to user dashboard");
                    window.location.href = "/frontend/dashboard.html";  // Redirect to user dashboard
                }
            }, 500);  // Delay to ensure login processing completes
        } else {
            const errorData = await res.json();
            console.log("Error data:", errorData);
            document.getElementById("error").innerText = errorData.detail || "Invalid credentials";
        }
    } catch (err) {
        console.error("Login error:", err);
        document.getElementById("error").innerText = "Something went wrong. Try again.";
    }
}
