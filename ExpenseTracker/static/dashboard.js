(() => {
  fetch('/api/expenses')
    .then(response => response.json())
    .then(data => {
      const labels = data.map(expense => expense.date); // Extract dates for labels
      const amounts = data.map(expense => expense.amount); // Extract amounts for data points
      const categories = data.map(expense => expense.category);
      
      //bit messy, functionally should work
      var food = [];
      var transport = [];
      var entertainment = [];
      var misc = [];
      var utilities = [];
      for ( i=0; i < categories.length; i++ ){
        if ( categories[i] == "food" ){
          food.push( i );
        }
        else if ( categories[i] == "transport" ){
          transport.push( i );
        }
        else if (  categories[i] == "entertainment" ){
          entertainment.push( i );
        }
        else if ( categories[i] == "misc" ){
          misc.push( i );
        }
        else if ( categories[i] == "utilities" ){
          utilities.push( i );
        }
      }
      foodsum = [];
      for ( i=0; i < food.length; i++ ){
        foodsum.push(amounts[food[i]]);
      }
      transportsum = [];
      for ( i=0; i < transport.length; i++ ){
        transportsum.push(amounts[transport[i]]);
      }
      entertainmentsum = [];
      for ( i=0; i < entertainment.length; i++ ){
        entertainmentsum.push(amounts[entertainment[i]]);
      }
      miscsum = [];
      for ( i=0; i < misc.length; i++ ){
        miscsum.push(amounts[misc[i]]);
      }
      utilitiessum = [];
      for ( i=0; i < utilities.length; i++ ){
        utilitiessum.push(amounts[utilities[i]]);
      }
      

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
      const ctx2 = document.getElementById('myChart2');
      new Chart(ctx2, {
        type: 'doughnut',
        data: {
          labels: ['Food', 'Transport', 'Entertainment', 'Misc', 'Utilities'],
          datasets: [{
            data: [foodsum.reduce((a,b) => a + b, 0),transportsum.reduce((a,b) => a+b,0), entertainmentsum.reduce((a,b) => a + b, 0), miscsum.reduce((a,b) => a + b, 0), utilitiessum.reduce((a,b) => a + b, 0)],
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
