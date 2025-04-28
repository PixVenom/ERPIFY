const form = document.getElementById("employee-form");
const tableBody = document.getElementById("employee-table-body");

let employees = [];

form.addEventListener("submit", function (e) {
    e.preventDefault();

    const employee = {
        id: document.getElementById("employee-id").value,
        name: document.getElementById("employee-name").value,
        position: document.getElementById("position").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        department: document.getElementById("department").value
    };

    employees.push(employee);
    renderTable();
    form.reset();
});

function renderTable() {
    tableBody.innerHTML = "";
    employees.forEach((employee, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
      <td>${employee.id}</td>
      <td>${employee.name}</td>
      <td>${employee.position}</td>
      <td>${employee.email}</td>
      <td>${employee.phone}</td>
      <td>${employee.department}</td>
      <td>
        <button class="btn btn-edit" onclick="editEmployee(${index})">Edit</button>
        <button class="btn btn-delete" onclick="deleteEmployee(${index})">Delete</button>
      </td>
    `;
        tableBody.appendChild(row);
    });
}

function deleteEmployee(index) {
    employees.splice(index, 1);
    renderTable();
}

function editEmployee(index) {
    const emp = employees[index];
    document.getElementById("employee-id").value = emp.id;
    document.getElementById("employee-name").value = emp.name;
    document.getElementById("position").value = emp.position;
    document.getElementById("email").value = emp.email;
    document.getElementById("phone").value = emp.phone;
    document.getElementById("department").value = emp.department;
    employees.splice(index, 1);
}
