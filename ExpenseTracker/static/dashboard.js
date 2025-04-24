(() => {
  fetch('/api/expenses')
    .then(response => response.json())
    .then(data => {
      const labels = data.map(expense => expense.date); // Extract dates for labels
      const amounts = data.map(expense => expense.amount); // Extract amounts for data points

      const ctx = document.getElementById('myChart');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            data: amounts,
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
    })
    .catch(error => {
      console.error('Error fetching expense data:', error);
    });
})();