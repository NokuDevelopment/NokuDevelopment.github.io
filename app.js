function updateData(){
   $.get("data.txt", function(data) {
      const fileDataArray = data.split("%");
      document.getElementById('lastUpdate').innerHTML = fileDataArray[0];
      document.getElementById('RPIStatus').innerHTML = fileDataArray[1];
      document.getElementById('RPIPollingPeriod').innerHTML = fileDataArray[2];
      document.getElementById('temperatureOutput').innerHTML = fileDataArray[3];

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

window.addEventListener('load', (event) => {
   updateData();
});