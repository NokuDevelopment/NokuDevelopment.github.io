function updateData(){
   $.get("data.txt", function(data) {
      const fileDataArray = data.split("%");
      document.getElementById('lastUpdate').innerHTML = fileDataArray[0];
      document.getElementById('RPIStatus').innerHTML = fileDataArray[1];
      document.getElementById('RPIPollingPeriod').innerHTML = fileDataArray[2];
      document.getElementById('temperatureOutput').innerHTML = fileDataArray[3];
      drawChart(fileDataArray[4], fileDataArray[3]);

      if(fileDataArray[1] == "Connected"){
         document.getElementById('RPIStatus').style.color = 'green';
      }
      else if(fileDataArray[1] == "Disconnected"){
         document.getElementById('RPIStatus').style.color = 'red';
      }
      else {
         document.getElementById('RPIStatus').style.color = 'yellow';
      }
   });
}

function drawChart(dataString, currentTemp){
   const dataStringArray = dataString.split('$');
   const dataArray = []
   for(i = 0; i < length(dataStringArray); i++){
      dataArray.push(parseFloat(dataStringArray[i]));
   }

   google.charts.load('current', {'packages':['corechart']});
   google.charts.setOnLoadCallback(drawChart);
   function drawChart() {
      var data = google.visualization.arrayToDataTable([
      ['Time', 'Temperature'],
      ['', dataArray[0]],
      ['', dataArray[1]],
      ['', dataArray[2]],
      ['', dataArray[3]],
      ['', dataArray[4]],
      ['', dataArray[5]],
      ['', dataArray[6]],
      ['', dataArray[7]],
      ['', dataArray[8]],
      ['', dataArray[9]],
      ['', dataArray[10]],
      ['', dataArray[11]],
      ['', dataArray[12]],
      ['', dataArray[13]],
      ['', dataArray[14]],
      ['', dataArray[15]],
      ['', currentTemp]
      ]);

      var options = {
      title: 'Temperature (past 8 hrs.)',
      curveType: 'function',
      legend: {position: 'bottom'}
      };

      var chart = new google.visualization.LineChart(document.getElementById('temperature_chart'));
      chart.draw(data, options)
   }
}

window.addEventListener('load', (event) => {
   updateData();
});