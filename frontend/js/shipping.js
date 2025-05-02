const form = document.getElementById("shipping-form");
const tableBody = document.getElementById("shipping-table-body");
const token = localStorage.getItem("token");
const apiURL = "http://localhost:8000/shipping";

document.addEventListener("DOMContentLoaded", fetchShipping);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newShipping = {
        invoice_id: parseInt(document.getElementById("invoice-id").value),
        shipping_date: document.getElementById("shipping-date").value,
        shipping_status: document.getElementById("shipping-status").value
    };

    try {
        const res = await fetch(apiURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(newShipping)
        });

        if (res.ok) {
            await fetchShipping();
            form.reset();
        } else {
            const data = await res.json().catch(() => ({}));
            alert(data.detail || "Failed to add shipping record.");
        }
    } catch (err) {
        console.error(err);
        alert("Error adding shipping record.");
    }
});

async function fetchShipping() {
    try {
        const res = await fetch(apiURL, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) {
            throw new Error("Failed to fetch shipping records");
        }

        const records = await res.json();
        renderTable(records);
    } catch (err) {
        console.error(err);
        alert("Could not load shipping data.");
    }
}

function renderTable(records) {
    tableBody.innerHTML = "";
    records.forEach((record) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${record.shipping_id}</td>
      <td>${record.invoice_id}</td>
      <td>${record.shipping_date}</td>
      <td>${record.shipping_status}</td>
      <td>
        <button onclick="deleteShipping(${record.shipping_id})">Delete</button>
      </td>
    `;
        tableBody.appendChild(row);
    });
}

async function deleteShipping(id) {
    if (!confirm("Are you sure you want to delete this shipping record?")) return;

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (res.ok) {
            await fetchShipping();
        } else {
            alert("Failed to delete shipping record.");
        }
    } catch (err) {
        console.error(err);
        alert("Error deleting shipping record.");
    }
}

function logout() {
    localStorage.clear();
    window.location.href = "/frontend/index.html";
}
