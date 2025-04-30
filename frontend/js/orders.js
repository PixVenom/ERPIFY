const form = document.getElementById("order-form");
const tableBody = document.getElementById("order-table-body");
const token = localStorage.getItem("token");
const apiURL = "http://localhost:8000/docs";

document.addEventListener("DOMContentLoaded", fetchOrders);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

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
            alert("Failed to place order.");
        }
    } catch (err) {
        console.error(err);
    }
});

async function fetchOrders() {
    try {
        const res = await fetch(apiURL + "/", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        const orders = await res.json();
        renderTable(orders);
    } catch (err) {
        console.error("Error fetching orders:", err);
    }
}

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

async function deleteOrder(id) {
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
            alert("Failed to delete order.");
        }
    } catch (err) {
        console.error(err);
    }
}

async function editOrder(id) {
    const product_id = prompt("Enter new product ID:");
    const customer_id = prompt("Enter new customer ID:");
    const quantity = prompt("Enter new quantity:");
    const order_date = prompt("Enter new order date (YYYY-MM-DD):");
    const status = prompt("Enter new status:");

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
            alert("Failed to update order.");
        }
    } catch (err) {
        console.error(err);
    }
}
