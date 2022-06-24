function refreshPage(){
   const axios = require('axios');

   var intervalId = window.setInterval(function(){
      axios
         .get('https://google.com')
         .then(res => {
            console.log(`statusCode: ${res.status}`);
            console.log(res);
         })
         .catch(error => {
            console.error(error);
   });

   }, 5000);
}