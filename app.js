function updateData(){
   $.get("data.txt", function(data) {
      const fileDataArray = data.split("%");
      document.getElementById('lastUpdate').innerHTML = fileDataArray[0];
      document.getElementById('RPIStatus').innerHTML = fileDataArray[1];
      document.getElementById('RPIPollingPeriod').innerHTML = fileDataArray[2];
      console.log(fileDataArray[2]);
      console.log(fileDataArray[3]);
      document.getElementById('temperatureOutput').innerHTML = fileDataArray[3];
   });
}

window.addEventListener('load', (event) => {
   updateData();
});