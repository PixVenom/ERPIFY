const form = document.getElementById("order-form");
const tableBody = document.getElementById("order-table-body");
const token = localStorage.getItem("token");
const apiURL = "http://localhost:8000/docs"; // API endpoint URL

document.addEventListener("DOMContentLoaded", fetchOrders);

// Handle form submission to add a new order
form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Validate form fields
    if (!form.checkValidity()) {
        alert("Please fill out all fields correctly.");
        return;
    }

    const newOrder = {
        product_id: parseInt(document.getElementById("order-product-id").value),
        customer_id: parseInt(document.getElementById("order-customer-id").value),
        quantity: parseInt(document.getElementById("order-quantity").value),
        order_date: document.getElementById("order-date").value,
        status: document.getElementById("order-status").value
    };

    try {
        const res = await fetch(apiURL + "/", {
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
            alert(`Failed to place order: ${error.message || "Unknown error"}`);
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while placing the order.");
    }
});

// Fetch orders and render them in the table
async function fetchOrders() {
    try {
        const res = await fetch(apiURL + "/", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        if (res.ok) {
            const orders = await res.json();
            renderTable(orders);
        } else {
            alert("Failed to fetch orders.");
        }
    } catch (err) {
        console.error("Error fetching orders:", err);
        alert("An error occurred while fetching orders.");
    }
}

// Render orders in the table
function renderTable(orders) {
    tableBody.innerHTML = "";
    orders.forEach((order) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${order.id}</td>
      <td>${order.product_id}</td>
      <td>${order.customer_id}</td>
      <td>${order.quantity}</td>
      <td>${order.order_date}</td>
      <td>${order.status}</td>
      <td>
        <button class="btn btn-edit" onclick="editOrder(${order.id})">Edit</button>
        <button class="btn btn-delete" onclick="deleteOrder(${order.id})">Delete</button>
      </td>
    `;
        tableBody.appendChild(row);
    });
}

// Delete order
async function deleteOrder(id) {
    const confirmDelete = confirm("Are you sure you want to delete this order?");
    if (!confirmDelete) return;

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
            alert(`Failed to delete order: ${error.message || "Unknown error"}`);
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while deleting the order.");
    }
}

// Edit order
async function editOrder(id) {
    const product_id = prompt("Enter new product ID:");
    const customer_id = prompt("Enter new customer ID:");
    const quantity = prompt("Enter new quantity:");
    const order_date = prompt("Enter new order date (YYYY-MM-DD):");
    const status = prompt("Enter new status:");

    if (!product_id || !customer_id || !quantity || !order_date || !status) {
        alert("Please fill out all fields.");
        return;
    }

    const updatedOrder = {
        product_id: parseInt(product_id),
        customer_id: parseInt(customer_id),
        quantity: parseInt(quantity),
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
            alert(`Failed to update order: ${error.message || "Unknown error"}`);
        }
    } catch (err) {
        console.error(err);
        alert("An error occurred while updating the order.");
    }
}