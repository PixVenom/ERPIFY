const token = localStorage.getItem("token");

if (!token) {
    window.location.href = "/frontend/index.html"; // Redirect if not logged in
} else {
    const username = localStorage.getItem("username") || "User";
    document.getElementById("username").innerText = username;
}

// Logout functionality
document.getElementById("logoutBtn").addEventListener("click", function () {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    window.location.href = "/frontend/index.html"; // Redirect to login after logout
});

// List of dashboard modules
const modules = [
    { name: 'Products', path: 'products' },
    { name: 'Customers', path: 'customers' },
    { name: 'Orders', path: 'orders' },
    { name: 'Projects', path: 'projects' },
    { name: 'Clients', path: 'clients' },
    { name: 'Employees', path: 'employees' },
    { name: 'Tasks', path: 'tasks' },
    { name: 'Timesheets', path: 'timesheets' },
    { name: 'Invoices', path: 'invoices' },
    { name: 'Payments', path: 'payments' },
    { name: 'Support Tickets', path: 'support-tickets' },
    { name: 'Assets', path: 'assets' },
    { name: 'Recruitment', path: 'recruitment' },
    { name: 'Leave Management', path: 'leave-management' },
    { name: 'Attendance', path: 'attendance' },
    { name: 'Reports', path: 'reports' },
    { name: 'Settings', path: 'settings' }
];

// Dynamically create dashboard cards
document.addEventListener('DOMContentLoaded', function () {
    const cardsContainer = document.getElementById('cardsContainer');

    modules.forEach(module => {
        const card = document.createElement('div');
        card.className = 'card';
        card.onclick = () => navigateTo(module.path);

        const h2 = document.createElement('h2');
        h2.textContent = module.name;

        card.appendChild(h2);
        cardsContainer.appendChild(card);
    });
});

// Dynamic navigation with error handling
function navigateTo(section) {
    const url = `/frontend/${section}.html`;

    fetch(url, { method: 'HEAD' })
        .then(response => {
            if (response.ok) {
                window.location.href = url;
            } else {
                alert(`The page for "${section}" is not ready yet.`);
            }
        })
        .catch(error => {
            console.error('Navigation error:', error);
            alert(`Unable to navigate to "${section}".`);
        });
}