const form = document.getElementById("customer-form");
const tableBody = document.getElementById("customer-table-body");
const token = localStorage.getItem("token");
const apiURL = "http://localhost:8000/customers";

document.addEventListener("DOMContentLoaded", fetchCustomers);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newCustomer = {
        name: document.getElementById("customer-name").value,
        email: document.getElementById("customer-email").value,
        phone: document.getElementById("customer-phone").value,
        address: document.getElementById("customer-address").value
    };

    try {
        const res = await fetch(apiURL + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(newCustomer)
        });

        if (res.ok) {
            fetchCustomers();
            form.reset();
        } else {
            alert("Failed to add customer.");
        }
    } catch (err) {
        console.error(err);
    }
});

async function fetchCustomers() {
    try {
        const res = await fetch(apiURL + "/", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        const customers = await res.json();
        renderTable(customers);
    } catch (err) {
        console.error("Error fetching customers:", err);
    }
}

function renderTable(customers) {
    tableBody.innerHTML = "";
    customers.forEach((customer) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${customer.id}</td>
      <td>${customer.name}</td>
      <td>${customer.email}</td>
      <td>${customer.phone}</td>
      <td>${customer.address}</td>
      <td>
        <button class="btn btn-edit" onclick="editCustomer(${customer.id})">Edit</button>
        <button class="btn btn-delete" onclick="deleteCustomer(${customer.id})">Delete</button>
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
            fetchCustomers();
        } else {
            alert("Failed to delete customer.");
        }
    } catch (err) {
        console.error(err);
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
            fetchCustomers();
        } else {
            alert("Failed to update customer.");
        }
    } catch (err) {
        console.error(err);
    }
}
