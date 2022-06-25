function updateData(){
   $.get("data.txt", function(data) {
      const fileDataArray = data.split("%");
      $('#lastUpdate').html(fileDataArray[0]);
      $('#RPIStatus').html(fileDataArray[1]);
      $('#RPIPollingPeriod').html(fileDataArray[2]);
      $('#temperatureOutput').html(fileDataArray[3]);
   });
}

window.addEventListener('load', (event) => {
   updateData();
});