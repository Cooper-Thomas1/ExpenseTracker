let lineChart, doughnutChart;
let alldata, dailydata, weeklydata, monthlydata, yearlydata;
let allcategory, dailycategory, weeklycategory, monthlycategory, yearlycategory;
let allcategorydata, dailycategorydata, weeklycategorydata, monthlycategorydata, yearlycategorydata;

const ctx = document.getElementById('myChart');
lineChart = new Chart(ctx, {
type: 'line',
data: {
  labels: [], // Dates as labels
  datasets: [{
    data: [], // Amounts as data points
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
  labels: [],
  datasets: [{
    data: [],
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

$('.dropdown-menu > li').click(function() {
  var $toggle = $(this).parent().siblings('.dropdown-toggle');
  $toggle.html($(this).text())
});

async function fetchData() {
  const response = await fetch('/api/expenses');
  const data = await response.json();
  return data;
}

fetchData().then(data => {
  try {
    // Sort data by date
    data.sort((a, b) => new Date(a.date) - new Date(b.date));

    var data1 = data.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= new Date().setHours(0,0,0,0);
    });
    var data2 = data.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= new Date((new Date()).setDate((new Date()).getDate() - (new Date()).getDate() + ((new Date()).getDate() === 0 ? -6 : 1))) && itemDate <= new Date();
    });
    var data3 = data.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= new Date(new Date().getFullYear(), new Date().getMonth(), 1) && itemDate <= new Date();
    });
    var data4 = data.filter(item => {
      const itemDate = new Date(item.date);
      return itemDate >= new Date(new Date().getFullYear(), 0, 1) && itemDate <= new Date();
    });

    function getCategoryData(currentdata) {
      const categorySums = {};
      currentdata.forEach(expense => {
        const category = expense.category; // Use the category directly
        if (!categorySums[category]) {
          categorySums[category] = 0;
        }
        categorySums[category] += expense.amount;
      });
      return categorySums;
    }

    const doughnutLabels = Object.keys(getCategoryData(data)), doughnutData = Object.values(getCategoryData(data)); // Sums as data points
    const doughnutLabels1 = Object.keys(getCategoryData(data1)), doughnutData1 = Object.values(getCategoryData(data1));
    const doughnutLabels2 = Object.keys(getCategoryData(data2)), doughnutData2 = Object.values(getCategoryData(data2));
    const doughnutLabels3 = Object.keys(getCategoryData(data3)), doughnutData3 = Object.values(getCategoryData(data3));
    const doughnutLabels4 = Object.keys(getCategoryData(data4)), doughnutData4 = Object.values(getCategoryData(data4));

    lineChart.data.labels = data.map(expense => expense.date);
    lineChart.data.datasets[0].data = data.map(expense => expense.amount);
    lineChart.update();

    doughnutChart.data.labels = doughnutLabels;
    doughnutChart.data.datasets[0].data = doughnutData;
    doughnutChart.update();

    alldata = data, dailydata = data1, weeklydata = data2, monthlydata = data3, yearlydata = data4;
    allcategory = doughnutLabels, dailycategory = doughnutLabels1, weeklycategory = doughnutLabels2, monthlycategory = doughnutLabels3, yearlycategory = doughnutLabels4;
    allcategorydata = doughnutData, dailycategorydata = doughnutData1, weeklycategorydata = doughnutData2, monthlycategorydata = doughnutData3, yearlycategorydata = doughnutData4;

  } catch (error) {
    console.error('Error processing data:', error);
  }
});

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

function updatelineChart(newdata) {
  lineChart.data.labels = newdata.map(expense => expense.date);
  lineChart.data.datasets[0].data = newdata.map(expense => expense.amount);
  lineChart.update();
}

function updatedoughnutChart(newlabel,newdata) {
  doughnutChart.data.labels = newlabel;
  doughnutChart.data.datasets[0].data = newdata;
  doughnutChart.update();
}

function dateFilter(item){
  if (item == 'all'){updatelineChart(alldata), updatedoughnutChart(allcategory, allcategorydata)}
  else if (item == 'day'){updatelineChart(dailydata), updatedoughnutChart(dailycategory, dailycategorydata)}
  else if (item == 'week'){updatelineChart(weeklydata), updatedoughnutChart(weeklycategory, weeklycategorydata)}
  else if (item == 'month'){updatelineChart(monthlydata), updatedoughnutChart(monthlycategory, monthlycategorydata)}
  else if (item == 'year'){updatelineChart(yearlydata), updatedoughnutChart(yearlycategory, yearlycategorydata)}
}
