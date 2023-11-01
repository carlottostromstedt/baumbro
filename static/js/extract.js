document.addEventListener("DOMContentLoaded", function(){
    let locationButton = document.querySelector("#locationButton")
    let locationDisplay = document.querySelector("#locationDisplay")
    const form = document.forms.locationExtract;
    let latitudeField = document.querySelector('#latitude')
    let longitudeField = document.querySelector('#longitude')

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
      latitudeField.value= position.coords.latitude
      longitudeField.value = position.coords.longitude
    }

    function addPosition(position){
      
    }

    locationButton.addEventListener("click", function(){
        getLocation();
    })
});