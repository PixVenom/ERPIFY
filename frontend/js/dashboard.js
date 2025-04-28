const token = localStorage.getItem("token");

if (!token) {
    // If no token is found, redirect to login page
    window.location.href = "/frontend/index.html";
} else {
    // Optionally, you can also get the role if necessary for user-specific features
    const username = localStorage.getItem("username") || "User";  // or fetch username from token
    document.getElementById("username").innerText = username;
}

// Logout functionality
document.getElementById("logoutBtn").addEventListener("click", function () {
    // Clear localStorage on logout
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "/frontend/index.html";  // Redirect to login page after logout
});

// Navigation function for different sections
function navigateTo(section) {
    switch (section) {
        case 'products':
            window.location.href = '/frontend/products.html';
            break;
        case 'customers':
            window.location.href = '/frontend/customers.html';
            break;
        case 'orders':
            window.location.href = '/frontend/orders.html';
            break;
        default:
            break;
    }
}
