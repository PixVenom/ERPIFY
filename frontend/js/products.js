const form = document.getElementById("product-form");
const cardContainer = document.getElementById("product-card-container");
const token = localStorage.getItem("token");
const apiURL = "http://127.0.0.1:8000/products";

document.addEventListener("DOMContentLoaded", fetchProducts);

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newProduct = {
        name: document.getElementById("product-name").value.trim(),
        price: parseFloat(document.getElementById("product-price").value),
        category: document.getElementById("product-category").value.trim(),
        supplier_id: parseInt(document.getElementById("product-supplier-id").value)
    };

    try {
        const res = await fetch(apiURL, {
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
            showToast("Product Added");
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

        if (!res.ok) throw new Error(`Failed to fetch products: ${res.status}`);
        const products = await res.json();
        renderCards(products);
    } catch (err) {
        renderCards([]);
    }
}

function renderCards(products) {
    cardContainer.innerHTML = "";

    if (!products || products.length === 0) {
        cardContainer.innerHTML = "<p class='no-products'>No products available</p>";
        return;
    }

    products.forEach((product) => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <h3>${product.name}</h3>
            <p><strong>Price:</strong> ₹${product.price}</p>
            <p><strong>Category:</strong> ${product.category || "N/A"}</p>
            <p><strong>Supplier ID:</strong> ${product.supplier_id || "N/A"}</p>
            <p><strong>ID:</strong> ${product.product_id}</p>
            <div class="actions">
                <button class="edit" onclick="editProduct(${product.product_id})">Edit</button>
                <button class="delete" onclick="deleteProduct(${product.product_id})">Delete</button>
            </div>
        `;
        cardContainer.appendChild(card);
    });
}

async function deleteProduct(id) {
    if (!confirm("Are you sure you want to delete this product?")) return;

    try {
        const res = await fetch(`${apiURL}?product_id=${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (res.ok) {
            await fetchProducts();
            showToast("Product Deleted");
        } else {
            const data = await res.json().catch(() => ({}));
            alert(data.detail || "Failed to delete product.");
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

    if (!name || !price || isNaN(price)) {
        alert("Invalid input.");
        return;
    }

    const updatedProduct = {
        name: name.trim(),
        price: parseFloat(price),
        category: category.trim(),
        supplier_id: parseInt(supplier_id)
    };

    try {
        const res = await fetch(`${apiURL}?product_id=${id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            },
            body: JSON.stringify(updatedProduct)
        });

        if (res.ok) {
            await fetchProducts();
            showToast("Product Updated");
        } else {
            const data = await res.json().catch(() => ({}));
            alert(data.detail || "Failed to update product.");
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

function showToast(message) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}