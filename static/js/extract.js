document.addEventListener("DOMContentLoaded", function(){
    let locationButton = document.querySelector("#locationButton")
    let locationDisplay = document.querySelector("#locationDisplay")

    function getLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
      } else { 
        locationDisplay.innerHTML = "Geolocation is not supported by this browser.";
      }
    }
    
    function showPosition(position) {
      locationDisplay.innerHTML = "Latitude: " + position.coords.latitude + 
      "<br>Longitude: " + position.coords.longitude;
    }

    locationButton.addEventListener("click", function(){
        getLocation();
    })
});