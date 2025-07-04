const form = document.getElementById("order-form");
const tableBody = document.getElementById("order-table-body");
const token = localStorage.getItem("token");
const apiURL = "http://localhost:8000/orders";

// Fetch orders on page load
document.addEventListener("DOMContentLoaded", () => {
    if (!token) {
        alert("No token found. Please log in first.");
        return;
    }
    fetchOrders();
});

// Handle form submission to add a new order
form.addEventListener("submit", async function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
        alert("Please fill out all fields correctly.");
        return;
    }

    const newOrder = {
        customer_id: parseInt(document.getElementById("customer_id").value),
        order_date: document.getElementById("order_date").value,
        status: document.getElementById("status").value
    };

    try {
        const res = await fetch(apiURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(newOrder)
        });

        if (res.ok) {
            fetchOrders();
            form.reset();
        } else {
            const error = await res.json();
            alert(`Failed to place order: ${error.detail || "Unknown error"}`);
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while placing the order.");
    }
});

// Fetch orders
async function fetchOrders() {
    try {
        const res = await fetch(apiURL, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });
        if (res.ok) {
            const orders = await res.json();
            renderTable(orders);
        } else if (res.status === 403) {
            alert("403 Forbidden: You do not have permission to access orders.");
        } else {
            alert("Failed to fetch orders.");
        }
    } catch (err) {
        console.error("Error fetching orders:", err);
        alert("An error occurred while fetching orders.");
    }
}

// Render orders in table
function renderTable(orders) {
    tableBody.innerHTML = "";
    orders.forEach((order) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${order.order_id}</td>
            <td>${order.customer_id}</td>
            <td>${order.order_date}</td>
            <td>${order.status}</td>
            <td>
                <button class="btn btn-edit" onclick="editOrder(${order.order_id})">Edit</button>
                <button class="btn btn-delete" onclick="deleteOrder(${order.order_id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Delete order
async function deleteOrder(id) {
    if (!confirm("Are you sure you want to delete this order?")) return;

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        if (res.ok) {
            fetchOrders();
        } else {
            const error = await res.json();
            alert(`Failed to delete order: ${error.detail || "Unknown error"}`);
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while deleting the order.");
    }
}

// Edit order
async function editOrder(id) {
    const customer_id = prompt("Enter new customer ID:");
    const order_date = prompt("Enter new order date (YYYY-MM-DD):");
    const status = prompt("Enter new status:");

    if (!customer_id || !order_date || !status) {
        alert("All fields are required.");
        return;
    }

    const updatedOrder = {
        customer_id: parseInt(customer_id),
        order_date,
        status
    };

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(updatedOrder)
        });

        if (res.ok) {
            fetchOrders();
        } else {
            const error = await res.json();
            alert(`Failed to update order: ${error.detail || "Unknown error"}`);
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while updating the order.");
    }
}
