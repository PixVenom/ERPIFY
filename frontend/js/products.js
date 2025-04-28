document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("product-form");
    const tableBody = document.getElementById("product-table-body");
    const token = localStorage.getItem("token");
    const apiURL = "http://localhost:8000/products";

    fetchProducts();

    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            const newProduct = {
                name: document.getElementById("productName").value,
                price: parseFloat(document.getElementById("price").value),
                quantity: parseInt(document.getElementById("quantity").value),
                category: document.getElementById("category").value
            };

            try {
                const res = await fetch(apiURL + "/frontend/js/products", {
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
                    alert("Failed to add product.");
                }
            } catch (err) {
                console.error("Error submitting product:", err);
            }
        });
    }

    async function fetchProducts() {
        try {
            const res = await fetch(apiURL + "/frontend/js/products.js", {
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
        tableBody.innerHTML = "/frontend/products.html";
        if (!Array.isArray(products)) {
            console.error("Expected array, got:", products);
            return;
        }

        products.forEach((product) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>$${product.price}</td>
                <td>${product.quantity}</td>
                <td>${product.category}</td>
                <td>
                    <button class="btn btn-edit" onclick="editProduct(${product.id})">Edit</button>
                    <button class="btn btn-delete" onclick="deleteProduct(${product.id})">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    window.deleteProduct = async function (id) {
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
            console.error("Error deleting product:", err);
        }
    };

    window.editProduct = async function (id) {
        const name = prompt("Enter new product name:");
        const price = prompt("Enter new price:");
        const quantity = prompt("Enter new quantity:");
        const category = prompt("Enter new category:");

        const updatedProduct = {
            name,
            price: parseFloat(price),
            quantity: parseInt(quantity),
            category
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
                fetchProducts();
            } else {
                alert("Failed to update product.");
            }
        } catch (err) {
            console.error("Error updating product:", err);
        }
    };
});