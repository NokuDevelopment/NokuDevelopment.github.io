function updateTemp(){
   $.get("data.txt", function(data) {
      $('#temperatureOutput').html(data);
      document.getElementById("temperatureOutput").innerHTML = data;
      console.log(data);
   });
}

window.addEventListener('load', (event) => {
   console.log('Window loaded');
   updateTemp();
   console.log("Temperature updated");
});