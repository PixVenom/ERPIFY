const form = document.getElementById("payment-form");
const tableBody = document.getElementById("payment-table-body");

let payments = [];

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const payment = {
        id: document.getElementById("payment-id").value,
        invoice: document.getElementById("invoice-id").value,
        customer: document.getElementById("customer-name").value,
        amount: document.getElementById("amount-paid").value,
        date: document.getElementById("payment-date").value,
        method: document.getElementById("payment-method").value
    };

    payments.push(payment);
    renderTable();
    form.reset();
});

function renderTable() {
    tableBody.innerHTML = "";
    payments.forEach((payment, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${payment.id}</td>
      <td>${payment.invoice}</td>
      <td>${payment.customer}</td>
      <td>${payment.amount}</td>
      <td>${payment.date}</td>
      <td>${payment.method}</td>
      <td>
        <button class="btn btn-edit" onclick="editPayment(${index})">Edit</button>
        <button class="btn btn-delete" onclick="deletePayment(${index})">Delete</button>
      </td>
    `;
        tableBody.appendChild(row);
    });
}

function deletePayment(index) {
    payments.splice(index, 1);
    renderTable();
}

function editPayment(index) {
    const payment = payments[index];
    document.getElementById("payment-id").value = payment.id;
    document.getElementById("invoice-id").value = payment.invoice;
    document.getElementById("customer-name").value = payment.customer;
    document.getElementById("amount-paid").value = payment.amount;
    document.getElementById("payment-date").value = payment.date;
    document.getElementById("payment-method").value = payment.method;
    payments.splice(index, 1);
}
