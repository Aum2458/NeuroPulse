let chart;

/**
 * Render a diagnosis bar chart using Chart.js
 * @param {string} chartId - Canvas element ID
 * @param {Object} dataObj - { label: confidence }
 */
function renderDiagnosisChart(chartId, dataObj) {
  const canvas = document.getElementById(chartId);
  if (!canvas || !dataObj || Object.keys(dataObj).length === 0) return;

  const ctx = canvas.getContext("2d");

  const labels = Object.keys(dataObj);
  const values = Object.values(dataObj).map(v => parseFloat(v) || 0);

  /* 🎨 Dynamic colors based on confidence */
  const backgroundColors = values.map(v =>
    v >= 80 ? "rgba(75, 192, 192, 0.7)" :
    v >= 50 ? "rgba(255, 206, 86, 0.7)" :
              "rgba(255, 99, 132, 0.7)"
  );

  const borderColors = values.map(v =>
    v >= 80 ? "rgba(75, 192, 192, 1)" :
    v >= 50 ? "rgba(255, 206, 86, 1)" :
              "rgba(255, 99, 132, 1)"
  );

  /* 🔄 Destroy existing chart */
  if (chart) {
    chart.destroy();
  }

  /* 📊 Create chart */
  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Confidence (%)",
        data: values,
        backgroundColor: backgroundColors,
        borderColor: borderColors,
        borderWidth: 2,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: value => `${value}%`
          },
          title: {
            display: true,
            text: "Confidence (%)"
          }
        },
        x: {
          title: {
            display: true,
            text: "Possible Conditions"
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: "AI Diagnosis Confidence Chart",
          font: {
            size: 18
          }
        },
        tooltip: {
          callbacks: {
            label: ctx => `Confidence: ${ctx.parsed.y}%`
          }
        }
      }
    }
  });
}

/* ✅ Auto-load chart with Flask-injected data */
document.addEventListener("DOMContentLoaded", () => {
  const dataEl = document.getElementById("chart-data");
  if (!dataEl) return;

  try {
    const chartData = JSON.parse(dataEl.textContent);
    renderDiagnosisChart("diagnosisChart", chartData);
  } catch (error) {
    console.warn("⚠️ Invalid or missing chart data", error);
  }
});
