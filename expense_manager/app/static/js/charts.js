// charts.js – Chart.js rendering helpers

const PALETTE = [
  '#0d6efd', '#20c997', '#fd7e14', '#dc3545',
  '#6f42c1', '#0dcaf0', '#ffc107', '#198754',
  '#6c757d', '#e83e8c'
];

function monthLabel(m, y) {
  const d = new Date(y, m - 1, 1);
  return d.toLocaleString('default', { month: 'short', year: '2-digit' });
}

let monthlyChartInstance = null;
let categoryChartInstance = null;

function renderMonthlyChart(data) {
  const ctx = document.getElementById('monthlyChart');
  if (!ctx) return;

  if (monthlyChartInstance) monthlyChartInstance.destroy();

  const labels = data.map(d => monthLabel(d.month, d.year));
  const values = data.map(d => d.total);

  monthlyChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Total Spend',
        data: values,
        backgroundColor: 'rgba(13, 110, 253, 0.18)',
        borderColor: '#0d6efd',
        borderWidth: 2,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => '₹' + Number(ctx.raw).toLocaleString('en-IN', { minimumFractionDigits: 2 })
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: v => '₹' + Number(v).toLocaleString('en-IN')
          },
          grid: { color: 'rgba(0,0,0,0.05)' }
        },
        x: { grid: { display: false } }
      }
    }
  });
}

function renderCategoryChart(data) {
  const ctx = document.getElementById('categoryChart');
  if (!ctx) return;

  if (categoryChartInstance) categoryChartInstance.destroy();

  if (!data.length) {
    ctx.parentElement.innerHTML += '<p class="text-muted text-center small mt-3">No data for this month.</p>';
    return;
  }

  const labels = data.map(d => d.category);
  const values = data.map(d => d.total);

  categoryChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: PALETTE.slice(0, labels.length),
        borderWidth: 2,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      cutout: '60%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { boxWidth: 12, padding: 12, font: { size: 12 } }
        },
        tooltip: {
          callbacks: {
            label: ctx => {
              const total = ctx.dataset.data.reduce((a, b) => a + b, 0);
              const pct = ((ctx.raw / total) * 100).toFixed(1);
              return `₹${Number(ctx.raw).toLocaleString('en-IN', { minimumFractionDigits: 2 })} (${pct}%)`;
            }
          }
        }
      }
    }
  });
}
