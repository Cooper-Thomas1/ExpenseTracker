let lineChart, doughnutChart;

(() => {
  fetch('/api/expenses')
    .then(response => response.json())
    .then(data => {
      const categorySums = {};
      data.forEach(expense => {
        const category = expense.category; // Use the category directly
        if (!categorySums[category]) {
          categorySums[category] = 0;
        }
        categorySums[category] += expense.amount;
      });

      const doughnutLabels = Object.keys(categorySums); // Categories as labels
      const doughnutData = Object.values(categorySums); // Sums as data points
      
      // Line Chart
      const ctx = document.getElementById('myChart');
      lineChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.map(expense => expense.date), // Dates as labels
          datasets: [{
            data: data.map(expense => expense.amount), // Amounts as data points
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#007bff',
            borderWidth: 4,
            pointBackgroundColor: '#007bff'
          }]
        },
        options: {
          plugins: {
            legend: { display: false },
            tooltip: { boxPadding: 3 }
          }
        }
      });

      // Doughnut Chart
      const ctx2 = document.getElementById('myChart2');
      doughnutChart = new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: doughnutLabels,
          datasets: [{
            data: doughnutData,
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(153, 102, 255)',
            ],
          }]
        },
        options: {
          plugins: {
            legend: { display: false },
            tooltip: { boxPadding: 3 }
          }
        }
      });
    })
    .catch(error => {
      console.error('Error fetching expense data:', error);
    });
})();

document.getElementById('downloadBothCharts').addEventListener('click', () => {
  if (lineChart && doughnutChart) {
    const lineLink = document.createElement('a');
    lineLink.href = lineChart.toBase64Image();
    lineLink.download = 'line_chart.png';
    lineLink.click();

    const doughnutLink = document.createElement('a');
    doughnutLink.href = doughnutChart.toBase64Image();
    doughnutLink.download = 'doughnut_chart.png';
    doughnutLink.click();
  } else {
    console.error("Charts are not ready yet.");
  }
});

