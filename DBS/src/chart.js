export function createLevelChart(canvasEl) {
  const ctx = canvasEl.getContext("2d");

  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "Level (cm)",
        data: [],
        tension: 0.2,
        pointRadius: 2
      }]
    },
    options: {
      responsive: true,
      animation: false,
      scales: {
        x: { title: { display: true, text: "Time" } },
        y: { title: { display: true, text: "cm" } }
      }
    }
  });

  return {
    setData(points) {
      // points: [{ts, level_cm}]
      const labels = [];
      const values = [];

      for (const p of points) {
        const tsMs = (p.ts ?? 0) * 1000;
        labels.push(tsMs ? new Date(tsMs).toLocaleTimeString() : "");
        values.push(p.level_cm);
      }

      chart.data.labels = labels;
      chart.data.datasets[0].data = values;
      chart.update();
    }
  };
}
