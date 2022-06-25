function updateData(){
   $.get("data.txt", function(data) {
      $('#temperatureOutput').html(data);
      document.getElementById("temperatureOutput").innerHTML = data;
      console.log(data);
   });
}

function updateData(){
   $.get("data.txt", function(data) {
      
   });
}

window.addEventListener('load', (event) => {
   updateData();
});