(() => {
  fetch('/api/expenses')
    .then(response => response.json())
    .then(data => {
      // Sort data by date
      data.sort((a, b) => new Date(a.date) - new Date(b.date));

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
      new Chart(ctx, {
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
      new Chart(ctx2, {
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
