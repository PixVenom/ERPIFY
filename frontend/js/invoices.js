const form = document.getElementById("invoice-form");
const tableBody = document.getElementById("invoice-table-body");

let invoices = [];

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const invoice = {
        id: document.getElementById("invoice-id").value,
        customer: document.getElementById("customer-name").value,
        date: document.getElementById("invoice-date").value,
        amount: document.getElementById("total-amount").value,
        status: document.getElementById("status").value
    };

    invoices.push(invoice);
    renderTable();
    form.reset();
});

function renderTable() {
    tableBody.innerHTML = "";
    invoices.forEach((invoice, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${invoice.id}</td>
      <td>${invoice.customer}</td>
      <td>${invoice.date}</td>
      <td>${invoice.amount}</td>
      <td>${invoice.status}</td>
      <td>
        <button class="btn btn-edit" onclick="editInvoice(${index})">Edit</button>
        <button class="btn btn-delete" onclick="deleteInvoice(${index})">Delete</button>
      </td>
    `;
        tableBody.appendChild(row);
    });
}

function deleteInvoice(index) {
    invoices.splice(index, 1);
    renderTable();
}

function editInvoice(index) {
    const invoice = invoices[index];
    document.getElementById("invoice-id").value = invoice.id;
    document.getElementById("customer-name").value = invoice.customer;
    document.getElementById("invoice-date").value = invoice.date;
    document.getElementById("total-amount").value = invoice.amount;
    document.getElementById("status").value = invoice.status;
    invoices.splice(index, 1);
}
