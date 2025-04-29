const form = document.getElementById("product-form");
const tableBody = document.getElementById("product-table-body");
const token = localStorage.getItem("token");

const apiURL = "http://localhost:8000/products"; // Correct backend API URL

document.addEventListener("DOMContentLoaded", fetchProducts);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newProduct = {
        name: document.getElementById("product-name").value,
        price: parseFloat(document.getElementById("product-price").value),
        category: document.getElementById("product-category").value,
        supplier_id: parseInt(document.getElementById("product-supplier-id").value)
    };

    try {
        const res = await fetch(apiURL, { // Fixed extra "/" here
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(newProduct)
        });

        if (res.ok) {
            await fetchProducts();
            form.reset();
        } else {
            const data = await res.json().catch(() => ({}));
            alert(data.detail || "Failed to add product.");
        }
    } catch (err) {
        console.error(err);
        alert("Error adding product.");
    }
});

async function fetchProducts() {
    try {
        const res = await fetch(apiURL, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) {
            throw new Error(`Failed to fetch products: ${res.status}`);
        }

        const products = await res.json();
        renderTable(products);
    } catch (err) {
        console.error("Error fetching products:", err);
        alert("Failed to load products.");
        renderTable([]); // Ensure empty table is rendered when there's an error
    }
}

function renderTable(products) {
    tableBody.innerHTML = "";

    if (products.length === 0) {
        const row = document.createElement("tr");
        row.innerHTML = "<td colspan='6'>No products available</td>";
        tableBody.appendChild(row);
        return;
    }

    products.forEach((product) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${product.product_id}</td>
            <td>${product.name}</td>
            <td>₹${product.price}</td>
            <td>${product.category}</td>
            <td>${product.supplier_id}</td>
            <td>
                <button onclick="editProduct(${product.product_id})">Edit</button>
                <button onclick="deleteProduct(${product.product_id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

async function deleteProduct(id) {
    if (!confirm("Are you sure you want to delete this product?")) return;

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (res.ok) {
            await fetchProducts();
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
    const category = prompt("Enter new category:");
    const supplier_id = prompt("Enter new supplier ID:");

    const updatedProduct = {
        name,
        price: parseFloat(price),
        category,
        supplier_id: parseInt(supplier_id)
    };

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
            await fetchProducts();
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