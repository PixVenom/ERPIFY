const form = document.getElementById("product-form");
const tableBody = document.getElementById("product-table-body");
const token = localStorage.getItem("token");

const apiURL = "http://localhost:8000/products";

document.addEventListener("DOMContentLoaded", fetchProducts);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newProduct = {
        name: document.getElementById("product-name").value,
        price: parseFloat(document.getElementById("product-price").value),
        quantity: parseInt(document.getElementById("product-quantity").value),
        category: document.getElementById("product-category").value
    };

    try {
        const res = await fetch(apiURL + "/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(newProduct)
        });

        if (res.ok) {
            fetchProducts();
            form.reset();
        } else {
            const data = await res.json();
            alert(data.detail || "Failed to add product.");
        }
    } catch (err) {
        console.error(err);
        alert("Error adding product.");
    }
});

async function fetchProducts() {
    try {
        const res = await fetch(apiURL + "/", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        const products = await res.json();
        renderTable(products);
    } catch (err) {
        console.error("Error fetching products:", err);
    }
}

function renderTable(products) {
    tableBody.innerHTML = "";
    products.forEach((product) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>$${product.price}</td>
            <td>${product.quantity}</td>
            <td>${product.category}</td>
            <td>
                <button onclick="editProduct(${product.id})">Edit</button>
                <button onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

async function deleteProduct(id) {
    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        if (res.ok) {
            fetchProducts();
        } else {
            alert("Failed to delete product.");
        }
    } catch (err) {
        console.error(err);
        alert("Error deleting product.");
    }
}

async function editProduct(id) {
    const name = prompt("Enter new product name:");
    const price = prompt("Enter new price:");
    const quantity = prompt("Enter new quantity:");
    const category = prompt("Enter new category:");

    const updatedProduct = { name, price: parseFloat(price), quantity: parseInt(quantity), category };

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(updatedProduct)
        });

        if (res.ok) {
            fetchProducts();
        } else {
            alert("Failed to update product.");
        }
    } catch (err) {
        console.error(err);
        alert("Error updating product.");
    }
}

function logout() {
    localStorage.clear();
    window.location.href = "/frontend/index.html";
}