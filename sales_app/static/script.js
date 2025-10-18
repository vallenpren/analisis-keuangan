// Global Chart.js defaults
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.responsive = true;
Chart.defaults.animation.duration = 1000;
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// 🎨 Warna putih global untuk teks chart
const whiteChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: "#fff", // warna teks legenda
                font: { size: 13 }
            }
        }
    },
    scales: {
        x: {
            ticks: {
                color: "#fff" // warna angka sumbu X
            },
            grid: {
                color: "rgba(255,255,255,0.1)" // garis bantu lembut
            }
        },
        y: {
            ticks: {
                color: "#fff" // warna angka sumbu Y
            },
            grid: {
                color: "rgba(255,255,255,0.1)"
            }
        }
    }
};

fetch("/chart-data")
.then(res => res.json())
.then(data => {
    // --- Chart Pendapatan ---
    new Chart(document.getElementById('chartPendapatan'), {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Pendapatan',
                data: data.pendapatan,
                borderColor: '#2196F3',
                backgroundColor: 'rgba(33,150,243,0.15)',
                fill: true,
                tension: 0.4
            }]
        },
        options: whiteChartOptions
    });

    // --- Chart Laba ---
    new Chart(document.getElementById('chartLaba'), {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Laba Bersih',
                data: data.laba,
                backgroundColor: 'rgba(76,175,80,0.6)',
                borderColor: '#388E3C',
                borderWidth: 1
            }]
        },
        options: whiteChartOptions
    });

    // --- Distribusi Normal ---
    new Chart(document.getElementById('chartDistribusi'), {
        type: 'line',
        data: {
            labels: data.dist_x,
            datasets: [{
                label: 'Distribusi Normal Laba',
                data: data.dist_y,
                borderColor: '#FF9800',
                backgroundColor: 'rgba(255,152,0,0.25)',
                fill: true,
                tension: 0.4
            }]
        },
        options: whiteChartOptions
    });
});
