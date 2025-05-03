(() => {
  let allExpenses = [];
  let lineChartInstance = null;
  let doughnutChartInstance = null;

  fetch('/api/expenses')
    .then(response => response.json())
    .then(data => {
      allExpenses = data;
      renderCharts(data); // Render charts with all data by default
    })
    .catch(error => {
      console.error('Error fetching expense data:', error);
    });

  function filterExpenses(period) {
    
    const now = new Date();
    let filteredExpenses = [];

    if (period === 'week') {
      const lastWeek = new Date();
      lastWeek.setDate(now.getDate() - 7);
      filteredExpenses = allExpenses.filter(expense => new Date(expense.date) >= lastWeek);
      console.log('Example date:', expense.date, '->', new Date(expense.date));
    } else if (period === 'month') {
      const lastMonth = new Date();
      lastMonth.setMonth(now.getMonth() - 1);
      filteredExpenses = allExpenses.filter(expense => new Date(expense.date) >= lastMonth);
    } else if (period === 'year') {
      const lastYear = new Date();
      lastYear.setFullYear(now.getFullYear() - 1);
      filteredExpenses = allExpenses.filter(expense => new Date(expense.date) >= lastYear);
    } else {
      filteredExpenses = allExpenses;
    }

    renderCharts(filteredExpenses);
  }

  function renderCharts(data) {
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

    const ctx = document.getElementById('myChart');
    const ctx2 = document.getElementById('myChart2');

    // Destroy previous charts if they exist
    if (lineChartInstance) lineChartInstance.destroy();
    if (doughnutChartInstance) doughnutChartInstance.destroy();

    lineChartInstance = new Chart(ctx, {
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
    doughnutChartInstance = new Chart(ctx2, {
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
  }

  window.filterExpenses = filterExpenses;
})();
