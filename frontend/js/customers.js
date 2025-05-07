const form = document.getElementById("customer-form");
const tableBody = document.getElementById("customer-table-body");
const token = localStorage.getItem("token");
const apiURL = "http://localhost:8000/customers";

document.addEventListener("DOMContentLoaded", fetchCustomers);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newCustomer = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        address: document.getElementById("address").value
    };

    try {
        const res = await fetch(apiURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(newCustomer)
        });

        if (res.ok) {
            fetchCustomers();  // Refresh the customer list
            form.reset();
        } else {
            const errorJson = await res.json();  // Attempt to get the JSON error details
            alert("Failed to add customer.\n" + errorJson.detail || 'Unknown error');
        }
    } catch (err) {
        console.error("Add customer error:", err);
    }
});

async function fetchCustomers() {
    try {
        const res = await fetch(apiURL, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) {
            const text = await res.text();
            throw new Error(`HTTP error: ${res.status}\n${text}`);
        }

        const customers = await res.json();
        if (!Array.isArray(customers)) {
            throw new Error("Expected an array but got: " + JSON.stringify(customers));
        }
        renderTable(customers);
    } catch (err) {
        console.error("Error fetching customers:", err);
        alert("Failed to fetch customers.\n" + err.message);  // Display the error in the UI
    }
}

function renderTable(customers) {
    tableBody.innerHTML = "";
    customers.forEach((customer) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${customer.customer_id}</td>
      <td>${customer.name}</td>
      <td>${customer.email}</td>
      <td>${customer.phone}</td>
      <td>${customer.address}</td>
      <td>
        <button class="btn btn-edit" onclick="editCustomer(${customer.customer_id})">Edit</button>
        <button class="btn btn-delete" onclick="deleteCustomer(${customer.customer_id})">Delete</button>
      </td>
    `;
        tableBody.appendChild(row);
    });
}

async function deleteCustomer(id) {
    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        if (res.ok) {
            fetchCustomers();  // Refresh the customer list
        } else {
            const errorText = await res.text();
            alert("Failed to delete customer.\n" + errorText);
        }
    } catch (err) {
        console.error("Delete error:", err);
    }
}

async function editCustomer(id) {
    const name = prompt("Enter new name:");
    const email = prompt("Enter new email:");
    const phone = prompt("Enter new phone:");
    const address = prompt("Enter new address:");

    const updatedCustomer = { name, email, phone, address };

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(updatedCustomer)
        });

        if (res.ok) {
            fetchCustomers();  // Refresh the customer list
        } else {
            const errorText = await res.text();
            alert("Failed to update customer.\n" + errorText);
        }
    } catch (err) {
        console.error("Edit error:", err);
    }
}