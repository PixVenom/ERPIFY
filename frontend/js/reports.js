let chartInstance = null;

function loadReport() {
    const type = document.getElementById("report-type").value;
    const ctx = document.getElementById("report-chart").getContext("2d");

    if (chartInstance) {
        chartInstance.destroy();
    }

    if (type === "sales") {
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
                datasets: [{
                    label: 'Sales ($)',
                    data: [1200, 1900, 3000, 2500, 2200],
                    backgroundColor: '#4CAF50'
                }]
            }
        });
    } else if (type === "inventory") {
        chartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Electronics', 'Clothing', 'Groceries', 'Books'],
                datasets: [{
                    label: 'Inventory Count',
                    data: [100, 200, 150, 80],
                    backgroundColor: ['#4CAF50', '#2196F3', '#FFC107', '#FF5722']
                }]
            }
        });
    } else if (type === "payments") {
        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                datasets: [{
                    label: 'Payments Received ($)',
                    data: [500, 1200, 800, 1600],
                    borderColor: '#4CAF50',
                    fill: false,
                    tension: 0.4
                }]
            }
        });
    }
}
