const form = document.getElementById("product-form");
const cardContainer = document.getElementById("product-card-container");
const apiURL = "http://127.0.0.1:8000/products";

// Check for token and fetch products
// Login handler (for index.html or login form)
// Only attaches if the login form is present on the page
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("http://127.0.0.1:8000/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem("access_token", response.access_token); // ✅ Store token
                    showToast("✅ Login successful! Redirecting...");
                    setTimeout(() => {
                        window.location.href = "/frontend/products.html";
                    }, 1000);
                } else {
                    alert(data.detail || "❌ Login failed.");
                }
            } catch (err) {
                console.error(err);
                alert("❌ Something went wrong during login.");
            }
        });
    }
});


// Fetch products
async function fetchProducts(token) {
    try {
        const res = await fetch(apiURL, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!res.ok) throw new Error(`Failed to fetch products: ${res.status}`);
        const products = await res.json();
        renderCards(products, token);
    } catch (err) {
        console.error(err);
        renderCards([], token);
        alert("❌ Could not fetch products. Please check your access rights.");
    }
}

// Render product cards
function renderCards(products, token) {
    cardContainer.innerHTML = "";

    if (!products || products.length === 0) {
        cardContainer.innerHTML = "<p class='no-products'>No products available</p>";
        return;
    }

    products.forEach((product) => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <h1>${product.product_id}</h1>
            <h3>${product.name}</h3>
            <p><strong>Price:</strong> ₹${product.price}</p>
            <p><strong>Category:</strong> ${product.category || "N/A"}</p>
            <p><strong>Supplier ID:</strong> ${product.supplier_id || "N/A"}</p>
            <div class="actions">
                <button class="edit" onclick="editProduct(${product.product_id}, '${token}')">✏️ Edit</button>
                <button class="delete" onclick="deleteProduct(${product.product_id}, '${token}')">🗑️ Delete</button>
            </div>
        `;
        cardContainer.appendChild(card);
    });
}

// Delete product
async function deleteProduct(id, token) {
    if (!confirm("Are you sure you want to delete this product?")) return;

    try {
        const res = await fetch(`${apiURL}/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await res.json().catch(() => ({}));

        if (res.ok) {
            await fetchProducts(token);
            showToast("🗑️ Product Deleted");
        } else {
            alert(data.detail || "❌ Failed to delete product.");
        }
    } catch (err) {
        console.error(err);
        alert("❌ Error deleting product.");
    }
}

// Edit product
async function editProduct(id, token) {
    const name = prompt("Enter new product name:");
    const price = prompt("Enter new price:");
    const category = prompt("Enter new category:");
    const supplier_id = prompt("Enter new supplier ID:");

    if (!name || !price || isNaN(price)) {
        alert("❌ Invalid input.");
        return;
    }

    const updatedProduct = {
        name: name.trim(),
        price: parseFloat(price),
        category: category.trim(),
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

        const data = await res.json().catch(() => ({}));

        if (res.ok) {
            await fetchProducts(token);
            showToast("✏️ Product Updated");
        } else {
            alert(data.detail || "❌ Failed to update product.");
        }
    } catch (err) {
        console.error(err);
        alert("❌ Error updating product.");
    }
}

// Logout function
function logout() {
    localStorage.clear();
    window.location.href = "/frontend/index.html";
}

// Toast notification
function showToast(message) {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}
